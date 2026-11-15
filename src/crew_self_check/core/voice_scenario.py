"""Simulated voice notes for the demo cases (T2, D-028). Everything here is simulated analog data.

One note per day for ``crew-01`` (stable: her case is about arrival, not about voice) and for
``crew-03`` (the isolation case: from T+3 his speech slows, his pauses lengthen, his pitch flattens
and his voice softens, as the sleep and mood readings fall). ``crew-02`` has no voice history, which
shows the baseline still building. Numbers only: no audio, no transcript, no emotion label.
Reproducible: a fixed variation, no random numbers.
"""

from __future__ import annotations

from datetime import timedelta

from crew_self_check.core.contract import Indicator, VoiceFeatures
from crew_self_check.core.scenario import EARTH_DAYS, Scenario, ScenarioDay

_NOTE_HOUR = timedelta(hours=12)  # midday of the journey day, like the astronaut's own entries
_WOBBLE = (0.0, 1.0, -1.0, 0.5, -0.5, 1.0, -1.0)

# (pitch Hz, pitch variation semitones, syllables/s, pause ratio, loudness dB) on a normal day
_USUAL = {
    "crew-01": (190.0, 2.6, 4.7, 0.21, -24.0),
    "crew-03": (118.0, 2.4, 4.5, 0.22, -23.0),
}
# crew-03 in transit, as a fraction of the way to the lowest point (T+3 to T+8), then it holds
_DRIFT_FROM = EARTH_DAYS + 2  # index of T+3
_DRIFT_DAYS = 6
_LOW = {"pitchVariation": -1.2, "speechRate": -1.7, "pauseRatio": 0.2, "loudnessDb": -5.0}


def _wobble(day: int, amount: float) -> float:
    return _WOBBLE[day % len(_WOBBLE)] * amount


def _features(crew_id: str, day: ScenarioDay) -> dict[str, float]:
    pitch, variation, rate, pause, loudness = _USUAL[crew_id]
    features = {
        "durationSeconds": 48.0 + _wobble(day.index, 6.0),
        "pitchMeanHz": pitch + _wobble(day.index, 3.0),
        "pitchVariation": variation + _wobble(day.index + 1, 0.15),
        "speechRate": rate + _wobble(day.index + 2, 0.15),
        "pauseRatio": pause + _wobble(day.index + 3, 0.015),
        "loudnessDb": loudness + _wobble(day.index + 4, 0.6),
    }
    if crew_id == "crew-03" and day.index >= _DRIFT_FROM:
        progress = min(1.0, (day.index - _DRIFT_FROM + 1) / _DRIFT_DAYS)
        if day.index >= _DRIFT_FROM + 11:  # a little recovery on the planet
            progress = 0.7
        for name, delta in _LOW.items():
            features[name] += delta * progress
    return {name: round(value, 3) for name, value in features.items()}


def generate_voice_notes(scenario: Scenario) -> tuple[VoiceFeatures, ...]:
    mood = {
        (m.crew_id, m.timestamp.date()): int(m.value)
        for m in scenario.measurements
        if m.indicator is Indicator.MOOD
    }
    notes: list[VoiceFeatures] = []
    for day in scenario.days:
        for crew_id in _USUAL:
            notes.append(
                VoiceFeatures(
                    crew_id=crew_id,
                    timestamp=day.timestamp + _NOTE_HOUR,
                    environment=day.environment,
                    features={k: float(v) for k, v in _features(crew_id, day).items()},
                    mood_survey_score=mood.get((crew_id, day.timestamp.date()), 0),
                )
            )
    return tuple(notes)
