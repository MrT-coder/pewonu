"""T2: a voice note is compared with the person's own earlier notes, never with a population."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from crew_self_check.core.contract import Environment, VoiceFeatures
from crew_self_check.core.scenario import generate_scenario
from crew_self_check.core.voice_baseline import MIN_NOTES, VoiceLevel, compare
from crew_self_check.core.voice_scenario import generate_voice_notes

START = datetime(2026, 11, 1, 20, 0, tzinfo=UTC)
USUAL = {
    "pitchMeanHz": 120.0,
    "pitchVariation": 2.5,
    "speechRate": 4.5,
    "pauseRatio": 0.2,
    "loudnessDb": -24.0,
}


def note(day: int, crew: str = "crew-01", env: Environment = Environment.EARTH, **changes: float):
    features = {**USUAL, **changes}
    # a tiny fixed wobble so the history has some spread
    features["speechRate"] += (day % 3 - 1) * 0.1
    features["pitchMeanHz"] += (day % 4 - 1.5) * 1.0
    return VoiceFeatures(crew, START + timedelta(days=day), env, features, 4)


def history(n: int, **kwargs) -> list[VoiceFeatures]:
    return [note(i, **kwargs) for i in range(n)]


def test_the_first_notes_only_build_the_baseline() -> None:
    result = compare(history(MIN_NOTES - 1), note(MIN_NOTES))
    assert result.level is VoiceLevel.BUILDING
    assert result.n_previous == MIN_NOTES - 1
    assert result.deviations == ()


def test_a_note_like_the_usual_is_usual() -> None:
    result = compare(history(8), note(9))
    assert result.level is VoiceLevel.USUAL
    assert result.changed == ()


def test_slower_speech_and_longer_pauses_are_reported_as_different_with_their_direction() -> None:
    result = compare(history(8), note(9, speechRate=2.8, pauseRatio=0.42))
    assert result.level is VoiceLevel.DIFFERENT
    by_name = {d.name: d for d in result.deviations}
    assert by_name["speechRate"].direction == "down"
    assert by_name["pauseRatio"].direction == "up"
    assert set(result.changed) >= {"speechRate", "pauseRatio"}


def test_one_changed_measure_alone_is_not_enough_to_call_it_different() -> None:
    result = compare(history(8), note(9, loudnessDb=-33.0))
    assert result.level is VoiceLevel.USUAL
    assert result.changed == ("loudnessDb",)


def test_a_flat_history_does_not_make_every_wobble_a_change() -> None:
    flat = [
        VoiceFeatures("crew-01", START + timedelta(days=i), Environment.EARTH, USUAL, 4)
        for i in range(8)
    ]
    result = compare(flat, note(9))
    assert result.level is VoiceLevel.USUAL


def test_only_notes_of_the_same_person_and_place_count() -> None:
    mixed = history(8, crew="crew-02") + history(8, env=Environment.SPACECRAFT)
    result = compare(mixed, note(20))
    assert result.level is VoiceLevel.BUILDING
    assert result.n_previous == 0


def test_the_new_note_is_not_part_of_its_own_baseline() -> None:
    new = note(9, speechRate=2.8, pauseRatio=0.42)
    result = compare([*history(8), new], new)
    assert result.level is VoiceLevel.DIFFERENT


@pytest.mark.parametrize("seed", [0, 7])
def test_the_isolation_case_drifts_in_transit_and_the_others_do_not(seed: int) -> None:
    scenario = generate_scenario(seed)
    notes = generate_voice_notes(scenario)

    def level_on(label: str, crew: str) -> VoiceLevel:
        day = next(d for d in scenario.days if d.label == label)
        mine = [
            n for n in notes if n.crew_id == crew and n.timestamp.date() <= day.timestamp.date()
        ]
        return compare(mine[:-1], mine[-1]).level

    assert level_on("E-1", "crew-03") is VoiceLevel.USUAL
    assert level_on("T+8", "crew-03") is VoiceLevel.DIFFERENT
    for day in scenario.days:
        assert level_on(day.label, "crew-01") is not VoiceLevel.DIFFERENT, day.label


def test_the_simulated_notes_are_numbers_flagged_experimental_and_reproducible() -> None:
    scenario = generate_scenario()
    notes = generate_voice_notes(scenario)
    assert notes == generate_voice_notes(scenario)
    assert {n.crew_id for n in notes} == {"crew-01", "crew-03"}  # crew-02 has no voice history
    for n in notes:
        assert n.to_dict()["experimental"] is True
        assert all(isinstance(v, float) for v in n.features.values())


def test_in_a_new_place_the_previous_place_is_the_reference_until_there_are_enough_notes() -> None:
    earth = history(14)
    ship = [
        note(14 + i, env=Environment.SPACECRAFT, speechRate=2.9, pauseRatio=0.4) for i in range(3)
    ]
    new = note(17, env=Environment.SPACECRAFT, speechRate=2.9, pauseRatio=0.4)
    result = compare([*earth, *ship], new)
    assert result.reference == "transition"
    assert result.baseline_environment is Environment.EARTH
    assert result.level is VoiceLevel.DIFFERENT


def test_once_the_new_place_has_enough_notes_it_is_its_own_reference() -> None:
    earth = history(14)
    ship = [
        note(14 + i, env=Environment.SPACECRAFT, speechRate=2.9, pauseRatio=0.4) for i in range(10)
    ]
    new = note(24, env=Environment.SPACECRAFT, speechRate=2.9, pauseRatio=0.4)
    result = compare([*earth, *ship], new)
    assert result.reference == "personal"
    assert result.baseline_environment is None
    assert result.level is VoiceLevel.USUAL
