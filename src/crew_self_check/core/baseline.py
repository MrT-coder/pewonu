"""Per-person baseline engine (D-013).

For one person, one indicator and one environment (``earth``, ``spacecraft``, ``planet``):

- The baseline is the median of the history with a robust band (median +- k * scaled MAD).
- The last ``sustained`` readings are judged against it and are *not* part of it, so a recent shift
  cannot widen its own band.
- ``insufficient_data`` until the baseline covers ``min_days`` distinct days (D-013: every new
  environment starts gray). ``watch`` when the last ``sustained`` readings are all outside the band,
  on the same side. Otherwise ``ok``.

Out of scope here (C4): red, the ``reference`` (personal, transition, population), the reason text,
the escalation and stale readings. Defaults are [SUPOSICION]: they are statistical conventions, not
clinical thresholds, and the team can tune them in ``BaselineConfig``.
"""

from __future__ import annotations

import math
import statistics
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from crew_self_check.core.contract import (
    Baseline,
    Environment,
    Indicator,
    Measurement,
    Status,
    TrendPoint,
)

# Scales the MAD to match the standard deviation of a normal distribution.
_MAD_SCALE = 1.4826


class Direction(StrEnum):
    ABOVE = "above"
    BELOW = "below"


@dataclass(frozen=True, slots=True)
class BaselineConfig:
    min_days: int = 5  # distinct days of history before the baseline counts
    sustained: int = 3  # consecutive recent readings outside the band to raise ``watch``
    band_k: float = 2.5  # half width of the band, in scaled MADs

    def __post_init__(self) -> None:
        if self.min_days < 1:
            raise ValueError("min_days must be at least 1")
        if self.sustained < 1:
            raise ValueError("sustained must be at least 1")
        if not math.isfinite(self.band_k) or self.band_k <= 0:
            raise ValueError("band_k must be a positive finite number")


DEFAULT_CONFIG = BaselineConfig()


@dataclass(frozen=True, slots=True)
class BaselineAssessment:
    status: Status  # ``ok``, ``watch`` or ``insufficient_data``
    baseline: Baseline | None
    latest: float | None
    recent: tuple[TrendPoint, ...]
    direction: Direction | None  # only set with ``watch``


def _build_baseline(history: list[Measurement], config: BaselineConfig) -> Baseline | None:
    n_days = len({m.timestamp.date() for m in history})
    if n_days < config.min_days:
        return None
    values = [m.value for m in history]
    center = statistics.median(values)
    mad = statistics.median(abs(v - center) for v in values) * _MAD_SCALE
    half = config.band_k * mad
    return Baseline(center=center, low=center - half, high=center + half, n_days=n_days)


def _sustained_direction(
    recent: list[Measurement], baseline: Baseline, need: int
) -> Direction | None:
    if len(recent) < need:
        return None
    if all(m.value > baseline.high for m in recent):
        return Direction.ABOVE
    if all(m.value < baseline.low for m in recent):
        return Direction.BELOW
    return None


def assess(
    measurements: Iterable[Measurement],
    crew_id: str,
    indicator: Indicator,
    environment: Environment,
    config: BaselineConfig = DEFAULT_CONFIG,
) -> BaselineAssessment:
    """Assess one person's indicator in one environment from their readings."""
    series = sorted(
        (
            m
            for m in measurements
            if m.crew_id == crew_id and m.indicator is indicator and m.environment is environment
        ),
        key=lambda m: m.timestamp,
    )
    recent = series[-config.sustained :]
    history = series[: -config.sustained]
    trend = tuple(TrendPoint(m.timestamp, m.value) for m in recent)
    latest = series[-1].value if series else None

    baseline = _build_baseline(history, config)
    if baseline is None:
        return BaselineAssessment(Status.INSUFFICIENT_DATA, None, latest, trend, None)

    direction = _sustained_direction(recent, baseline, config.sustained)
    status = Status.OK if direction is None else Status.WATCH
    return BaselineAssessment(status, baseline, latest, trend, direction)
