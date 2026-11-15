"""The pulse result says what the count means and what to do next, not only a badge (A5)."""

from __future__ import annotations

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.pulse_guidance import outside_band, pulse_guidance
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Escalation, Status
from crew_self_check.core.reasons import Language
from crew_self_check.core.status import escalation_for


def _state(code_index: int = 0) -> AppState:
    state = AppState(simulated_directory())
    state.login(state.demo_codes()[code_index])
    state.start_pulse()
    assert state.pulse is not None
    for _ in range(3):
        state.pulse.complete_station()
    return state


def _count(state: AppState, bpm: int) -> None:
    assert state.pulse is not None
    state.pulse.set_interval(60)
    state.pulse.submit_count(bpm)


@pytest.mark.parametrize("status", [*Status, None])
@pytest.mark.parametrize("outside", [False, True])
def test_every_guidance_text_exists_in_both_languages(status: Status | None, outside: bool) -> None:
    for key in pulse_guidance(status, outside).steps:
        for language in Language:
            assert translate(key, language).strip()


@pytest.mark.parametrize("status", [Status.WATCH, Status.ACT])
def test_outside_the_range_says_to_rest_recount_and_who_to_tell(status: Status) -> None:
    guidance = pulse_guidance(status)
    assert "pulse.todo.rest" in guidance.steps  # MedlinePlus: rest at least 10 minutes
    assert "pulse.todo.recount" in guidance.steps
    assert "pulse.todo.uneven" in guidance.steps
    assert guidance.escalation is escalation_for(status)


def test_inside_the_range_does_not_send_anyone_to_the_doctor() -> None:
    guidance = pulse_guidance(Status.OK)
    assert guidance.escalation is Escalation.SELF_CARE
    assert "pulse.todo.recount" not in guidance.steps
    assert "pulse.todo.same_time" in guidance.steps


def test_without_enough_data_it_says_to_keep_measuring() -> None:
    for status in (Status.INSUFFICIENT_DATA, None):
        guidance = pulse_guidance(status)
        assert "pulse.todo.keep_measuring" in guidance.steps
        assert guidance.escalation is Escalation.SELF_CARE


def test_the_guidance_never_gives_a_dose_or_a_clinical_step() -> None:
    for status in (*Status, None):
        for key in pulse_guidance(status, True).steps + pulse_guidance(status).steps:
            text = translate(key, Language.EN).lower()
            assert "mg" not in text
            assert "take a" not in text
            assert "medicat" not in text


def test_the_preview_compares_the_count_with_the_persons_baseline_before_saving() -> None:
    state = _state()
    _count(state, 62)
    resolution = state.preview_pulse()
    assert resolution is not None
    assert resolution.status.status is Status.OK
    assert resolution.status.latest == 62
    assert state.own_measurements() == ()  # nothing was saved


def test_one_count_outside_the_band_is_not_called_fine_and_not_called_a_trend() -> None:
    """The engine needs several readings in a row for amber (D-013): one count is a recount."""
    state = _state()
    _count(state, 110)
    resolution = state.preview_pulse()
    assert resolution is not None
    assert resolution.status.status is Status.OK  # not sustained yet
    assert outside_band(resolution)
    steps = pulse_guidance(resolution.status.status, outside_band(resolution)).steps
    assert steps[0] == "pulse.todo.single"
    assert "pulse.todo.rest" in steps
    assert "pulse.todo.recount" in steps


def test_a_count_inside_the_band_is_not_outside_it() -> None:
    state = _state()
    _count(state, 61)
    resolution = state.preview_pulse()
    assert resolution is not None
    assert not outside_band(resolution)


def test_without_a_baseline_nothing_is_outside_it() -> None:
    state = _state(1)
    _count(state, 70)
    resolution = state.preview_pulse()
    assert resolution is not None
    assert not outside_band(resolution)


def test_a_person_without_history_is_compared_with_the_labelled_population_reference() -> None:
    state = _state(1)
    _count(state, 108)
    resolution = state.preview_pulse()
    assert resolution is not None
    assert resolution.status.reference.value == "population"
    assert resolution.status.status is Status.ACT


def test_there_is_no_preview_before_a_valid_count() -> None:
    state = _state()
    assert state.preview_pulse() is None
    _count(state, 10)  # implausible: the app asks for a recount
    assert state.preview_pulse() is None
