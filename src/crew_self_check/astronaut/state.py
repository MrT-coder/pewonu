"""Application state: session, language, section, the journey and what was recorded. No UI.

The demo runs on **simulated time**: the journey (C5, D-013) moves day by day from Earth through
the spacecraft to the planet, and what the astronaut records is stamped with that day. A fixed
``clock`` can be injected (tests do); by default the clock is the journey itself.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass, replace
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
from crew_self_check.astronaut.voice_capture import (
    VOICE_PROMPTS,
    SyntheticVoiceRecorder,
    VoiceRecorder,
)
from crew_self_check.core.contract import (
    CrewProfile,
    Indicator,
    Measurement,
    Status,
    System,
    SystemStatus,
    VoiceFeatures,
)
from crew_self_check.core.fhir import ShareSelection, build_bundle, check_bundle
from crew_self_check.core.reasons import Language
from crew_self_check.core.scenario import Scenario, ScenarioDay, generate_scenario
from crew_self_check.core.status import IndicatorResolution, resolve_indicator, resolve_system
from crew_self_check.core.storage import (
    InMemoryMeasurementStore,
    InMemoryVoiceStore,
    MeasurementStore,
    VoiceStore,
)
from crew_self_check.core.voice_analysis import VoiceAnalysis, analyze
from crew_self_check.core.voice_baseline import VoiceComparison, compare
from crew_self_check.core.voice_scenario import generate_voice_notes

START_LABEL = "E-1"  # the journey opens on the last day on Earth, with a full history behind it
_MIDDAY = timedelta(hours=12)


class Section(StrEnum):
    HOME = "home"
    CHECKIN = "checkin"
    BODY = "body"
    SUMMARY = "summary"
    DATA = "data"
    HAZARDS = "hazards"


class Modal(StrEnum):
    """What is open on top of the single screen (UX v2)."""

    NONE = "none"
    ZONE = "zone"
    PULSE = "pulse"
    MOOD = "mood"
    SHARE = "share"


class VoiceStage(StrEnum):
    IDLE = "idle"
    PROMPT = "prompt"
    RECORDING = "recording"
    RESULT = "result"


@dataclass(frozen=True, slots=True)
class VoiceResult:
    """What came out of one voice note. It holds numbers only: the audio is gone."""

    analysis: VoiceAnalysis
    comparison: VoiceComparison | None
    saved: bool
    shared: bool = False  # sent to the ground base (standing consent, shown on screen)


class AppState:
    def __init__(
        self,
        directory: AccessDirectory,
        clock: Callable[[], datetime] | None = None,
        scenario: Scenario | None = None,
        store: MeasurementStore | None = None,
        ground_link: GroundLink | None = None,
        voice_recorder: VoiceRecorder | None = None,
        voice_store: VoiceStore | None = None,
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
        # The voice log (T2): numbers only, the audio lives in the recorder until it stops.
        self._voice_recorder = voice_recorder
        self._voice_store: VoiceStore = voice_store or InMemoryVoiceStore()
        self._voice_seed = generate_voice_notes(self.scenario)
        self._voice_rng = random.Random()
        self.voice_stage = VoiceStage.IDLE
        self.voice_prompt: str = VOICE_PROMPTS[0]
        self.voice_tick = 0  # lets only the newest recording screen update the meter
        # The single screen opens everything in modals; one at a time (UX v2).
        self.modal = Modal.NONE
        self.pulse_tab = "data"  # "data" (collected) or "hand" (measure by hand)
        self.bubble_offset: tuple[int, int] = (28, 28)  # right and bottom, in pixels
        self.voice_result: VoiceResult | None = None

    @property
    def logged_in(self) -> bool:
        return self.profile is not None

    def demo_codes(self) -> tuple[str, ...]:
        return self._directory.codes()

    def demo_cases(self) -> tuple[tuple[str, str], ...]:
        """Each demo code with the ``crew_id`` it opens."""
        return tuple((code, profile.crew_id) for code, profile in self._directory.entries())

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

    # --- modals (UX v2) -------------------------------------------------------------------

    def _open(self, kind: Modal) -> None:
        if self.profile is None:
            raise RuntimeError("sign in first")
        self.close_modal()
        self.modal = kind

    def open_zone(self, system: System) -> None:
        self._open(Modal.ZONE)
        self.selected_system = system

    def open_pulse(self) -> None:
        self._open(Modal.PULSE)
        self.pulse_tab = "data"

    def pulse_measure(self) -> None:
        """Switch the pulse modal to measuring by hand (starts the guided mission)."""
        self.pulse_tab = "hand"
        self.start_pulse()

    def pulse_data(self) -> None:
        """Back to the collected data; an unfinished mission is abandoned."""
        self.pulse_tab = "data"
        self.pulse = None

    def open_mood(self) -> None:
        self._open(Modal.MOOD)
        self.mood_choice = None

    def save_mood_and_continue(self) -> Measurement:
        """Save the face and go on to the voice log in the same modal."""
        measurement = self.save_mood()
        self.new_voice_prompt()
        self.open_voice()
        return measurement

    def open_share(self) -> None:
        self._open(Modal.SHARE)

    def close_modal(self) -> None:
        """Close whatever is open. A recording or an unfinished pulse is abandoned."""
        if self.voice_stage is not VoiceStage.IDLE:
            self.cancel_voice()
        if self.pulse is not None:
            self.pulse = None
        self.mood_choice = None
        self.selected_system = None
        self.pulse_tab = "data"
        self.modal = Modal.NONE

    def move_bubble(self, dx: float, dy: float) -> None:
        """Drag the mood bubble: it hangs from the right and bottom edges."""
        right, bottom = self.bubble_offset
        self.bubble_offset = (max(8, round(right - dx)), max(8, round(bottom - dy)))

    def logout(self) -> None:
        self.close_modal()
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
        self.pulse_tab = "data"  # back to the collected data, now with this reading
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

    # --- the voice log (T2, D-028) ----------------------------------------------------------

    def set_voice_rng(self, rng: random.Random) -> None:
        self._voice_rng = rng

    def voice_available(self) -> bool:
        return self._voice_recorder is not None and self._voice_recorder.available()

    def voice_synthetic(self) -> bool:
        return self._voice_recorder is not None and self._voice_recorder.synthetic

    def voice_level(self) -> float:
        return self._voice_recorder.level() if self._voice_recorder is not None else 0.0

    def new_voice_prompt(self) -> str:
        """A random open question, never the same one twice in a row."""
        choices = [key for key in VOICE_PROMPTS if key != self.voice_prompt]
        self.voice_prompt = self._voice_rng.choice(choices)
        return self.voice_prompt

    def open_voice(self) -> None:
        """Show a question: the first step of a voice note."""
        if self.profile is None:
            raise RuntimeError("sign in first")
        self.voice_stage = VoiceStage.PROMPT
        self.voice_result = None

    def use_synthetic_voice(self, kind: str = "usual") -> None:
        """No microphone: use a generated, labelled sample so the flow can be shown."""
        self._voice_recorder = SyntheticVoiceRecorder(kind=kind)

    def synthetic_kind(self) -> str | None:
        recorder = self._voice_recorder
        return recorder.kind if isinstance(recorder, SyntheticVoiceRecorder) else None

    def start_voice(self) -> None:
        if self.profile is None or self._voice_recorder is None:
            raise RuntimeError("a voice note needs a signed-in person and a recorder")
        self._voice_recorder.start()
        self.voice_stage = VoiceStage.RECORDING
        self.voice_result = None

    def stop_voice(self) -> VoiceResult:
        """Stop, analyse, keep the numbers if the note is usable, and throw the audio away."""
        if self.profile is None or self._voice_recorder is None:
            raise RuntimeError("there is no voice note to stop")
        samples, rate = self._voice_recorder.stop()
        analysis = analyze(samples, rate)
        del samples  # the only copy of the audio held by the app
        comparison: VoiceComparison | None = None
        saved = False
        shared = False
        if analysis.quality_ok:
            note = VoiceFeatures(
                crew_id=self.profile.crew_id,
                timestamp=self._now(),
                environment=self.environment,
                features=analysis.features,
                mood_survey_score=self._latest_mood(),
            )
            comparison = compare(self.voice_history(), note)
            self._voice_store.add(note)
            saved = True
            shared = self._share_voice(note, comparison)
        self.voice_result = VoiceResult(analysis, comparison, saved, shared)
        self.voice_stage = VoiceStage.RESULT
        return self.voice_result

    def _share_voice(self, note: VoiceFeatures, comparison: VoiceComparison) -> bool:
        """Send the numbers to the ground base (the crew agreed to this when joining).

        Only numbers travel, never audio or words (D-028). Without a link nothing is sent.
        """
        if self.profile is None or self._ground_link is None:
            return False
        selection = ShareSelection(
            profile=self.profile,
            confirmed=True,  # standing consent, shown on the voice screen
            confirmed_at=self.journey_time(),
            measurements=(),
            statuses=(),
            voice=((note, comparison),),
        )
        bundle = build_bundle(selection)
        item = OutboxItem(
            crew_id=self.profile.crew_id,
            day_label=self.current_day.label,
            sent_at=selection.confirmed_at,
            arrives_at=selection.confirmed_at + timedelta(minutes=self.ground_delay_minutes),
            bundle=bundle,
            readings=0,
            states=0,
            indicators=(),
            voices=1,
        )
        item = self._hand_to_ground(item)
        self.outbox.append(item)
        return item not in self._unsent

    def cancel_voice(self) -> None:
        """Leave the voice screen: a recording in progress is stopped and discarded."""
        if self.voice_stage is VoiceStage.RECORDING and self._voice_recorder is not None:
            self._voice_recorder.stop()
        self.voice_stage = VoiceStage.IDLE
        self.voice_result = None
        if self.modal is Modal.MOOD:  # leaving the voice step leaves the whole bubble
            self.modal = Modal.NONE

    def voice_history_own(self) -> tuple[VoiceFeatures, ...]:
        """The notes this person recorded in the app (not the simulated history)."""
        if self.profile is None:
            return ()
        return self._voice_store.for_crew(self.profile.crew_id)

    def voice_history(self) -> tuple[VoiceFeatures, ...]:
        """Simulated notes up to the end of today plus the person's own, oldest first."""
        if self.profile is None:
            return ()
        cutoff = self.current_day.timestamp + timedelta(days=1)
        crew_id = self.profile.crew_id
        seeded = [n for n in self._voice_seed if n.crew_id == crew_id and n.timestamp < cutoff]
        own = [n for n in self.voice_history_own() if n.timestamp < cutoff]
        return tuple(sorted([*seeded, *own], key=lambda n: n.timestamp))

    def _latest_mood(self) -> int:
        moods = [m for m in self.visible_measurements() if m.indicator is Indicator.MOOD]
        return int(moods[-1].value) if moods else 0  # 0: no survey answered yet

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
