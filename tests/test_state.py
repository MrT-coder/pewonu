"""Part 1: application state, without any UI."""

from crew_self_check.astronaut.access import AccessError, simulated_directory
from crew_self_check.astronaut.state import AppState, Section
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
