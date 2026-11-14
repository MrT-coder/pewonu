"""C4: deterministic reason templates in English and Spanish."""

import re

import pytest

from crew_self_check.core.contract import Environment
from crew_self_check.core.reasons import (
    TEMPLATES,
    Language,
    Reason,
    ReasonCode,
)


def fields(template: str) -> set[str]:
    return set(re.findall(r"{(\w+)}", template))


def test_every_code_has_both_languages() -> None:
    assert set(TEMPLATES) == set(ReasonCode)
    for code, by_language in TEMPLATES.items():
        assert set(by_language) == set(Language), code
        for text in by_language.values():
            assert text.strip(), code


def test_both_languages_use_the_same_placeholders() -> None:
    for code, by_language in TEMPLATES.items():
        assert fields(by_language[Language.EN]) == fields(by_language[Language.ES]), code


def test_the_contract_example_reason_is_reproduced() -> None:
    reason = Reason(ReasonCode.PERSONAL_ABOVE, {"n": 3})
    assert reason.text(Language.EN) == "3 consecutive readings above personal range"
    assert reason.text(Language.ES) == "3 lecturas seguidas por encima de tu rango personal"


def test_environment_names_are_localised() -> None:
    reason = Reason(ReasonCode.TRANSITION_OK, {"previous": Environment.EARTH})
    assert "Earth" in reason.text(Language.EN)
    assert "Tierra" in reason.text(Language.ES)
    assert "earth" not in reason.text(Language.EN)


POPULATION_CODES = [code for code in ReasonCode if code.name.startswith("POPULATION")]


@pytest.mark.parametrize("code", POPULATION_CODES)
def test_population_reasons_say_it_is_not_the_personal_baseline(code: ReasonCode) -> None:
    reason = Reason(code, {})
    assert "population" in reason.text(Language.EN).lower()
    assert "poblaci" in reason.text(Language.ES).lower()


def test_text_is_deterministic() -> None:
    reason = Reason(ReasonCode.BUILDING_BASELINE, {"days": 2, "needed": 5})
    assert reason.text(Language.EN) == reason.text(Language.EN)
    assert reason.text(Language.EN) == "Building your personal baseline: 2 of 5 days."


def test_missing_parameter_is_an_error_not_a_blank() -> None:
    with pytest.raises(KeyError):
        Reason(ReasonCode.PERSONAL_ABOVE, {}).text(Language.EN)


def test_no_template_diagnoses() -> None:
    forbidden = ("diagnos", "disease", "illness", "enfermedad", "diagnóstic")
    for by_language in TEMPLATES.values():
        for text in by_language.values():
            assert not any(word in text.lower() for word in forbidden), text


def test_the_spanish_texts_have_no_contraction_mistakes() -> None:
    for code, by_language in TEMPLATES.items():
        text = " " + by_language[Language.ES].lower() + " "
        assert " de el " not in text, code
        assert " a el " not in text, code
