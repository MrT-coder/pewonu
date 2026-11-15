"""The space backdrop: a deep gradient, two soft nebulae and a field of stars (UX v2).

Drawn once with the canvas: fixed stars (the same sky every run) so nothing here needs a timer.
"""

from __future__ import annotations

import random

import flet as ft
import flet.canvas as cv

from crew_self_check.astronaut import theme

_SKY_WIDTH, _SKY_HEIGHT = 2000, 1200


def _stars() -> list[cv.Shape]:
    rng = random.Random(7)
    shapes: list[cv.Shape] = []
    for _ in range(190):
        radius = rng.choice((0.6, 0.8, 1.0, 1.2, 1.6))
        color = ft.Colors.with_opacity(rng.uniform(0.25, 0.95), "#cfe3ff")
        shapes.append(
            cv.Circle(
                rng.uniform(0, _SKY_WIDTH),
                rng.uniform(0, _SKY_HEIGHT),
                radius,
                ft.Paint(color=color, style=ft.PaintingStyle.FILL),
            )
        )
    return shapes


_STARS = _stars()


def _nebula(
    color: str,
    size: int,
    left: int | None = None,
    top: int | None = None,
    right: int | None = None,
    bottom: int | None = None,
) -> ft.Control:
    return ft.Container(
        width=size,
        height=size,
        border_radius=size // 2,
        gradient=ft.RadialGradient(
            colors=[ft.Colors.with_opacity(0.22, color), ft.Colors.with_opacity(0.0, color)]
        ),
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )


def space_background(content: ft.Control) -> ft.Control:
    """``content`` over the sky. It fills the page."""
    return ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[theme.BG_TOP, theme.BG_BOTTOM],
                ),
            ),
            _nebula("#38bdf8", 900, left=-260, top=-300),
            _nebula("#7c3aed", 800, right=-260, bottom=-280),
            cv.Canvas(shapes=_STARS, expand=True),
            content,
        ],
    )
