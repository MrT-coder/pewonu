"""T1: the five NASA HRP hazards as a frame of the app, tied to the person's own indicators."""

from __future__ import annotations

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.cases import Hazard
from crew_self_check.astronaut.hazards import (
    HAZARD_INDICATORS,
    HazardMode,
    build_hazards,
    here_key,
)
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Environment, Indicator, Status
from crew_self_check.core.reasons import Language


def _state(code: str = "AST-0001", day: str = "E-1") -> AppState:
    state = AppState(simulated_directory())
    state.login(code)
    state.set_day(next(d.index for d in state.scenario.days if d.label == day))
    return state


def test_nothing_without_a_session() -> None:
    assert build_hazards(AppState(simulated_directory())) == ()


def test_there_is_one_card_per_hazard_in_order() -> None:
    cards = build_hazards(_state())
    assert [c.hazard for c in cards] == list(Hazard)


def test_radiation_is_honestly_not_measured_here() -> None:
    radiation = next(c for c in build_hazards(_state()) if c.hazard is Hazard.RADIATION)
    assert radiation.mode is HazardMode.NOT_MEASURED
    assert radiation.indicators == ()


def test_distance_is_about_the_communication_delay_not_an_indicator() -> None:
    state = _state()
    state.ground_delay_minutes = 9
    distance = next(c for c in build_hazards(state) if c.hazard is Hazard.DISTANCE)
    assert distance.mode is HazardMode.COMMUNICATION
    assert distance.delay_minutes == 9


def test_every_mapped_indicator_exists_and_the_map_is_documented_as_ours() -> None:
    mapped = [i for indicators in HAZARD_INDICATORS.values() for i in indicators]
    assert set(mapped) <= set(Indicator)
    assert "not an official list" in translate("hazards.assumption", Language.EN).lower()
    assert "no es una lista oficial" in translate("hazards.assumption", Language.ES).lower()


@pytest.mark.parametrize("hazard", list(Hazard))
@pytest.mark.parametrize("environment", list(Environment))
@pytest.mark.parametrize("language", list(Language))
def test_what_the_hazard_means_in_each_place_exists_in_both_languages(
    hazard: Hazard, environment: Environment, language: Language
) -> None:
    assert translate(here_key(hazard, environment), language).strip()


def test_the_isolation_case_shows_up_in_the_isolation_hazard() -> None:
    cards = build_hazards(_state("AST-0003", "T+6"))
    isolation = next(c for c in cards if c.hazard is Hazard.ISOLATION)
    assert isolation.worst is Status.WATCH
    assert {i.indicator for i in isolation.indicators} == {Indicator.SLEEP_HOURS, Indicator.MOOD}
    flagged = {i.indicator for i in isolation.indicators if i.status is Status.WATCH}
    assert flagged == {Indicator.SLEEP_HOURS, Indicator.MOOD}


def test_the_arrival_case_shows_up_in_the_gravity_hazard() -> None:
    cards = build_hazards(_state("AST-0001", "R+2"))
    gravity = next(c for c in cards if c.hazard is Hazard.GRAVITY)
    assert gravity.worst in (Status.WATCH, Status.ACT)


def test_a_hazard_that_stays_in_range_is_not_flagged() -> None:
    cards = build_hazards(_state("AST-0003", "T+6"))
    environment = next(c for c in cards if c.hazard is Hazard.ENVIRONMENT)
    assert environment.worst in (Status.OK, Status.INSUFFICIENT_DATA)


def test_the_card_says_which_place_it_is_describing() -> None:
    cards = build_hazards(_state(day="T+2"))
    assert all(c.here_key == here_key(c.hazard, Environment.SPACECRAFT) for c in cards)
