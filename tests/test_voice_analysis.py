"""T2: acoustic numbers from a voice note, on synthetic signals of known pitch and rhythm."""

from __future__ import annotations

import array
import math
import random

import pytest

from crew_self_check.core.voice_analysis import MIN_SECONDS, analyze

RATE = 16000


def speech_like(
    seconds: float = 12.0,
    f0: float = 130.0,
    glide: float = 0.0,
    syllables_per_second: float = 4.0,
    amplitude: float = 8000.0,
    pause_every: float = 0.0,
    pause_length: float = 0.0,
    noise: float = 30.0,
    seed: int = 1,
) -> array.array:
    """Harmonics at ``f0`` (gliding by ``glide`` semitones), shaped into syllables, with pauses."""
    rng = random.Random(seed)
    samples = array.array("h")
    phase = 0.0
    for n in range(int(seconds * RATE)):
        t = n / RATE
        in_pause = pause_every > 0 and (t % pause_every) > (pause_every - pause_length)
        envelope = 0.0 if in_pause else math.sin(math.pi * syllables_per_second * t) ** 2
        pitch = f0 * 2 ** ((glide * math.sin(2 * math.pi * 0.5 * t)) / 12)
        phase += 2 * math.pi * pitch / RATE
        voiced = sum(math.sin(h * phase) / h for h in range(1, 6))
        value = amplitude * envelope * voiced + rng.gauss(0, noise)
        samples.append(int(max(-32768, min(32767, value))))
    return samples


def test_pitch_is_found_within_a_few_percent() -> None:
    for f0 in (110.0, 130.0, 200.0):
        result = analyze(speech_like(f0=f0), RATE)
        assert result.features["pitchMeanHz"] == pytest.approx(f0, rel=0.05), f0


def test_a_steady_voice_has_no_pitch_variation_and_a_gliding_one_has_some() -> None:
    steady = analyze(speech_like(glide=0.0), RATE).features["pitchVariation"]
    gliding = analyze(speech_like(glide=4.0), RATE).features["pitchVariation"]
    assert steady < 0.6
    assert gliding > steady + 0.8


def test_the_speech_rate_follows_the_rhythm() -> None:
    slow = analyze(speech_like(syllables_per_second=2.5), RATE).features["speechRate"]
    fast = analyze(speech_like(syllables_per_second=5.0), RATE).features["speechRate"]
    assert fast > slow * 1.5
    assert fast == pytest.approx(5.0, rel=0.35)


def test_pauses_raise_the_pause_ratio() -> None:
    none = analyze(speech_like(), RATE).features["pauseRatio"]
    some = analyze(speech_like(pause_every=3.0, pause_length=1.2), RATE).features["pauseRatio"]
    assert some > none + 0.15
    assert 0.0 <= none <= 1.0 and 0.0 <= some <= 1.0


def test_a_louder_voice_measures_louder() -> None:
    quiet = analyze(speech_like(amplitude=3000), RATE).features["loudnessDb"]
    loud = analyze(speech_like(amplitude=12000), RATE).features["loudnessDb"]
    assert loud > quiet + 6


def test_a_good_note_passes_the_quality_check() -> None:
    result = analyze(speech_like(), RATE)
    assert result.quality_ok
    assert result.problems == ()


def test_silence_or_noise_alone_is_not_a_usable_note() -> None:
    rng = random.Random(3)
    noise = array.array("h", (int(rng.gauss(0, 200)) for _ in range(RATE * 10)))
    result = analyze(noise, RATE)
    assert not result.quality_ok
    assert result.problems


def test_a_note_that_is_too_short_is_flagged() -> None:
    result = analyze(speech_like(seconds=MIN_SECONDS - 2), RATE)
    assert not result.quality_ok
    assert "too_short" in result.problems


def test_a_clipped_recording_is_flagged() -> None:
    result = analyze(speech_like(amplitude=60000), RATE)
    assert "clipping" in result.problems


def test_only_numbers_come_out_and_nothing_that_looks_like_audio() -> None:
    result = analyze(speech_like(), RATE)
    assert all(isinstance(v, float) for v in result.features.values())
    assert set(result.features) == {
        "durationSeconds",
        "pitchMeanHz",
        "pitchVariation",
        "speechRate",
        "pauseRatio",
        "loudnessDb",
    }


def test_the_input_is_not_modified() -> None:
    samples = speech_like(seconds=6)
    copy = array.array("h", samples)
    analyze(samples, RATE)
    assert samples == copy


def test_a_long_note_is_analysed_in_reasonable_time() -> None:
    import time

    samples = speech_like(seconds=90)
    started = time.perf_counter()
    analyze(samples, RATE)
    assert time.perf_counter() - started < 20


def test_a_tone_below_the_pitch_range_is_unvoiced_and_does_not_crash() -> None:
    """Regression: a correlation peak at the edge of the lag range raised StopIteration."""
    import math

    from crew_self_check.core.voice_analysis import _pitch

    rate = 16000
    frame = [math.sin(2 * math.pi * 70 * i / rate) * 3000 for i in range(1024)]
    assert _pitch(frame, rate) is None
