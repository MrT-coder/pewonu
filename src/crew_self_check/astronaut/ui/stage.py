"""The single screen: the body in the middle, the journey on one side and the data on the other."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.cases import case_card
from crew_self_check.astronaut.ui.common import Actions
from crew_self_check.astronaut.ui.data_panel import build_data_panel
from crew_self_check.astronaut.ui.figure import STAGE_HEIGHT, STAGE_WIDTH, build_figure
from crew_self_check.astronaut.ui.pewonu import build_pillars
from crew_self_check.astronaut.ui.ring import build_ring

_SIDE_LEFT = 290
_SIDE_RIGHT = 360


def build_stage(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    case = case_card(language, state.profile.crew_id) if state.profile else None
    left = ft.Column(
        width=_SIDE_LEFT,
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            build_ring(state, actions),
            build_pillars(state, actions),
            *([case] if case is not None else []),
        ],
    )
    center = ft.Container(
        expand=True,
        alignment=ft.Alignment.TOP_CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=6,
            controls=[
                ft.Container(
                    width=STAGE_WIDTH, height=STAGE_HEIGHT, content=build_figure(state, actions)
                ),
                ft.Text(translate("stage.hint", language), size=12, color=theme.MUTED),
            ],
        ),
    )
    right = ft.Container(width=_SIDE_RIGHT, content=build_data_panel(state, actions))
    return ft.Row(
        expand=True,
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[left, center, right],
    )
