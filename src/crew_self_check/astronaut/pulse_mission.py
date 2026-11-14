"""The manual pulse as a guided mission (D-014, D-021). Pure logic: times are passed in explicitly.

Technique (MedlinePlus, https://medlineplus.gov/ency/article/003399.htm): rest first, index and
middle fingers on the inside of the wrist, light pressure, then count for a full minute or for 30
seconds and double it. The app counts the taps and calculates the beats per minute.

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
ATTEMPT_POINTS = 10  # for finishing a count, whatever it gave
MEASUREMENT_BONUS = 20  # for a count that gives a usable measurement


class Station(StrEnum):
    REST = "rest"
    LOCATE = "locate"
    PRESSURE = "pressure"
    COUNT = "count"
    RESULT = "result"


_STEPS = (Station.REST, Station.LOCATE, Station.PRESSURE)


@dataclass(frozen=True, slots=True)
class PulseResult:
    taps: int
    interval: int
    bpm: int
    valid: bool  # inside the plausibility limits; if not, the app asks for a recount


class PulseMission:
    def __init__(self, interval: int = 30) -> None:
        self._check_interval(interval)
        self.interval = interval
        self.station = Station.REST
        self.taps = 0
        self.result: PulseResult | None = None
        self._started_at: float | None = None
        self._attempted = False

    @staticmethod
    def _check_interval(interval: int) -> None:
        if interval not in INTERVALS:
            raise ValueError(f"interval must be one of {INTERVALS}, got {interval}")

    def set_interval(self, interval: int) -> None:
        self._check_interval(interval)
        if self._started_at is not None or self.station is Station.RESULT:
            raise RuntimeError("the interval can only change before counting")
        self.interval = interval

    # --- the three steps -------------------------------------------------------------------

    def complete_station(self) -> None:
        """Confirm the current step (rest, locate, pressure) and move to the next station."""
        if self.station not in _STEPS:
            raise RuntimeError("the steps are done: use the count station")
        self.station = Station(
            {
                Station.REST: Station.LOCATE,
                Station.LOCATE: Station.PRESSURE,
                Station.PRESSURE: Station.COUNT,
            }[self.station]
        )

    # --- the count -------------------------------------------------------------------------

    def start_count(self, now: float) -> None:
        if self.station is not Station.COUNT:
            raise RuntimeError("confirm the steps before counting")
        if self._started_at is not None:
            raise RuntimeError("already counting")
        self._started_at = now
        self.taps = 0

    @property
    def counting(self) -> bool:
        """True while the count is running (started and not finished)."""
        return self._started_at is not None and self.result is None

    def remaining(self, now: float) -> float:
        if self._started_at is None:
            return float(self.interval)
        return max(0.0, self._started_at + self.interval - now)

    def tap(self, now: float) -> bool:
        """Count one beat if the window is open; returns whether it was counted."""
        if (
            self._started_at is None
            or not self._started_at <= now <= self._started_at + self.interval
        ):
            return False
        self.taps += 1
        return True

    def finish(self, now: float) -> PulseResult:
        if self._started_at is None:
            raise RuntimeError("the count has not started")
        if now < self._started_at + self.interval:
            raise RuntimeError("the time is not up yet")
        bpm = round(self.taps * 60 / self.interval)
        self.result = PulseResult(
            taps=self.taps,
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
        self.taps = 0
        self._started_at = None
        self.station = Station.COUNT

    # --- the game: technique, never the value ----------------------------------------------

    @property
    def points(self) -> int:
        done = sum(1 for step in _STEPS if self._reached(step))
        total = done * STEP_POINTS
        if self._attempted:
            total += ATTEMPT_POINTS
        if self.result is not None and self.result.valid:
            total += MEASUREMENT_BONUS
        return total

    def _reached(self, step: Station) -> bool:
        order = [*_STEPS, Station.COUNT, Station.RESULT]
        return order.index(self.station) > order.index(step)

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
