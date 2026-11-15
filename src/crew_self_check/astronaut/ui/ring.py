"""The mission ring: Earth, spacecraft and the planet as three arcs of one circle (UX v2).

A marker rides the ring as the simulated day advances, with the icon of where the crew is: a globe
on Earth, a rocket in the spacecraft and a red planet on arrival. Tapping the ring jumps to that
day. Nothing here changes a state: it only moves the journey clock (``actions.set_day``).
"""

from __future__ import annotations

import asyncio
import math

import flet as ft
import flet.canvas as cv

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, card
from crew_self_check.core.contract import Environment

_SIZE = 240
_CENTER = _SIZE / 2
_RADIUS = 100
_MARKER = 44
_COLORS = {
    Environment.EARTH: "#38bdf8",
    Environment.SPACECRAFT: "#a78bfa",
    Environment.PLANET: "#fb923c",
}
_STEP_SECONDS = 0.9


def place_icon(environment: Environment, size: int) -> ft.Control:
    """A globe, a rocket or a red planet: the same three icons wherever the place is shown."""
    if environment is Environment.EARTH:
        return ft.Icon(ft.Icons.PUBLIC, size=size, color=_COLORS[environment])
    if environment is Environment.SPACECRAFT:
        return ft.Icon(ft.Icons.ROCKET_LAUNCH, size=size, color=_COLORS[environment])
    return ft.Container(
        width=size,
        height=size,
        border_radius=size // 2,
        gradient=ft.RadialGradient(
            center=ft.Alignment(-0.35, -0.4), colors=["#ffb089", "#e2582b", "#8a2e14"]
        ),
    )


def _angle(day: int, total: int) -> float:
    """The middle of ``day`` on the ring, in radians from 3 o'clock, starting at the top."""
    return (day + 0.5) / total * 2 * math.pi - math.pi / 2


def _arcs(state: AppState) -> list[cv.Shape]:
    days = state.scenario.days
    total = len(days)
    shapes: list[cv.Shape] = [
        cv.Circle(
            _CENTER,
            _CENTER,
            _RADIUS,
            ft.Paint(color="#0e1d38", style=ft.PaintingStyle.STROKE, stroke_width=22),
        )
    ]
    start = 0
    for index in range(1, total + 1):
        if index < total and days[index].environment is days[start].environment:
            continue
        sweep = (index - start) / total * 2 * math.pi
        shapes.append(
            cv.Arc(
                _CENTER - _RADIUS,
                _CENTER - _RADIUS,
                _RADIUS * 2,
                _RADIUS * 2,
                start_angle=-math.pi / 2 + start / total * 2 * math.pi + 0.02,
                sweep_angle=sweep - 0.04,
                use_center=False,
                paint=ft.Paint(
                    color=_COLORS[days[start].environment],
                    style=ft.PaintingStyle.STROKE,
                    stroke_width=14,
                    stroke_cap=ft.StrokeCap.ROUND,
                ),
            )
        )
        start = index
    return shapes


def _day_at(state: AppState, x: float, y: float) -> int:
    total = len(state.scenario.days)
    turn = (math.atan2(y - _CENTER, x - _CENTER) + math.pi / 2) % (2 * math.pi)
    return min(total - 1, int(turn / (2 * math.pi) * total))


def build_ring(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    day = state.current_day
    total = len(state.scenario.days)
    angle = _angle(state.journey_day, total)
    place = translate(f"env.{day.environment.value}.short", language)

    marker = ft.Container(
        left=_CENTER + _RADIUS * math.cos(angle) - _MARKER / 2,
        top=_CENTER + _RADIUS * math.sin(angle) - _MARKER / 2,
        width=_MARKER,
        height=_MARKER,
        border_radius=_MARKER // 2,
        bgcolor="#0a1730",
        border=ft.Border.all(2, "#ffffff"),
        alignment=ft.Alignment.CENTER,
        content=place_icon(day.environment, 24),
        shadow=ft.BoxShadow(blur_radius=22, color=ft.Colors.with_opacity(0.55, "#ffffff")),
        animate_position=ft.Animation(550, ft.AnimationCurve.EASE_IN_OUT),
    )
    center = ft.Container(
        left=0,
        top=0,
        width=_SIZE,
        height=_SIZE,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            tight=True,
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                place_icon(day.environment, 36),
                ft.Text(day.label, size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                ft.Text(place, size=12, color=theme.MUTED),
            ],
        ),
    )

    def jump(event: ft.TapEvent[ft.GestureDetector]) -> None:
        position = event.local_position
        if position is not None:
            actions.set_day(_day_at(state, position.x, position.y))

    ring = ft.GestureDetector(
        on_tap_down=jump,
        content=ft.Stack(
            width=_SIZE,
            height=_SIZE,
            controls=[cv.Canvas(width=_SIZE, height=_SIZE, shapes=_arcs(state)), center, marker],
        ),
    )

    last = total - 1

    async def play_loop() -> None:
        while state.journey_playing and state.journey_day < last:
            await asyncio.sleep(_STEP_SECONDS)
            if not state.journey_playing:
                return
            actions.set_day(state.journey_day + 1)
        state.journey_playing = False
        actions.rerender()

    def toggle(_: object) -> None:
        state.journey_playing = not state.journey_playing
        if state.journey_playing:
            if state.journey_day >= last:
                state.set_day(0)
            actions.run_task(play_loop)
        actions.rerender()

    legend = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        spacing=12,
        controls=[
            ft.Row(
                spacing=4,
                tight=True,
                controls=[
                    place_icon(environment, 14),
                    ft.Text(
                        translate(f"env.{environment.value}.short", language),
                        size=11,
                        color=theme.MUTED,
                    ),
                ],
            )
            for environment in Environment
        ],
    )
    return card(
        ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    translate("journey.title", language),
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=theme.MUTED,
                ),
                ring,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_LEFT,
                            tooltip=translate("journey.previous", language),
                            disabled=state.journey_day == 0,
                            on_click=lambda _: actions.set_day(state.journey_day - 1),
                        ),
                        ft.OutlinedButton(
                            content=translate(
                                "journey.pause" if state.journey_playing else "journey.play",
                                language,
                            ),
                            icon=ft.Icons.PAUSE if state.journey_playing else ft.Icons.PLAY_ARROW,
                            on_click=toggle,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_RIGHT,
                            tooltip=translate("journey.next", language),
                            disabled=state.journey_day == last,
                            on_click=lambda _: actions.set_day(state.journey_day + 1),
                        ),
                    ],
                ),
                legend,
            ],
        )
    )
