"""Application state: who is logged in, the language, the section and what was recorded. No UI."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from enum import StrEnum

from crew_self_check.astronaut.access import AccessDirectory, AccessError
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
        return True

    def logout(self) -> None:
        self.profile = None
        self.code = None
        self.error = None
        self.section = Section.HOME
        self.pulse = None  # an unfinished mission is abandoned; what was saved stays

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

    # --- what this person recorded ---------------------------------------------------------

    def own_measurements(self) -> tuple[Measurement, ...]:
        if self.profile is None:
            return ()
        return tuple(m for m in self.measurements if m.crew_id == self.profile.crew_id)

    def last_pulse(self) -> Measurement | None:
        pulses = [m for m in self.own_measurements() if m.indicator is Indicator.RESTING_HR]
        return pulses[-1] if pulses else None
