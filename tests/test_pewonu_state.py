"""T9/T10: the WOD and the meal log inside the single-screen app (state level)."""

from __future__ import annotations

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.state import AppState, Modal
from crew_self_check.core.nutrition import FOODS


def _state(code: str = "AST-0001") -> AppState:
    state = AppState(simulated_directory())
    state.login(code)
    return state


def test_the_two_new_modals_open_and_close() -> None:
    state = _state()
    state.open_wod()
    assert state.modal is Modal.WOD
    state.open_nutrition()
    assert state.modal is Modal.NUTRITION
    state.close_modal()
    assert state.modal is Modal.NONE


def test_the_plan_rotates_with_the_mission_day() -> None:
    state = _state()
    kinds = []
    for day in range(7):
        state.set_day(day)
        plan = state.wod_plan()
        assert plan is not None
        kinds.append(plan.kind)
    assert len(set(kinds)) == 7


def test_days_in_space_only_count_after_leaving_earth() -> None:
    state = _state()
    state.set_day(0)
    assert state.wod_context().days_in_space == 0
    state.set_day(len(state.scenario.days) - 1)
    assert state.wod_context().days_in_space > 0


def test_the_nutrition_estimate_includes_the_planned_exercise() -> None:
    state = _state()
    plan = state.nutrition_plan()
    wod = state.wod_plan()
    assert plan is not None and wod is not None and wod.energy_kcal is not None
    assert plan.energy_kcal > wod.energy_kcal


def test_meals_are_logged_removed_and_kept_per_day() -> None:
    state = _state()
    state.add_meal(FOODS[0].id)
    state.add_meal(FOODS[1].id)
    assert [m.food_id for m in state.meals()] == [FOODS[0].id, FOODS[1].id]
    state.remove_meal(0)
    assert [m.food_id for m in state.meals()] == [FOODS[1].id]
    state.set_day(state.journey_day + 1)
    assert state.meals() == ()
    state.set_day(state.journey_day - 1)
    assert len(state.meals()) == 1


def test_meals_belong_to_the_person_in_session() -> None:
    state = _state()
    state.add_meal(FOODS[0].id)
    state.logout()
    state.login("AST-0002")
    assert state.meals() == ()


def test_an_unknown_food_is_refused() -> None:
    state = _state()
    with pytest.raises(KeyError):
        state.add_meal("nope")


def test_the_workout_can_be_marked_done_and_undone() -> None:
    state = _state()
    assert not state.wod_done()
    state.toggle_wod_done()
    assert state.wod_done()
    state.toggle_wod_done()
    assert not state.wod_done()
