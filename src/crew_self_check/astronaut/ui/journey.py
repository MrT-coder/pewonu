"""The journey bar: where the simulated mission is (Earth, spacecraft, planet) and a day control."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, card


def journey_bar(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    day = state.current_day
    last = len(state.scenario.days) - 1
    place = translate(f"env.{day.environment.value}", language)

    def moved(event: ft.Event[ft.Slider]) -> None:
        actions.set_day(int(event.control.value or 0))

    return card(
        ft.Column(
            spacing=6,
            controls=[
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.PUBLIC, size=22, color=theme.ACCENT),
                        ft.Text(
                            translate("journey.title", language),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT,
                        ),
                        ft.Text(
                            translate("journey.day", language, label=day.label, place=place),
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=theme.ACCENT,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_LEFT,
                            tooltip=translate("journey.previous", language),
                            disabled=state.journey_day == 0,
                            on_click=lambda _: actions.set_day(state.journey_day - 1),
                        ),
                        ft.Slider(
                            min=0,
                            max=last,
                            divisions=last,
                            value=state.journey_day,
                            expand=True,
                            on_change_end=moved,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_RIGHT,
                            tooltip=translate("journey.next", language),
                            disabled=state.journey_day == last,
                            on_click=lambda _: actions.set_day(state.journey_day + 1),
                        ),
                    ],
                ),
                ft.Text(translate("journey.note", language), size=11, color=theme.MUTED),
            ],
        ),
        padding=12,
    )
