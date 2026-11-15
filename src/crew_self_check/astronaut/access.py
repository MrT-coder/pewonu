"""Access by unique astronaut code (D-020).

The code opens one fictitious crew profile on this computer. It is a way to pick *whose* data the
app shows, not a security boundary: there is no password and no real person's data here (AGENTS.md,
section 8). Pure logic: no UI, no files, no network.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from crew_self_check.core.contract import CrewProfile
from crew_self_check.core.scenario import CREW

_CODE = re.compile(r"AST-[0-9]{4}")


class AccessError(StrEnum):
    INVALID_FORMAT = "invalid_format"
    UNKNOWN_CODE = "unknown_code"


@dataclass(frozen=True, slots=True)
class LoginResult:
    profile: CrewProfile | None
    code: str | None  # the normalised code, only on success: the typed text is never kept
    error: AccessError | None


def normalize_code(typed: str) -> str | None:
    """``AST-0000`` form of what was typed (trimmed, any case), or ``None`` if it is malformed."""
    candidate = typed.strip().upper()
    return candidate if _CODE.fullmatch(candidate) else None


class AccessDirectory:
    def __init__(self, profiles_by_code: Mapping[str, CrewProfile]) -> None:
        directory: dict[str, CrewProfile] = {}
        for typed, profile in profiles_by_code.items():
            code = normalize_code(typed)
            if code is None:
                raise ValueError(f"invalid code format: {typed!r}")
            if code in directory:
                raise ValueError(f"duplicate code: {code}")
            directory[code] = profile
        self._profiles = directory

    def codes(self) -> tuple[str, ...]:
        return tuple(sorted(self._profiles))

    def entries(self) -> tuple[tuple[str, CrewProfile], ...]:
        """Every code with the profile it opens, in code order (for the demo list)."""
        return tuple((code, self._profiles[code]) for code in self.codes())

    def login(self, typed: str) -> LoginResult:
        code = normalize_code(typed)
        if code is None:
            return LoginResult(None, None, AccessError.INVALID_FORMAT)
        profile = self._profiles.get(code)
        if profile is None:
            return LoginResult(None, None, AccessError.UNKNOWN_CODE)
        return LoginResult(profile, code, None)


def simulated_directory() -> AccessDirectory:
    """One code per fictitious crew member of the simulated scenario (C5)."""
    return AccessDirectory({f"AST-{i:04d}": profile for i, profile in enumerate(CREW, start=1)})
