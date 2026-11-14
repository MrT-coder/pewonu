"""Application state: session, language, section, the journey and what was recorded. No UI.

The demo runs on **simulated time**: the journey (C5, D-013) moves day by day from Earth through
the spacecraft to the planet, and what the astronaut records is stamped with that day. A fixed
``clock`` can be injected (tests do); by default the clock is the journey itself.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from enum import StrEnum

from crew_self_check.astronaut.access import AccessDirectory, AccessError
from crew_self_check.astronaut.mood import check_level, mood_measurement
from crew_self_check.astronaut.pulse_mission import PulseMission
from crew_self_check.core.contract import (
    CrewProfile,
    Indicator,
    Measurement,
    System,
    SystemStatus,
)
from crew_self_check.core.reasons import Language
from crew_self_check.core.scenario import Scenario, ScenarioDay, generate_scenario
from crew_self_check.core.status import IndicatorResolution, resolve_indicator, resolve_system

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
    ) -> None:
        self._directory = directory
        self._clock = clock
        self.scenario = scenario or generate_scenario()
        self.language = Language.EN  # English is the source language (D-016)
        self.section = Section.HOME
        self.profile: CrewProfile | None = None
        self.code: str | None = None
        self.error: AccessError | None = None
        self.journey_day = next((d.index for d in self.scenario.days if d.label == START_LABEL), 0)
        self.environment = self.current_day.environment
        # In memory for now: SQLite behind a storage port comes with A2.
        self.measurements: list[Measurement] = []
        self.pulse: PulseMission | None = None
        self.mood_choice: int | None = None  # the face tapped and not saved yet
        self.selected_system: System | None = None

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
        return True

    def logout(self) -> None:
        self.profile = None
        self.code = None
        self.error = None
        self.section = Section.HOME
        self.pulse = None  # an unfinished mission is abandoned; what was saved stays
        self.mood_choice = None
        self.selected_system = None

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
        self.measurements.append(measurement)
        self.pulse = None
        return measurement

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
        self.measurements.append(measurement)
        self.mood_choice = None
        return measurement

    # --- what this person recorded ---------------------------------------------------------

    def own_measurements(self) -> tuple[Measurement, ...]:
        """What the astronaut recorded in the app (not the simulated history)."""
        if self.profile is None:
            return ()
        return tuple(m for m in self.measurements if m.crew_id == self.profile.crew_id)

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
        pool = [*self.scenario.measurements, *self.measurements]
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
