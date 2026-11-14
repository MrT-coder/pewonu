"""Application state: who is logged in, the language and the current section. No UI here."""

from __future__ import annotations

from enum import StrEnum

from crew_self_check.astronaut.access import AccessDirectory, AccessError
from crew_self_check.core.contract import CrewProfile
from crew_self_check.core.reasons import Language


class Section(StrEnum):
    HOME = "home"
    CHECKIN = "checkin"
    BODY = "body"
    SUMMARY = "summary"


class AppState:
    def __init__(self, directory: AccessDirectory) -> None:
        self._directory = directory
        self.language = Language.EN  # English is the source language (D-016)
        self.section = Section.HOME
        self.profile: CrewProfile | None = None
        self.code: str | None = None
        self.error: AccessError | None = None

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
        return True

    def logout(self) -> None:
        self.profile = None
        self.code = None
        self.error = None
        self.section = Section.HOME

    def set_language(self, language: Language) -> None:
        self.language = language

    def go(self, section: Section) -> None:
        if self.logged_in:
            self.section = section
