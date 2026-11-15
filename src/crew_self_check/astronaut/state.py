"""Application state: session, language, section, the journey and what was recorded. No UI.

The demo runs on **simulated time**: the journey (C5, D-013) moves day by day from Earth through
the spacecraft to the planet, and what the astronaut records is stamped with that day. A fixed
``clock`` can be injected (tests do); by default the clock is the journey itself.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from enum import StrEnum

from crew_self_check.astronaut.access import AccessDirectory, AccessError
from crew_self_check.astronaut.ground_client import GroundLink, GroundRejected, GroundUnreachable
from crew_self_check.astronaut.mood import check_level, mood_measurement
from crew_self_check.astronaut.pulse_mission import PulseMission
from crew_self_check.astronaut.share_model import (
    DEFAULT_GROUND_DELAY_MINUTES,
    DeliveryState,
    OutboxItem,
    delivery_state,
)
from crew_self_check.core.contract import (
    CrewProfile,
    Indicator,
    Measurement,
    Status,
    System,
    SystemStatus,
)
from crew_self_check.core.fhir import ShareSelection, build_bundle, check_bundle
from crew_self_check.core.reasons import Language
from crew_self_check.core.scenario import Scenario, ScenarioDay, generate_scenario
from crew_self_check.core.status import IndicatorResolution, resolve_indicator, resolve_system
from crew_self_check.core.storage import InMemoryMeasurementStore, MeasurementStore

START_LABEL = "E-1"  # the journey opens on the last day on Earth, with a full history behind it
_MIDDAY = timedelta(hours=12)


class Section(StrEnum):
    HOME = "home"
    CHECKIN = "checkin"
    BODY = "body"
    SUMMARY = "summary"


class AppState:
    def __init__(
        self,
        directory: AccessDirectory,
        clock: Callable[[], datetime] | None = None,
        scenario: Scenario | None = None,
        store: MeasurementStore | None = None,
        ground_link: GroundLink | None = None,
    ) -> None:
        self._directory = directory
        self._ground_link = ground_link
        self._clock = clock
        self.scenario = scenario or generate_scenario()
        self.language = Language.EN  # English is the source language (D-016)
        self.section = Section.HOME
        self.profile: CrewProfile | None = None
        self.code: str | None = None
        self.error: AccessError | None = None
        self.journey_day = next((d.index for d in self.scenario.days if d.label == START_LABEL), 0)
        self.environment = self.current_day.environment
        # What the astronaut records lives behind a storage port (A2); memory unless injected.
        self._store: MeasurementStore = store or InMemoryMeasurementStore()
        self.pulse: PulseMission | None = None
        self.mood_choice: int | None = None  # the face tapped and not saved yet
        self.selected_system: System | None = None
        # Sharing with the ground team (A10): nothing leaves without the astronaut's confirmation.
        self.share_selection: set[Indicator] = set()
        self.share_confirmed = False
        self.ground_delay_minutes = DEFAULT_GROUND_DELAY_MINUTES
        self.outbox: list[OutboxItem] = []
        self.ground_inbox: list[
            OutboxItem
        ] = []  # the simulated inbox, used when no ground is linked
        self.ground_error: str | None = None  # "unreachable" while a package waits to be resent
        self._unsent: list[OutboxItem] = []

    @property
    def logged_in(self) -> bool:
        return self.profile is not None

    def demo_codes(self) -> tuple[str, ...]:
        return self._directory.codes()

    def login(self, typed: str) -> bool:
        """Try a code. A failure never locks the astronaut out and never ends a session."""
        result = self._directory.login(typed)
        self.error = result.error
        if result.profile is None:
            return False
        self.profile, self.code = result.profile, result.code
        self.section = Section.HOME
        self.pulse = None
        self.mood_choice = None
        self.selected_system = None
        self.clear_share()
        return True

    def logout(self) -> None:
        self.profile = None
        self.code = None
        self.error = None
        self.section = Section.HOME
        self.pulse = None  # an unfinished mission is abandoned; what was saved stays
        self.mood_choice = None
        self.selected_system = None
        self.clear_share()

    def set_language(self, language: Language) -> None:
        self.language = language

    def go(self, section: Section) -> None:
        if self.logged_in:
            self.section = section

    # --- the journey (A7) ------------------------------------------------------------------

    @property
    def current_day(self) -> ScenarioDay:
        return self.scenario.days[self.journey_day]

    def journey_time(self) -> datetime:
        """The simulated "now": midday of the current day."""
        return self.current_day.timestamp + _MIDDAY

    def set_day(self, index: int) -> None:
        if not 0 <= index < len(self.scenario.days):
            raise IndexError(f"day {index} is outside 0..{len(self.scenario.days) - 1}")
        self.journey_day = index
        self.environment = self.current_day.environment
        self._sync_ground()
        self._deliver()

    def advance(self) -> None:
        if self.journey_day < len(self.scenario.days) - 1:
            self.set_day(self.journey_day + 1)

    def previous(self) -> None:
        if self.journey_day > 0:
            self.set_day(self.journey_day - 1)

    def _now(self) -> datetime:
        return self._clock() if self._clock is not None else self.journey_time()

    # --- the manual pulse ------------------------------------------------------------------

    def start_pulse(self) -> None:
        if self.logged_in:
            self.pulse = PulseMission()

    def cancel_pulse(self) -> None:
        self.pulse = None

    def save_pulse(self) -> Measurement:
        """Record the finished mission as a contract measurement of this person."""
        if self.pulse is None or self.profile is None:
            raise RuntimeError("there is no pulse mission to save")
        measurement = self.pulse.to_measurement(self.profile.crew_id, self.environment, self._now())
        self._store.add(measurement)
        self.pulse = None
        return measurement

    def preview_pulse(self) -> IndicatorResolution | None:
        """What the counted pulse would be compared with, before it is saved (nothing is stored)."""
        if self.pulse is None or self.profile is None:
            return None
        if self.pulse.result is None or not self.pulse.result.valid:
            return None
        counted = self.pulse.to_measurement(self.profile.crew_id, self.environment, self._now())
        return resolve_indicator(
            (*self.visible_measurements(), counted),
            self.profile.crew_id,
            Indicator.RESTING_HR,
            self.environment,
            profile=self.profile,
            as_of=self.journey_time(),
        )

    # --- the mood survey -------------------------------------------------------------------

    def choose_mood(self, level: int) -> None:
        self.mood_choice = check_level(level)

    def save_mood(self) -> Measurement:
        """Record the chosen face as a contract measurement of this person."""
        if self.profile is None or self.mood_choice is None:
            raise RuntimeError("there is no mood choice to save")
        measurement = mood_measurement(
            self.profile.crew_id, self.mood_choice, self.environment, self._now()
        )
        self._store.add(measurement)
        self.mood_choice = None
        return measurement

    # --- what this person recorded ---------------------------------------------------------

    def own_measurements(self) -> tuple[Measurement, ...]:
        """What the astronaut recorded in the app (not the simulated history)."""
        if self.profile is None:
            return ()
        return self._store.for_crew(self.profile.crew_id)

    def _last(self, indicator: Indicator) -> Measurement | None:
        found = [m for m in self.own_measurements() if m.indicator is indicator]
        return found[-1] if found else None

    def last_pulse(self) -> Measurement | None:
        return self._last(Indicator.RESTING_HR)

    def last_mood(self) -> Measurement | None:
        return self._last(Indicator.MOOD)

    # --- the calculated states (C3, C4) ----------------------------------------------------

    def visible_measurements(self) -> tuple[Measurement, ...]:
        """This person's simulated history plus what they recorded, up to the end of the day."""
        if self.profile is None:
            return ()
        crew_id = self.profile.crew_id
        cutoff = self.current_day.timestamp + timedelta(days=1)
        pool = [*self.scenario.measurements, *self._store.all()]
        mine = [m for m in pool if m.crew_id == crew_id and m.timestamp < cutoff]
        return tuple(sorted(mine, key=lambda m: m.timestamp))

    def resolutions(self) -> dict[Indicator, IndicatorResolution]:
        """The status of every indicator in the current space, for the person in session."""
        if self.profile is None:
            return {}
        visible = self.visible_measurements()
        return {
            indicator: resolve_indicator(
                visible,
                self.profile.crew_id,
                indicator,
                self.environment,
                profile=self.profile,
                as_of=self.journey_time(),
            )
            for indicator in Indicator
        }

    def system_statuses(self) -> dict[System, SystemStatus | None]:
        """The status of each body system; ``None`` for a system with nothing measured."""
        if self.profile is None:
            return {}
        statuses = [r.status for r in self.resolutions().values()]
        return {system: resolve_system(self.profile.crew_id, system, statuses) for system in System}

    def select_system(self, system: System | None) -> None:
        self.selected_system = system

    # --- sharing with the ground team (A10) --------------------------------------------------

    def shareable(self) -> tuple[Indicator, ...]:
        """The indicators with a reading in the current space, in the contract's order."""
        return tuple(
            indicator
            for indicator, resolution in self.resolutions().items()
            if resolution.status.latest is not None
        )

    def toggle_share(self, indicator: Indicator) -> None:
        if self.profile is None:
            return
        if indicator not in self.shareable():
            raise ValueError(f"no reading to share for {indicator.value}")
        self.share_selection ^= {indicator}
        self.share_confirmed = False  # a different selection needs a new confirmation

    def select_attention(self) -> None:
        wanted = {
            indicator
            for indicator, resolution in self.resolutions().items()
            if resolution.status.status in (Status.WATCH, Status.ACT)
        }
        self.share_selection = wanted & set(self.shareable())
        self.share_confirmed = False

    def select_all(self) -> None:
        self.share_selection = set(self.shareable())
        self.share_confirmed = False

    def clear_share(self) -> None:
        self.share_selection = set()
        self.share_confirmed = False

    def set_share_confirmed(self, confirmed: bool) -> None:
        self.share_confirmed = confirmed

    def send_to_ground(self) -> OutboxItem:
        """Pack what was chosen as a FHIR Bundle. ``ConsentRequired`` unless it was confirmed."""
        if self.profile is None:
            raise RuntimeError("nobody is signed in")
        resolutions = self.resolutions()
        latest: dict[Indicator, Measurement] = {}
        for measurement in self.visible_measurements():  # oldest first: the last one wins
            if measurement.environment is self.environment:
                latest[measurement.indicator] = measurement
        chosen = [i for i in Indicator if i in self.share_selection]
        selection = ShareSelection(
            profile=self.profile,
            confirmed=self.share_confirmed,
            confirmed_at=self.journey_time(),
            measurements=tuple(latest[i] for i in chosen if i in latest),
            statuses=tuple(resolutions[i].status for i in chosen),
        )
        bundle = build_bundle(selection)
        problems = check_bundle(bundle)
        if problems:
            raise RuntimeError(f"the package is not valid: {problems}")
        item = OutboxItem(
            crew_id=self.profile.crew_id,
            day_label=self.current_day.label,
            sent_at=selection.confirmed_at,
            arrives_at=selection.confirmed_at + timedelta(minutes=self.ground_delay_minutes),
            bundle=bundle,
            readings=len(selection.measurements),
            states=len(selection.statuses),
            indicators=tuple(chosen),
        )
        item = self._hand_to_ground(item)
        self.outbox.append(item)
        self.clear_share()
        return item

    # --- the link to the ground base (G1) ------------------------------------------------------

    @property
    def ground_linked(self) -> bool:
        return self._ground_link is not None

    def unsent_to_ground(self) -> tuple[OutboxItem, ...]:
        """Packages the ground base has not taken yet (it was unreachable)."""
        return tuple(self._unsent)

    def _hand_to_ground(self, item: OutboxItem) -> OutboxItem:
        """Give ``item`` to the linked ground base. The ground decides when it arrives.

        Unreachable: the package stays queued for a retry and the app keeps working (offline-first).
        Refused: ``RuntimeError`` with the reasons, and nothing is queued.
        """
        if self._ground_link is None:
            return item
        try:
            self._ground_link.sync_clock(self.journey_time())
            arrives = self._ground_link.send(item.bundle)
        except GroundUnreachable:
            self.ground_error = "unreachable"
            self._unsent.append(item)
            return item
        except GroundRejected as error:
            raise RuntimeError(f"the ground base refused the package: {error}") from error
        self.ground_error = None
        return replace(item, arrives_at=arrives)

    def _retry_unsent(self, link: GroundLink) -> None:
        for item in tuple(self._unsent):
            try:
                link.sync_clock(self.journey_time())
                arrives = link.send(item.bundle)
            except GroundUnreachable:
                return
            except GroundRejected:
                self._unsent.remove(item)  # it will never be accepted: do not retry forever
                continue
            self._unsent.remove(item)
            self.outbox[self.outbox.index(item)] = replace(item, arrives_at=arrives)
        if not self._unsent:
            self.ground_error = None

    def _sync_ground(self) -> None:
        if self._ground_link is None:
            return
        try:
            self._ground_link.sync_clock(self.journey_time())
        except GroundUnreachable:
            return
        self._retry_unsent(self._ground_link)

    def own_outbox(self) -> tuple[OutboxItem, ...]:
        """The packages this person sent, up to the simulated "now"."""
        if self.profile is None:
            return ()
        now = self.journey_time()
        return tuple(
            i for i in self.outbox if i.crew_id == self.profile.crew_id and i.sent_at <= now
        )

    def delivered(self) -> tuple[OutboxItem, ...]:
        return tuple(
            i
            for i in self.own_outbox()
            if delivery_state(i, self.journey_time()) is DeliveryState.DELIVERED
        )

    def _deliver(self) -> None:
        """Move what has arrived by the simulated time to the (simulated) ground inbox."""
        now = self.journey_time()
        for item in self.outbox:
            if (
                item not in self.ground_inbox
                and delivery_state(item, now) is DeliveryState.DELIVERED
            ):
                self.ground_inbox.append(item)
