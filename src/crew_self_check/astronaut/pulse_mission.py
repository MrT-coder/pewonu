"""The manual pulse as a guided mission (D-014, D-021). Pure logic.

Technique (MedlinePlus, https://medlineplus.gov/ency/article/003399.htm): rest first, index and
middle fingers on the inside of the wrist, light pressure, then count for a full minute or for 30
seconds and double it. The astronaut counts with the fingers on the wrist and **enters** how many
beats they counted; the app calculates the beats per minute. There is nothing to tap while counting.

The game rewards the technique and the regularity of measuring, **never the value**: the points and
the badge are the same for any pulse (AGENTS.md, section 6; A12). The plausibility limits below are
a data-entry check ("recount, you probably lost count"), not a clinical threshold.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source

INTERVALS = (30, 60)  # seconds to count: 30 s doubles, 60 s is direct
MIN_PLAUSIBLE_BPM = 20
MAX_PLAUSIBLE_BPM = 250

STEP_POINTS = 10  # for each of the three confirmed steps
ATTEMPT_POINTS = 10  # for entering a count, whatever it gave
MEASUREMENT_BONUS = 20  # for a count that gives a usable measurement


class Station(StrEnum):
    REST = "rest"
    LOCATE = "locate"
    PRESSURE = "pressure"
    COUNT = "count"
    RESULT = "result"


_STEPS = (Station.REST, Station.LOCATE, Station.PRESSURE)
_ORDER = (*_STEPS, Station.COUNT, Station.RESULT)


@dataclass(frozen=True, slots=True)
class PulseResult:
    beats: int  # what the astronaut counted
    interval: int  # seconds they counted for
    bpm: int
    valid: bool  # inside the plausibility limits; if not, the app asks for a recount


class PulseMission:
    def __init__(self, interval: int = 30) -> None:
        self._check_interval(interval)
        self.interval = interval
        self.station = Station.REST
        self.result: PulseResult | None = None
        self._attempted = False

    @staticmethod
    def _check_interval(interval: int) -> None:
        if interval not in INTERVALS:
            raise ValueError(f"interval must be one of {INTERVALS}, got {interval}")

    def set_interval(self, interval: int) -> None:
        self._check_interval(interval)
        if self.station is Station.RESULT:
            raise RuntimeError("the interval can only change before the count is entered")
        self.interval = interval

    # --- the three steps -------------------------------------------------------------------

    def complete_station(self) -> None:
        """Confirm the current step (rest, locate, pressure) and move to the next station."""
        if self.station not in _STEPS:
            raise RuntimeError("the steps are done: use the count station")
        self.station = _ORDER[_ORDER.index(self.station) + 1]

    # --- the count -------------------------------------------------------------------------

    def submit_count(self, beats: int) -> PulseResult:
        """Enter how many beats were counted in ``interval`` seconds and calculate the bpm."""
        if self.station is Station.RESULT:
            raise RuntimeError("the count was already entered: retry to count again")
        if self.station is not Station.COUNT:
            raise RuntimeError("confirm the steps before entering the count")
        if isinstance(beats, bool) or not isinstance(beats, int) or beats < 0:
            raise ValueError(f"beats must be a whole number of 0 or more, got {beats!r}")
        bpm = round(beats * 60 / self.interval)
        self.result = PulseResult(
            beats=beats,
            interval=self.interval,
            bpm=bpm,
            valid=MIN_PLAUSIBLE_BPM <= bpm <= MAX_PLAUSIBLE_BPM,
        )
        self._attempted = True
        self.station = Station.RESULT
        return self.result

    def retry(self) -> None:
        """Count again after an implausible result; the steps do not have to be repeated."""
        if self.result is None or self.result.valid:
            raise RuntimeError("a retry only makes sense after an implausible result")
        self.result = None
        self.station = Station.COUNT

    # --- the game: technique, never the value ----------------------------------------------

    @property
    def points(self) -> int:
        reached = _ORDER.index(self.station)
        total = sum(STEP_POINTS for index in range(len(_STEPS)) if reached > index)
        if self._attempted:
            total += ATTEMPT_POINTS
        if self.result is not None and self.result.valid:
            total += MEASUREMENT_BONUS
        return total

    @property
    def earned_badge(self) -> bool:
        return self.result is not None and self.result.valid

    # --- the result is a contract measurement ----------------------------------------------

    def to_measurement(
        self, crew_id: str, environment: Environment, timestamp: datetime
    ) -> Measurement:
        if self.result is None:
            raise RuntimeError("there is no result yet")
        if not self.result.valid:
            raise RuntimeError("the result is not valid: count again")
        return Measurement(
            crew_id=crew_id,
            indicator=Indicator.RESTING_HR,
            value=float(self.result.bpm),
            unit="bpm",
            timestamp=timestamp,
            source=Source.MANUAL,
            environment=environment,
            method=Method.PALPATION,
        )
