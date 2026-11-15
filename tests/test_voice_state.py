"""T2: the voice log in the app state: prompt, record, analyse, keep only numbers."""

from __future__ import annotations

import array
import itertools
import random
from pathlib import Path

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.sqlite_store import SqliteVoiceStore
from crew_self_check.astronaut.state import AppState, VoiceStage
from crew_self_check.astronaut.voice_capture import VOICE_PROMPTS, SyntheticVoiceRecorder
from crew_self_check.core.storage import InMemoryVoiceStore
from crew_self_check.core.voice_analysis import analyze
from crew_self_check.core.voice_baseline import VoiceLevel


class FakeRecorder:
    """Records a prepared signal and remembers whether the app asked to throw it away."""

    def __init__(self, samples: array.array, rate: int = 16000) -> None:
        self._samples, self._rate = samples, rate
        self.running = False
        self.released = False

    def available(self) -> bool:
        return True

    def start(self) -> None:
        self.running = True

    def level(self) -> float:
        return 0.4 if self.running else 0.0

    def stop(self) -> tuple[array.array, int]:
        self.running = False
        samples, self._samples = self._samples, array.array("h")
        self.released = True
        return samples, self._rate


def _signal(seconds: float = 12.0, **kwargs: float) -> array.array:
    from test_voice_analysis import speech_like

    return speech_like(seconds=seconds, **kwargs)


def _state(recorder: FakeRecorder | None = None, code: str = "AST-0003", **kwargs) -> AppState:
    state = AppState(simulated_directory(), voice_recorder=recorder, **kwargs)
    state.login(code)
    return state


def test_the_prompts_are_open_questions_and_there_are_a_few_not_thirty() -> None:
    assert 5 <= len(VOICE_PROMPTS) <= 10
    for key in VOICE_PROMPTS:
        assert not translate_is_yes_no(key)


def translate_is_yes_no(key: str) -> bool:
    from crew_self_check.astronaut.i18n import translate
    from crew_self_check.core.reasons import Language

    first = translate(key, Language.EN).split()[0].lower()
    return first in {"are", "is", "do", "did", "have", "can", "will", "would", "were", "was"}


def test_a_new_prompt_is_random_but_never_repeats_the_last_one() -> None:
    state = _state()
    state.set_voice_rng(random.Random(5))
    seen = [state.new_voice_prompt() for _ in range(30)]
    assert len(set(seen)) > 1
    assert all(a != b for a, b in itertools.pairwise(seen))
    assert set(seen) <= set(VOICE_PROMPTS)


def test_without_a_microphone_the_app_says_so() -> None:
    state = _state(None)
    assert not state.voice_available()


def test_recording_then_stopping_gives_a_result_and_throws_the_audio_away() -> None:
    recorder = FakeRecorder(_signal())
    state = _state(recorder)
    state.start_voice()
    assert state.voice_stage is VoiceStage.RECORDING
    assert recorder.running
    result = state.stop_voice()
    assert state.voice_stage is VoiceStage.RESULT
    assert recorder.released
    assert result.analysis.quality_ok
    assert result.saved
    assert result.comparison is not None


def test_only_numbers_are_kept_never_the_samples() -> None:
    store = InMemoryVoiceStore()
    state = _state(FakeRecorder(_signal()), voice_store=store)
    state.start_voice()
    state.stop_voice()
    (kept,) = store.all()
    assert set(kept.features) == {
        "durationSeconds",
        "pitchMeanHz",
        "pitchVariation",
        "speechRate",
        "pauseRatio",
        "loudnessDb",
    }
    assert all(isinstance(v, float) for v in kept.features.values())
    for value in vars(state).values():
        assert not isinstance(value, array.array | bytes | bytearray)


def test_a_note_with_poor_quality_is_reported_and_not_saved() -> None:
    store = InMemoryVoiceStore()
    state = _state(FakeRecorder(_signal(seconds=2.0)), voice_store=store)
    state.start_voice()
    result = state.stop_voice()
    assert not result.saved
    assert "too_short" in result.analysis.problems
    assert store.all() == ()


def test_the_isolation_case_shows_a_different_voice_in_transit() -> None:
    state = _state(
        FakeRecorder(_signal(syllables_per_second=2.2, pause_every=3.0, pause_length=1.4))
    )
    state.set_day(next(d.index for d in state.scenario.days if d.label == "T+8"))
    state.start_voice()
    result = state.stop_voice()
    assert result.comparison is not None
    assert result.comparison.level is VoiceLevel.DIFFERENT


def test_a_person_without_voice_history_starts_building_the_baseline() -> None:
    state = _state(FakeRecorder(_signal()), code="AST-0002")
    state.start_voice()
    result = state.stop_voice()
    assert result.comparison is not None
    assert result.comparison.level is VoiceLevel.BUILDING


def test_the_history_includes_the_simulated_notes_up_to_today_and_the_persons_own() -> None:
    state = _state(FakeRecorder(_signal()))
    state.set_day(next(d.index for d in state.scenario.days if d.label == "T+2"))
    before = len(state.voice_history())
    assert before == 16  # 14 Earth days + T+1 + T+2
    state.start_voice()
    state.stop_voice()
    assert len(state.voice_history()) == before + 1


def test_the_notes_survive_a_restart(tmp_path: Path) -> None:
    path = tmp_path / "voice.db"
    first = _state(FakeRecorder(_signal()), voice_store=SqliteVoiceStore(path))
    first.start_voice()
    first.stop_voice()
    again = _state(None, voice_store=SqliteVoiceStore(path))
    assert len(again.voice_history()) == len(first.voice_history())


def test_leaving_the_screen_while_recording_stops_and_discards() -> None:
    recorder = FakeRecorder(_signal())
    state = _state(recorder)
    state.start_voice()
    state.cancel_voice()
    assert state.voice_stage is VoiceStage.IDLE
    assert recorder.released
    assert not state.voice_history_own()


def test_the_synthetic_sample_is_labelled_and_analysable() -> None:
    recorder = SyntheticVoiceRecorder()
    assert recorder.available()
    assert recorder.synthetic
    recorder.start()
    samples, rate = recorder.stop()
    assert analyze(samples, rate).quality_ok


def test_without_a_session_nothing_can_be_recorded() -> None:
    state = AppState(simulated_directory(), voice_recorder=FakeRecorder(_signal()))
    with pytest.raises(RuntimeError):
        state.start_voice()
