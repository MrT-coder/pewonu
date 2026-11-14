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


# --- acronyms are explained (D-024) -----------------------------------------------------------

ACRONYM = re.compile(r"\b(?:[A-Z]{2,}|bpm|lpm)\b")
PLACEHOLDER = re.compile(r"{\w+}")  # {bpm} names a value, it is not text the user reads


@pytest.mark.parametrize("language", list(Language))
def test_every_acronym_in_the_interface_is_in_the_glossary(language: Language) -> None:
    from crew_self_check.astronaut.i18n import glossary_terms

    known = glossary_terms(language)
    unexplained = {
        (key, token)
        for key, by_language in STRINGS.items()
        for token in ACRONYM.findall(PLACEHOLDER.sub("", by_language[language]))
        if token not in known
    }
    assert not unexplained, f"add these to the glossary or spell them out: {sorted(unexplained)}"


@pytest.mark.parametrize("language", list(Language))
def test_the_glossary_has_a_definition_for_every_term(language: Language) -> None:
    from crew_self_check.astronaut.i18n import GLOSSARY

    assert GLOSSARY
    for entry in GLOSSARY:
        term, definition = entry[language]
        assert term.strip()
        assert len(definition.split()) >= 2, (term, definition)


def test_the_pulse_unit_is_spelled_out_where_it_is_the_main_datum() -> None:
    for key, expected in [
        ("pulse.formula_30", {Language.EN: "beats per minute", Language.ES: "latidos por minuto"}),
        ("pulse.formula_60", {Language.EN: "beats per minute", Language.ES: "latidos por minuto"}),
        ("pulse.last", {Language.EN: "beats per minute", Language.ES: "latidos por minuto"}),
    ]:
        for language, phrase in expected.items():
            assert phrase in STRINGS[key][language], (key, language)


def test_ai_and_nih_are_spelled_out_next_to_the_acronym() -> None:
    assert "artificial intelligence (AI)" in STRINGS["pulse.illustrations"][Language.EN]
    assert "inteligencia artificial (IA)" in STRINGS["pulse.illustrations"][Language.ES]
    assert "National Institutes of Health (NIH)" in STRINGS["pulse.source"][Language.EN]
    assert "Institutos Nacionales de Salud" in STRINGS["pulse.source"][Language.ES]


def test_the_code_prefix_is_explained_where_the_code_is_asked() -> None:
    assert "AST = astronaut" in STRINGS["login.error.invalid_format"][Language.EN]
    assert "AST = astronauta" in STRINGS["login.error.invalid_format"][Language.ES]
