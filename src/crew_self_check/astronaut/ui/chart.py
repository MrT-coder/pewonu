"""The trend chart, drawn with Flet's own canvas (no chart library, so no new dependency)."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft
import flet.canvas as cv

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.chart_layout import layout_series


def trend_chart(
    values: Sequence[float],
    low: float | None,
    high: float | None,
    last_color: str,
    width: float = 460,
    height: float = 150,
) -> ft.Control | None:
    """Readings as a line over the band they are compared with; ``None`` if too few readings."""
    layout = layout_series(values, low, high, width, height)
    if layout is None:
        return None
    shapes: list[cv.Shape] = []
    if layout.band is not None:
        x, y, band_width, band_height = layout.band
        shapes.append(
            cv.Rect(
                x,
                y,
                band_width,
                band_height,
                border_radius=6,
                paint=ft.Paint(
                    color=ft.Colors.with_opacity(0.2, theme.ACCENT), style=ft.PaintingStyle.FILL
                ),
            )
        )
    start, *rest = layout.points
    elements: list[cv.Path.PathElement] = [cv.Path.MoveTo(*start)]
    elements += [cv.Path.LineTo(px, py) for px, py in rest]
    shapes.append(
        cv.Path(
            elements,
            paint=ft.Paint(color=theme.ACCENT, stroke_width=2.5, style=ft.PaintingStyle.STROKE),
        )
    )
    last = len(layout.points) - 1
    for index, (px, py) in enumerate(layout.points):
        shapes.append(
            cv.Circle(
                px,
                py,
                6 if index == last else 3,
                paint=ft.Paint(
                    color=last_color if index == last else theme.ACCENT,
                    style=ft.PaintingStyle.FILL,
                ),
            )
        )
    return cv.Canvas(shapes=shapes, width=width, height=height)
