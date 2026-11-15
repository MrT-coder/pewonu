"""The three demo astronauts are three different cases, each tied to a NASA HRP hazard."""

from __future__ import annotations

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.cases import CASES, HAZARD_URL, Hazard, case_for
from crew_self_check.astronaut.i18n import translate
from crew_self_check.core.reasons import Language
from crew_self_check.core.scenario import CREW


def test_there_is_one_case_per_crew_member_and_one_code_each() -> None:
    assert set(CASES) == {p.crew_id for p in CREW}
    assert len(simulated_directory().codes()) == len(CASES)


def test_the_three_cases_stress_three_different_hazards() -> None:
    assert len({case.hazard for case in CASES.values()}) == 3


def test_the_hazards_are_the_five_of_the_nasa_hrp_page() -> None:
    assert {h.value for h in Hazard} == {
        "radiation",
        "isolation",
        "distance",
        "gravity",
        "environment",
    }
    assert HAZARD_URL == "https://www.nasa.gov/hrp/hazards/"


@pytest.mark.parametrize("crew_id", sorted(CASES))
def test_every_case_text_exists_in_both_languages(crew_id: str) -> None:
    case = case_for(crew_id)
    assert case is not None
    keys = [case.title_key, case.story_key, case.system_key, f"hazard.{case.hazard.value}"]
    for key in keys:
        for language in Language:
            assert translate(key, language).strip()


@pytest.mark.parametrize("hazard", list(Hazard))
def test_every_hazard_has_a_name_and_a_description_in_both_languages(hazard: Hazard) -> None:
    for language in Language:
        assert translate(f"hazard.{hazard.value}", language).strip()
        assert translate(f"hazard.{hazard.value}.what", language).strip()


def test_an_unknown_crew_member_has_no_case() -> None:
    assert case_for("crew-99") is None


def test_the_case_texts_say_it_is_simulated_and_never_diagnose() -> None:
    for case in CASES.values():
        text = translate(case.story_key, Language.EN).lower()
        assert "diagnos" not in text
        assert "disease" not in text


def test_each_demo_code_opens_its_own_case() -> None:
    from crew_self_check.astronaut.state import AppState

    state = AppState(simulated_directory())
    pairs = state.demo_cases()
    assert [code for code, _ in pairs] == list(state.demo_codes())
    assert [crew for _, crew in pairs] == ["crew-01", "crew-02", "crew-03"]
    for code, crew_id in pairs:
        assert state.login(code)
        assert state.profile is not None and state.profile.crew_id == crew_id
        assert case_for(crew_id) is not None
