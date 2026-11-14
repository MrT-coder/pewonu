"""Part 1: English source and Spanish translation (D-016)."""

import re

import pytest

from crew_self_check.astronaut.i18n import SAME_IN_BOTH, STRINGS, translate
from crew_self_check.core.reasons import Language


def fields(text: str) -> set[str]:
    return set(re.findall(r"{(\w+)}", text))


def test_every_key_has_both_languages_and_none_is_blank() -> None:
    for key, by_language in STRINGS.items():
        assert set(by_language) == set(Language), key
        for language, text in by_language.items():
            assert text.strip(), (key, language)


def test_both_languages_use_the_same_placeholders() -> None:
    for key, by_language in STRINGS.items():
        assert fields(by_language[Language.EN]) == fields(by_language[Language.ES]), key


def test_spanish_is_really_translated() -> None:
    same = [
        k for k, v in STRINGS.items() if v[Language.EN] == v[Language.ES] and k not in SAME_IN_BOTH
    ]
    assert not same, f"identical in both languages (translate or justify): {same}"


def test_translate_formats_parameters() -> None:
    assert "AST-0001" in translate("home.greeting", Language.EN, code="AST-0001")
    assert "AST-0001" in translate("home.greeting", Language.ES, code="AST-0001")


def test_an_unknown_key_or_missing_parameter_is_an_error_not_a_blank() -> None:
    with pytest.raises(KeyError):
        translate("no.such.key", Language.EN)
    with pytest.raises(KeyError):
        translate("home.greeting", Language.EN)


def test_the_limits_are_stated_in_both_languages() -> None:
    en = translate("limits.body", Language.EN).lower()
    es = translate("limits.body", Language.ES).lower()
    assert "simulated" in en and "diagnos" in en
    assert "simulad" in es and "diagnostic" in es


FORBIDDEN = (
    "detects disease",
    "diagnoses ",
    "risk of",
    "bradycardia",
    "tachycardia",
    "bradicardia",
    "taquicardia",
    "detecta enfermedad",
    "0 bytes",
)


def test_no_text_claims_a_diagnosis_or_an_unverifiable_promise() -> None:
    for key, by_language in STRINGS.items():
        for text in by_language.values():
            assert not any(word in text.lower() for word in FORBIDDEN), (key, text)
