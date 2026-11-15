"""The five NASA HRP hazards as a frame of the app (T1, D-028). Pure logic: texts live in ``i18n``.

Which indicator relates to which hazard is **our reading** of the HRP pages, not an official list
([SUPOSICION], said on screen). Radiation is not measured by this prototype (it needs a dosimeter,
see ``research/12``); distance is about the communication delay, not an indicator. Nothing here
computes a state: the colors come from the engine through ``AppState.resolutions``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from crew_self_check.astronaut.cases import Hazard
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Environment, Indicator, Status

_SEVERITY = {Status.OK: 0, Status.INSUFFICIENT_DATA: 1, Status.WATCH: 2, Status.ACT: 3}


class HazardMode(StrEnum):
    INDICATORS = "indicators"  # the hazard touches indicators the astronaut records
    NOT_MEASURED = "not_measured"  # this prototype has no instrument for it
    COMMUNICATION = "communication"  # about the delay to the ground, not a body indicator


HAZARD_INDICATORS: dict[Hazard, tuple[Indicator, ...]] = {
    Hazard.RADIATION: (),
    Hazard.ISOLATION: (Indicator.SLEEP_HOURS, Indicator.MOOD),
    Hazard.DISTANCE: (),
    Hazard.GRAVITY: (
        Indicator.ORTHOSTATIC_HR_DELTA,
        Indicator.VESTIBULAR_SYMPTOMS,
        Indicator.TANDEM_WALK_OK,
        Indicator.RESTING_HR,
        Indicator.SYSTOLIC_BP,
        Indicator.DIASTOLIC_BP,
    ),
    Hazard.ENVIRONMENT: (Indicator.SPO2, Indicator.BODY_TEMP),
}

_MODES = {
    Hazard.RADIATION: HazardMode.NOT_MEASURED,
    Hazard.DISTANCE: HazardMode.COMMUNICATION,
}


@dataclass(frozen=True, slots=True)
class HazardIndicator:
    indicator: Indicator
    status: Status
    latest: float | None
    unit: str


@dataclass(frozen=True, slots=True)
class HazardCard:
    hazard: Hazard
    mode: HazardMode
    here_key: str  # what the hazard means in the place the person is in now
    indicators: tuple[HazardIndicator, ...]
    worst: Status | None  # ``None`` when the hazard has no indicator
    delay_minutes: int | None  # only for the communication hazard


def here_key(hazard: Hazard, environment: Environment) -> str:
    return f"hazard.{hazard.value}.here.{environment.value}"


def build_hazards(state: AppState) -> tuple[HazardCard, ...]:
    if state.profile is None:
        return ()
    resolutions = state.resolutions()
    cards: list[HazardCard] = []
    for hazard in Hazard:
        indicators = tuple(
            HazardIndicator(
                indicator,
                resolutions[indicator].status.status,
                resolutions[indicator].status.latest,
                _unit(state, indicator),
            )
            for indicator in HAZARD_INDICATORS[hazard]
        )
        worst = max((i.status for i in indicators), key=_SEVERITY.__getitem__, default=None)
        cards.append(
            HazardCard(
                hazard=hazard,
                mode=_MODES.get(hazard, HazardMode.INDICATORS),
                here_key=here_key(hazard, state.environment),
                indicators=indicators,
                worst=worst,
                delay_minutes=state.ground_delay_minutes if hazard is Hazard.DISTANCE else None,
            )
        )
    return tuple(cards)


def _unit(state: AppState, indicator: Indicator) -> str:
    for measurement in reversed(state.visible_measurements()):
        if measurement.indicator is indicator:
            return measurement.unit
    return ""
