"""Part 1: access by unique astronaut code (D-020). Pure logic, no UI."""

import pytest

from crew_self_check.astronaut.access import (
    AccessDirectory,
    AccessError,
    normalize_code,
    simulated_directory,
)
from crew_self_check.core.scenario import CREW


@pytest.mark.parametrize(
    ("typed", "expected"),
    [
        ("AST-0001", "AST-0001"),
        ("  ast-0001  ", "AST-0001"),
        ("Ast-0002", "AST-0002"),
        ("AST-0001\n", "AST-0001"),
    ],
)
def test_the_code_is_trimmed_and_case_insensitive(typed: str, expected: str) -> None:
    assert normalize_code(typed) == expected


@pytest.mark.parametrize(
    "typed",
    ["", "   ", "AST-1", "AST-00001", "ABC-0001", "AST0001", "AST-00A1", "0001", "AST- 0001"],
)
def test_a_malformed_code_has_no_normal_form(typed: str) -> None:
    assert normalize_code(typed) is None


def test_a_known_code_opens_that_crew_profile() -> None:
    directory = simulated_directory()
    first = directory.login("AST-0001")
    assert first.error is None
    assert first.profile is not None
    assert first.profile.crew_id == "crew-01"
    assert first.code == "AST-0001"
    second = directory.login(" ast-0002 ")
    assert second.profile is not None
    assert second.profile.crew_id == "crew-02"


def test_an_unknown_code_is_refused_without_a_profile() -> None:
    result = simulated_directory().login("AST-9999")
    assert result.profile is None
    assert result.error is AccessError.UNKNOWN_CODE


@pytest.mark.parametrize("typed", ["", "hello", "AST-1"])
def test_a_malformed_code_is_refused_as_such(typed: str) -> None:
    result = simulated_directory().login(typed)
    assert result.profile is None
    assert result.error is AccessError.INVALID_FORMAT


def test_every_simulated_crew_member_has_exactly_one_code() -> None:
    directory = simulated_directory()
    codes = directory.codes()
    assert len(codes) == len(set(codes)) == len(CREW)
    opened = {directory.login(code).profile for code in codes}
    assert opened == set(CREW)


def test_the_directory_rejects_duplicate_or_malformed_codes() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        AccessDirectory({"AST-0001": CREW[0], "ast-0001": CREW[1]})
    with pytest.raises(ValueError, match="format"):
        AccessDirectory({"nope": CREW[0]})


def test_the_error_never_echoes_the_typed_text() -> None:
    result = simulated_directory().login("<script>")
    assert "<script>" not in repr(result)
