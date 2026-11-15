"""Acoustic numbers from a voice note (T2, D-015, D-019, D-028). Pure Python, no audio kept.

``analyze`` takes the samples of one recording and returns a handful of numbers about *how* it was
said: pitch and its variation, speech rate, pauses and loudness. The numbers are inspired by the
GeMAPS voice-research set (Eyben et al., 2016) but are our own simple estimators, **experimental**:
there is no emotion label and nothing here moves a state. Jitter and shimmer are left out on
purpose: they are unreliable on noisy or compressed audio, which is what a spacecraft cabin gives.

The input is never modified and never stored. Only the returned numbers outlive the call.
"""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence
from dataclasses import dataclass

MIN_SECONDS = 5.0  # shorter notes say too little about a voice
MAX_PITCH_FRAMES = 1500  # long notes are sampled so the analysis stays quick

_WORKING_RATE = 4000  # Hz after a crude low-pass decimation: enough for the pitch of speech
_WINDOW_S = 0.025
_HOP_S = 0.010
_PITCH_WINDOW_S = 0.030
_MIN_F0, _MAX_F0 = 75.0, 400.0
_VOICED_CORRELATION = 0.4
_PAUSE_FRAMES = 25  # a quiet run of at least 250 ms counts as a pause, shorter dips do not
_SYLLABLE_GAP_FRAMES = 12  # nuclei closer than 120 ms are one syllable
_CLIP_LEVEL = 32000
_FEATURES = (
    "durationSeconds",
    "pitchMeanHz",
    "pitchVariation",
    "speechRate",
    "pauseRatio",
    "loudnessDb",
)


@dataclass(frozen=True, slots=True)
class VoiceAnalysis:
    features: dict[str, float]
    quality_ok: bool
    problems: tuple[str, ...]  # codes: too_short, low_signal, clipping, too_few_voiced


def _decimate(samples: Sequence[int], factor: int) -> list[float]:
    if factor <= 1:
        return [float(s) for s in samples]
    return [
        sum(samples[i : i + factor]) / factor for i in range(0, len(samples) - factor + 1, factor)
    ]


def _frame_rms(x: list[float], window: int, hop: int) -> list[float]:
    return [
        math.sqrt(sum(v * v for v in x[i : i + window]) / window)
        for i in range(0, len(x) - window + 1, hop)
    ]


def _percentile(sorted_values: list[float], fraction: float) -> float:
    return sorted_values[min(len(sorted_values) - 1, int(fraction * len(sorted_values)))]


def _pitch(frame: list[float], rate: int) -> float | None:
    """Pitch of one frame by normalised autocorrelation, or ``None`` if it is not voiced."""
    mean = sum(frame) / len(frame)
    x = [v - mean for v in frame]
    energy = sum(v * v for v in x)
    if energy <= 0:
        return None
    low, high = int(rate / _MAX_F0), int(rate / _MIN_F0)
    if high + 2 >= len(x):
        return None
    corr = {
        lag: sum(a * b for a, b in zip(x, x[lag:], strict=False)) / energy
        for lag in range(low - 1, high + 2)
    }
    best = max(corr[lag] for lag in range(low, high + 1))
    if best < _VOICED_CORRELATION:
        return None
    # the shortest strong peak: avoids picking a multiple of the period
    lag = next(
        (
            lag
            for lag in range(low, high + 1)
            if corr[lag] >= 0.85 * best
            and corr[lag] >= corr[lag - 1]
            and corr[lag] >= corr[lag + 1]
        ),
        None,
    )
    if lag is None:  # the strongest value sits at the edge of the range: no real peak inside it
        return None
    a, b, c = corr[lag - 1], corr[lag], corr[lag + 1]
    denominator = a - 2 * b + c
    shift = 0.5 * (a - c) / denominator if denominator else 0.0
    return rate / (lag + max(-1.0, min(1.0, shift)))


def _runs(flags: list[bool], value: bool) -> list[tuple[int, int]]:
    """Start and length of each run of ``value`` in ``flags``."""
    found: list[tuple[int, int]] = []
    start: int | None = None
    for index, flag in enumerate([*flags, not value]):
        if flag is value and start is None:
            start = index
        elif flag is not value and start is not None:
            found.append((start, index - start))
            start = None
    return found


def analyze(samples: Sequence[int], sample_rate: int) -> VoiceAnalysis:
    duration = len(samples) / sample_rate if sample_rate else 0.0
    problems: list[str] = []
    if duration < MIN_SECONDS:
        problems.append("too_short")
    clipped = sum(1 for s in samples if abs(s) >= _CLIP_LEVEL)
    if samples and clipped / len(samples) >= 0.01:
        problems.append("clipping")

    factor = max(1, sample_rate // _WORKING_RATE)
    rate = sample_rate // factor
    x = _decimate(samples, factor)
    window, hop = int(_WINDOW_S * rate), int(_HOP_S * rate)
    rms = _frame_rms(x, window, hop) if len(x) > window else []

    zero = dict.fromkeys(_FEATURES, 0.0)
    zero["durationSeconds"] = round(duration, 2)
    zero["loudnessDb"] = -90.0
    if not rms:
        return VoiceAnalysis(zero, False, (*problems, "low_signal"))

    ordered = sorted(rms)
    floor, top = _percentile(ordered, 0.10), _percentile(ordered, 0.90)
    threshold = max(floor * 2.5, top * 0.12)
    active = [value > threshold for value in rms]
    active_seconds = sum(active) * _HOP_S
    snr = 20 * math.log10(max(top, 1e-6) / max(floor, 1e-6))
    if active_seconds < 2.0 or snr < 10 or top < 150:
        return VoiceAnalysis(zero, False, (*problems, "low_signal"))

    first = active.index(True)
    last = len(active) - 1 - active[::-1].index(True)
    span = active[first : last + 1]
    pause_frames = sum(length for _, length in _runs(span, False) if length >= _PAUSE_FRAMES)
    pause_ratio = pause_frames / len(span)

    active_rms = [v for v, on in zip(rms, active, strict=True) if on]
    loudness = statistics.fmean(20 * math.log10(max(v, 1e-6) / 32768) for v in active_rms)

    # syllable nuclei: peaks of the smoothed energy envelope
    smooth = [statistics.fmean(rms[max(0, i - 2) : i + 3]) for i in range(len(rms))]
    peaks = 0
    last_peak = -_SYLLABLE_GAP_FRAMES
    for i in range(1, len(smooth) - 1):
        if (
            smooth[i] > threshold * 1.2
            and smooth[i] >= smooth[i - 1]
            and smooth[i] > smooth[i + 1]
            and i - last_peak >= _SYLLABLE_GAP_FRAMES
        ):
            peaks += 1
            last_peak = i
    speech_rate = peaks / max(active_seconds, 1.0)

    # pitch on the active stretches, every k-th frame so long notes stay quick
    pitch_window = int(_PITCH_WINDOW_S * rate)
    pitch_hop = pitch_window
    starts = [
        i * hop
        for i, on in enumerate(active)
        if on and i * hop % pitch_hop < hop and i * hop + pitch_window <= len(x)
    ]
    stride = max(1, math.ceil(len(starts) / MAX_PITCH_FRAMES))
    voiced: list[float] = []
    for start in starts[::stride]:
        found = _pitch(x[start : start + pitch_window], rate)
        if found is not None:
            voiced.append(found)
    if len(voiced) < 20:
        problems.append("too_few_voiced")
    if voiced:
        center = statistics.median(voiced)
        variation = (
            statistics.pstdev(12 * math.log2(f / center) for f in voiced) if len(voiced) > 1 else 0
        )
    else:
        center, variation = 0.0, 0.0

    features = {
        "durationSeconds": round(duration, 2),
        "pitchMeanHz": round(center, 1),
        "pitchVariation": round(variation, 2),
        "speechRate": round(speech_rate, 2),
        "pauseRatio": round(pause_ratio, 3),
        "loudnessDb": round(loudness, 1),
    }
    return VoiceAnalysis(features, not problems, tuple(problems))
