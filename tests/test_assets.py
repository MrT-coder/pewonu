"""The pulse guide illustrations: one per step and language, all real JPEG files."""

from pathlib import Path

import pytest

from crew_self_check.core.reasons import Language

PULSE_ASSETS = Path(__file__).resolve().parent.parent / "src/crew_self_check/astronaut/assets/pulse"


@pytest.mark.parametrize("language", list(Language))
@pytest.mark.parametrize("step", [1, 2, 3, 4])
def test_every_step_has_an_illustration_in_both_languages(language: Language, step: int) -> None:
    path = PULSE_ASSETS / f"{language.value}-step{step}.jpg"
    assert path.is_file(), path
    assert path.read_bytes()[:3] == bytes([0xFF, 0xD8, 0xFF])  # JPEG signature
    assert path.stat().st_size > 10_000


def test_there_are_no_other_files_in_the_guide_folder() -> None:
    names = {p.name for p in PULSE_ASSETS.iterdir() if p.name != "README.md"}
    assert names == {f"{lang.value}-step{n}.jpg" for lang in Language for n in range(1, 5)}
