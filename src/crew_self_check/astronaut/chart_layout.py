"""Geometry of the trend chart: pure numbers, no UI, so it can be tested and drawn by any view.

Readings run left to right, higher values are higher on the screen (smaller ``y``), and the band
(the range a reading is compared with) is a rectangle. The scale always shows both the readings
and the band, so a reading far outside the band is drawn outside it, not squeezed into it.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChartLayout:
    points: tuple[tuple[float, float], ...]  # (x, y) of each reading, oldest first
    band: tuple[float, float, float, float] | None  # (x, y, width, height) of the band


def layout_series(
    values: Sequence[float],
    low: float | None,
    high: float | None,
    width: float,
    height: float,
    padding: float = 12.0,
) -> ChartLayout | None:
    """Place ``values`` in a ``width`` x ``height`` box. ``None`` if there are fewer than two."""
    if len(values) < 2:
        return None
    seen = [*values]
    if low is not None and high is not None:
        seen += [low, high]
    top_value, bottom_value = max(seen), min(seen)
    if top_value == bottom_value:  # a flat series: give the scale some room
        top_value, bottom_value = top_value + 1.0, bottom_value - 1.0
    inner_width, inner_height = width - 2 * padding, height - 2 * padding

    def y_of(value: float) -> float:
        return padding + (top_value - value) / (top_value - bottom_value) * inner_height

    step = inner_width / (len(values) - 1)
    points = tuple((padding + i * step, y_of(v)) for i, v in enumerate(values))
    band = None
    if low is not None and high is not None:
        band_top, band_bottom = y_of(high), y_of(low)
        band = (padding, band_top, inner_width, max(band_bottom - band_top, 2.0))
    return ChartLayout(points, band)
