"""Application state: who is logged in, the language, the section and what was recorded. No UI."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from enum import StrEnum

from crew_self_check.astronaut.access import AccessDirectory, AccessError
from crew_self_check.astronaut.mood import check_level, mood_measurement
from crew_self_check.astronaut.pulse_mission import PulseMission
from crew_self_check.core.contract import CrewProfile, Environment, Indicator, Measurement
from crew_self_check.core.reasons import Language


class Section(StrEnum):
    HOME = "home"
    CHECKIN = "checkin"
    BODY = "body"
    SUMMARY = "summary"


def _utc_now() -> datetime:
    return datetime.now(UTC)


class AppState:
    def __init__(
        self, directory: AccessDirectory, clock: Callable[[], datetime] = _utc_now
    ) -> None:
        self._directory = directory
        self._clock = clock
        self.language = Language.EN  # English is the source language (D-016)
        self.section = Section.HOME
        self.profile: CrewProfile | None = None
        self.code: str | None = None
        self.error: AccessError | None = None
        # Where the astronaut is now. [SUPOSICION] on board until the journey player (A7) sets it.
        self.environment = Environment.SPACECRAFT
        # In memory for now: SQLite behind a storage port comes with A2.
        self.measurements: list[Measurement] = []
        self.pulse: PulseMission | None = None
        self.mood_choice: int | None = None  # the face tapped and not saved yet

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
        return True

    def logout(self) -> None:
        self.profile = None
        self.code = None
        self.error = None
        self.section = Section.HOME
        self.pulse = None  # an unfinished mission is abandoned; what was saved stays
        self.mood_choice = None

    def set_language(self, language: Language) -> None:
        self.language = language

    def go(self, section: Section) -> None:
        if self.logged_in:
            self.section = section

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
        measurement = self.pulse.to_measurement(
            self.profile.crew_id, self.environment, self._clock()
        )
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
            self.profile.crew_id, self.mood_choice, self.environment, self._clock()
        )
        self.measurements.append(measurement)
        self.mood_choice = None
        return measurement

    # --- what this person recorded ---------------------------------------------------------

    def own_measurements(self) -> tuple[Measurement, ...]:
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
