"""Compare a voice note with the person's own earlier notes (T2, D-028). Pure Python.

There is no population norm and no emotion label: a note is only "usual" or "different from your
usual", and the numbers that moved say in which direction. The reference is the same person's
earlier notes, like the indicator baseline (D-013): the notes of the same place (Earth, spacecraft,
planet) once there are enough of them, and meanwhile the notes of the previous place, said so on
screen (``reference: transition``). Without that rule a drift that starts on arrival would become
its own baseline within days. It never moves a state: the result is context, not an alert.
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from crew_self_check.core.contract import Environment, VoiceFeatures

MIN_NOTES = 4  # earlier notes needed before a note can be compared
MATURE_NOTES = 10  # earlier notes of the same place after which they are the reference
CHANGE_Z = 2.5  # robust distance at which one measure counts as changed
MIN_CHANGED = 2  # changed measures needed to call the whole note different
_MAD_SCALE = 1.4826

COMPARED = ("pitchMeanHz", "pitchVariation", "speechRate", "pauseRatio", "loudnessDb")
# The smallest spread that counts, so a very steady history does not make every wobble a change.
_MIN_SCALE = {
    "pitchMeanHz": 4.0,
    "pitchVariation": 0.35,
    "speechRate": 0.35,
    "pauseRatio": 0.04,
    "loudnessDb": 1.5,
}
_PREVIOUS = {
    Environment.EARTH: (),
    Environment.SPACECRAFT: (Environment.EARTH,),
    Environment.PLANET: (Environment.SPACECRAFT, Environment.EARTH),
}


class VoiceLevel(StrEnum):
    BUILDING = "building"  # not enough earlier notes yet
    USUAL = "usual"
    DIFFERENT = "different"


@dataclass(frozen=True, slots=True)
class FeatureDeviation:
    name: str
    value: float
    center: float  # the median of the reference notes
    z: float  # robust distance from the center, in spreads
    direction: str | None  # "up" or "down" when it changed, else ``None``


@dataclass(frozen=True, slots=True)
class VoiceComparison:
    level: VoiceLevel
    n_previous: int  # notes in the reference
    deviations: tuple[FeatureDeviation, ...]
    reference: str = "personal"  # "personal" (same place) or "transition" (previous place)
    baseline_environment: Environment | None = None  # set when the reference is the previous place

    @property
    def changed(self) -> tuple[str, ...]:
        return tuple(d.name for d in self.deviations if d.direction is not None)


def _reference(
    earlier: list[VoiceFeatures], environment: Environment
) -> tuple[list[VoiceFeatures], str, Environment | None]:
    same = [n for n in earlier if n.environment is environment]
    if len(same) >= MATURE_NOTES:
        return same, "personal", None
    for previous in _PREVIOUS[environment]:
        notes = [n for n in earlier if n.environment is previous]
        if len(notes) >= MIN_NOTES:
            return notes, "transition", previous
    return same, "personal", None


def compare(history: Sequence[VoiceFeatures], new: VoiceFeatures) -> VoiceComparison:
    earlier = [
        n
        for n in history
        if n is not new and n.crew_id == new.crew_id and n.timestamp < new.timestamp
    ]
    notes, reference, previous = _reference(earlier, new.environment)
    if len(notes) < MIN_NOTES:
        return VoiceComparison(VoiceLevel.BUILDING, len(notes), (), reference, previous)
    deviations: list[FeatureDeviation] = []
    for name in COMPARED:
        values = [n.features[name] for n in notes if name in n.features]
        if len(values) < MIN_NOTES or name not in new.features:
            continue
        center = statistics.median(values)
        spread = _MAD_SCALE * statistics.median(abs(v - center) for v in values)
        z = (new.features[name] - center) / max(spread, _MIN_SCALE[name])
        direction = None if abs(z) < CHANGE_Z else ("up" if z > 0 else "down")
        deviations.append(
            FeatureDeviation(name, new.features[name], center, round(z, 2), direction)
        )
    changed = sum(1 for d in deviations if d.direction is not None)
    level = VoiceLevel.DIFFERENT if changed >= MIN_CHANGED else VoiceLevel.USUAL
    return VoiceComparison(level, len(notes), tuple(deviations), reference, previous)
