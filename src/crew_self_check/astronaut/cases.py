"""The three demo astronauts as three cases (D-013, D-027). Pure data: texts live in ``i18n``.

Each case is a fictitious crew member of the simulated scenario (``core.scenario``) whose data
stresses a different one of the five hazards of human spaceflight listed by the NASA Human Research
Program (https://www.nasa.gov/hrp/hazards/). The case says what to look at and how the system
approaches it; it is a demonstration of the comparison, never data of a real astronaut.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

HAZARD_URL = "https://www.nasa.gov/hrp/hazards/"


class Hazard(StrEnum):
    """The five hazards of human spaceflight (NASA HRP)."""

    RADIATION = "radiation"
    ISOLATION = "isolation"
    DISTANCE = "distance"
    GRAVITY = "gravity"
    ENVIRONMENT = "environment"


@dataclass(frozen=True, slots=True)
class CaseInfo:
    crew_id: str
    hazard: Hazard

    @property
    def title_key(self) -> str:
        return f"case.{self.crew_id}.title"

    @property
    def story_key(self) -> str:
        return f"case.{self.crew_id}.story"

    @property
    def system_key(self) -> str:
        return f"case.{self.crew_id}.system"


CASES: dict[str, CaseInfo] = {
    "crew-01": CaseInfo("crew-01", Hazard.GRAVITY),
    "crew-02": CaseInfo("crew-02", Hazard.DISTANCE),
    "crew-03": CaseInfo("crew-03", Hazard.ISOLATION),
}


def case_for(crew_id: str) -> CaseInfo | None:
    return CASES.get(crew_id)
