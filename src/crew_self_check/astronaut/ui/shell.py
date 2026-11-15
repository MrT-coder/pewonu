"""The shell after login: a top bar, the single screen or the hazards, and what floats over them.

UX v2: the body, the journey ring and the data share one screen; the pulse, the mood and voice log,
the share panel and every system open in modals; the mood bubble floats and can be dragged. The
hazards are a second screen. The old sections (Home, Check-in, Summary, Data) are gone: ``Section``
still names them, and any of them shows the single screen.
"""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.bubble import build_bubble
from crew_self_check.astronaut.ui.common import Actions, language_switch
from crew_self_check.astronaut.ui.hazards import build_hazards_view
from crew_self_check.astronaut.ui.modals import modal_overlay
from crew_self_check.astronaut.ui.space import space_background
from crew_self_check.astronaut.ui.stage import build_stage


def _top_bar(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def screen(event: ft.Event[ft.SegmentedButton]) -> None:
        wanted = next(iter(event.control.selected))
        actions.go(Section.HAZARDS if wanted == "hazards" else Section.BODY)

    selected = "hazards" if state.section is Section.HAZARDS else "body"
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
        border_radius=20,
        bgcolor=ft.Colors.with_opacity(0.66, theme.CARD),
        border=ft.Border.all(1, theme.CARD_BORDER),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=16,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Image(src="brand/pewonu.png", height=40, fit=ft.BoxFit.CONTAIN),
                                ft.Text(
                                    translate("app.name", language),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.TEXT,
                                ),
                            ],
                        ),
                        ft.SegmentedButton(
                            selected=[selected],
                            allow_empty_selection=False,
                            segments=[
                                ft.Segment(
                                    value="body",
                                    icon=ft.Icon(ft.Icons.ACCESSIBILITY_NEW),
                                    label=ft.Text(translate("nav.body", language)),
                                ),
                                ft.Segment(
                                    value="hazards",
                                    icon=ft.Icon(ft.Icons.WARNING_AMBER),
                                    label=ft.Text(translate("nav.hazards", language)),
                                ),
                            ],
                            on_change=screen,
                        ),
                    ],
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                            border_radius=20,
                            bgcolor=theme.ACCENT_SOFT,
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=theme.ACCENT),
                                    ft.Text(state.code or "", size=13, color=theme.ACCENT),
                                ],
                            ),
                        ),
                        language_switch(state, actions),
                        ft.IconButton(
                            icon=ft.Icons.MENU_BOOK_OUTLINED,
                            tooltip=translate("nav.glossary", language),
                            on_click=lambda _: actions.show_glossary(),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.INFO_OUTLINE,
                            tooltip=translate("nav.limits", language),
                            on_click=lambda _: actions.show_limits(),
                        ),
                        ft.OutlinedButton(
                            content=translate("nav.logout", language),
                            icon=ft.Icons.LOGOUT,
                            on_click=lambda _: actions.logout(),
                        ),
                    ],
                ),
            ],
        ),
    )


def build_shell(state: AppState, actions: Actions) -> ft.Control:
    screen = (
        build_hazards_view(state, actions)
        if state.section is Section.HAZARDS
        else build_stage(state, actions)
    )
    page = ft.Column(
        expand=True,
        spacing=12,
        controls=[
            _top_bar(state, actions),
            ft.Container(
                expand=True,
                content=ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[screen])
                if state.section is Section.HAZARDS
                else screen,
            ),
        ],
    )
    layers: list[ft.Control] = [
        ft.Container(expand=True, padding=16, content=page),
        build_bubble(state, actions),
    ]
    overlay = modal_overlay(state, actions)
    if overlay is not None:
        layers.append(overlay)
    return space_background(ft.Stack(expand=True, controls=layers))
