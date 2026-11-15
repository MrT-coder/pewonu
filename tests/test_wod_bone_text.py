"""The bone note must not print a projection for zero time in space."""

import pytest

from crew_self_check.astronaut.ui.pewonu import bone_text
from crew_self_check.core.reasons import Language
from crew_self_check.core.wod import BoneNote


def _note(months: float) -> BoneNote:
    return BoneNote(
        baseline=1.04, months=months, expected_low_pct=months, expected_high_pct=2 * months
    )


@pytest.mark.parametrize("language", list(Language))
def test_on_earth_the_note_gives_the_range_without_a_zero_projection(language: Language) -> None:
    text = bone_text(_note(0.0), language)
    assert "1.04" in text
    assert "0.0" not in text


@pytest.mark.parametrize("language", list(Language))
def test_in_space_the_note_keeps_the_projection(language: Language) -> None:
    text = bone_text(_note(2.0), language)
    assert "2.0" in text and "4.0" in text
