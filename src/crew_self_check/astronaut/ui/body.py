"""The body view: a figure whose zones are colored by the calculated state of each system (A3)."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import status_label_key
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.astronaut.ui.system_card import build_system_card
from crew_self_check.core.contract import Status, System, SystemStatus

_FIGURE_WIDTH = 380
_FIGURE_HEIGHT = 520

# System, center of its badge on the figure, and its icon. The silhouette is a standing person.
_ZONES: tuple[tuple[System, int, int, ft.IconData], ...] = (
    (System.SLEEP_BRAIN, 190, 52, ft.Icons.PSYCHOLOGY),
    (System.VESTIBULAR, 78, 118, ft.Icons.HEARING),
    (System.MOOD, 302, 118, ft.Icons.SENTIMENT_SATISFIED_ALT),
    (System.CARDIOVASCULAR, 190, 215, ft.Icons.FAVORITE),
    (System.IMMUNE, 190, 320, ft.Icons.SHIELD_OUTLINED),
    (System.BONE_MUSCLE, 190, 440, ft.Icons.FITNESS_CENTER),
)

# The legend, in the order a person reads it: the three states, gray, and "nothing measured".
_LEGEND: tuple[Status | None, ...] = (
    Status.OK,
    Status.WATCH,
    Status.ACT,
    Status.INSUFFICIENT_DATA,
    None,
)


def _zone(
    state: AppState,
    actions: Actions,
    system: System,
    center: tuple[int, int],
    icon: ft.IconData,
    system_status: SystemStatus | None,
) -> ft.Control:
    selected = state.selected_system is system
    status = system_status.status if system_status else None
    color = status_color(status)
    cx, cy = center

    def pick(_: object) -> None:
        actions.select_system(None if selected else system)

    return ft.Container(
        left=cx - 62,
        top=cy - 36,
        width=124,
        ink=True,
        border_radius=12,
        on_click=pick,
        tooltip=translate(status_label_key(status), state.language),
        content=ft.Column(
            tight=True,
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=64,
                    height=64,
                    border_radius=32,
                    bgcolor=color,
                    alignment=ft.Alignment.CENTER,
                    border=ft.Border.all(
                        4 if selected else 1, "#ffffff" if selected else theme.BG_TOP
                    ),
                    content=ft.Icon(icon, size=30, color="#04070d"),
                ),
                ft.Text(
                    translate(f"system.{system.value}", state.language),
                    size=11,
                    text_align=ft.TextAlign.CENTER,
                    color=theme.TEXT if selected else theme.MUTED,
                    weight=ft.FontWeight.W_600 if selected else ft.FontWeight.NORMAL,
                ),
            ],
        ),
    )


def _figure(
    state: AppState, actions: Actions, statuses: dict[System, SystemStatus | None]
) -> ft.Control:
    silhouette = ft.Container(
        left=(_FIGURE_WIDTH - 480) // 2,
        top=0,
        content=ft.Icon(ft.Icons.ACCESSIBILITY_NEW, size=480, color=theme.CARD_BORDER),
    )
    zones = [
        _zone(state, actions, system, (x, y), icon, statuses.get(system))
        for system, x, y, icon in _ZONES
    ]
    return ft.Stack(width=_FIGURE_WIDTH, height=_FIGURE_HEIGHT, controls=[silhouette, *zones])


def _legend(state: AppState) -> ft.Control:
    language = state.language
    rows: list[ft.Control] = [
        ft.Text(
            translate("body.legend", language),
            size=14,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
        )
    ]
    for status in _LEGEND:
        rows.append(
            ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        width=14, height=14, border_radius=7, bgcolor=status_color(status)
                    ),
                    ft.Text(
                        translate(status_label_key(status), language), size=13, color=theme.TEXT
                    ),
                ],
            )
        )
    rows.append(ft.Text(translate("body.colors_note", language), size=12, color=theme.MUTED))
    return card(ft.Column(spacing=8, controls=rows))


def build_body(state: AppState, actions: Actions) -> ft.Control:
    statuses = state.system_statuses()
    right: list[ft.Control] = []
    if state.selected_system is None:
        right.append(ft.Text(translate("body.hint", state.language), size=15, color=theme.MUTED))
    else:
        system = state.selected_system
        right.append(build_system_card(state, system, statuses.get(system), state.resolutions()))
    right.append(_legend(state))
    return ft.Row(
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            card(_figure(state, actions, statuses), padding=10),
            ft.Column(expand=True, spacing=14, scroll=ft.ScrollMode.AUTO, controls=right),
        ],
    )
