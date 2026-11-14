"""Part 1: application state, without any UI."""

from datetime import UTC, datetime

import pytest

from crew_self_check.astronaut.access import AccessError, simulated_directory
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.core.contract import Environment
from crew_self_check.core.reasons import Language


def make() -> AppState:
    return AppState(simulated_directory())


def test_it_starts_logged_out_in_english_on_the_home_section() -> None:
    state = make()
    assert state.profile is None
    assert state.code is None
    assert state.language is Language.EN
    assert state.section is Section.HOME
    assert state.error is None
    assert not state.logged_in


def test_a_good_code_logs_in_and_clears_the_error() -> None:
    state = make()
    assert state.login("AST-9999") is False
    assert state.error is AccessError.UNKNOWN_CODE
    assert state.login(" ast-0001 ") is True
    assert state.logged_in
    assert state.error is None
    assert state.code == "AST-0001"
    assert state.profile is not None
    assert state.profile.crew_id == "crew-01"


def test_a_bad_code_leaves_the_state_logged_out() -> None:
    state = make()
    assert state.login("nope") is False
    assert state.error is AccessError.INVALID_FORMAT
    assert not state.logged_in
    for _ in range(5):  # no lockout: a typo must never trap the astronaut
        state.login("AST-9999")
    assert state.login("AST-0002") is True


def test_a_failed_login_does_not_log_out_a_session_in_progress() -> None:
    state = make()
    state.login("AST-0001")
    assert state.login("AST-9999") is False
    assert state.code == "AST-0001"


def test_logout_clears_the_session_and_goes_home_but_keeps_the_language() -> None:
    state = make()
    state.set_language(Language.ES)
    state.login("AST-0001")
    state.go(Section.BODY)
    state.logout()
    assert not state.logged_in
    assert state.section is Section.HOME
    assert state.language is Language.ES


def test_navigation_only_works_when_logged_in() -> None:
    state = make()
    state.go(Section.BODY)
    assert state.section is Section.HOME
    state.login("AST-0001")
    state.go(Section.BODY)
    assert state.section is Section.BODY


def test_the_language_can_be_switched_at_any_time() -> None:
    state = make()
    state.set_language(Language.ES)
    assert state.language is Language.ES
    state.login("AST-0001")
    state.set_language(Language.EN)
    assert state.language is Language.EN
    assert state.logged_in


def test_the_sections_are_the_four_parts() -> None:
    assert [s.value for s in Section] == ["home", "checkin", "body", "summary"]


# --- the pulse mission and what it records ------------------------------------------------------

FIXED = datetime(2026, 11, 14, 21, 40, tzinfo=UTC)


def make_with_clock() -> AppState:
    return AppState(simulated_directory(), clock=lambda: FIXED)


def finish_a_pulse(state: AppState, taps: int = 35) -> None:
    assert state.pulse is not None
    for _ in range(3):
        state.pulse.complete_station()
    state.pulse.start_count(0.0)
    for i in range(taps):
        state.pulse.tap(i * 0.8)
    state.pulse.finish(30.0)


def test_a_pulse_mission_needs_a_session() -> None:
    state = make_with_clock()
    state.start_pulse()
    assert state.pulse is None
    state.login("AST-0001")
    state.start_pulse()
    assert state.pulse is not None


def test_saving_the_pulse_records_a_measurement_for_the_person_in_the_current_environment() -> None:
    state = make_with_clock()
    state.login("AST-0001")
    state.start_pulse()
    finish_a_pulse(state)
    saved = state.save_pulse()
    assert saved.crew_id == "crew-01"
    assert saved.value == 70
    assert saved.timestamp == FIXED
    assert saved.environment is state.environment is Environment.SPACECRAFT
    assert state.pulse is None
    assert state.own_measurements() == (saved,)
    assert state.last_pulse() == saved


def test_the_pulse_follows_the_environment_of_the_journey() -> None:
    state = make_with_clock()
    state.login("AST-0001")
    state.environment = Environment.PLANET
    state.start_pulse()
    finish_a_pulse(state)
    assert state.save_pulse().environment is Environment.PLANET


def test_each_person_only_sees_their_own_readings() -> None:
    state = make_with_clock()
    state.login("AST-0001")
    state.start_pulse()
    finish_a_pulse(state)
    state.save_pulse()
    state.logout()
    state.login("AST-0002")
    assert state.own_measurements() == ()
    assert state.last_pulse() is None
    state.logout()
    state.login("AST-0001")
    assert state.last_pulse() is not None


def test_logging_out_abandons_an_unfinished_mission() -> None:
    state = make_with_clock()
    state.login("AST-0001")
    state.start_pulse()
    state.logout()
    assert state.pulse is None


def test_the_mission_can_be_left() -> None:
    state = make_with_clock()
    state.login("AST-0001")
    state.start_pulse()
    state.cancel_pulse()
    assert state.pulse is None
    assert state.own_measurements() == ()


def test_saving_without_a_finished_mission_is_an_error() -> None:
    state = make_with_clock()
    state.login("AST-0001")
    with pytest.raises(RuntimeError, match="pulse"):
        state.save_pulse()
    state.start_pulse()
    with pytest.raises(RuntimeError, match="result"):
        state.save_pulse()
