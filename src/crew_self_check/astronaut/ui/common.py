"""Pieces shared by the views: actions, cards, background, language switch, limits dialog."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import GLOSSARY, translate
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.core.reasons import Language


@dataclass(frozen=True, slots=True)
class Actions:
    """What a view can ask the app to do. Views never touch the page directly."""

    login: Callable[[str], bool]
    set_language: Callable[[Language], None]
    go: Callable[[Section], None]
    logout: Callable[[], None]
    show_limits: Callable[[], None]
    show_glossary: Callable[[], None]
    refresh: Callable[[], None]  # push control changes to the screen
    rerender: Callable[[], None]  # rebuild the whole view from the state


def cabin_background(content: ft.Control) -> ft.Container:
    return ft.Container(
        content=content,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=[theme.BG_TOP, theme.BG_BOTTOM],
        ),
    )


def card(
    content: ft.Control, *, padding: int = 20, border_color: str = theme.CARD_BORDER
) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=theme.CARD,
        border=ft.Border.all(1, border_color),
        border_radius=16,
    )


def language_switch(state: AppState, actions: Actions) -> ft.SegmentedButton:
    def changed(event: ft.Event[ft.SegmentedButton]) -> None:
        chosen = next(iter(event.control.selected), Language.EN.value)
        actions.set_language(Language(chosen))

    return ft.SegmentedButton(
        selected=[state.language.value],
        allow_empty_selection=False,
        segments=[
            ft.Segment(value=Language.EN.value, label=ft.Text("English")),
            ft.Segment(value=Language.ES.value, label=ft.Text("Español")),
        ],
        on_change=changed,
    )


def limits_dialog(language: Language, close: Callable[[], None]) -> ft.AlertDialog:
    """Shown from every screen (A9): analog data, nothing validated, no diagnosis."""
    return ft.AlertDialog(
        title=ft.Text(translate("limits.title", language)),
        content=ft.Container(width=460, content=ft.Text(translate("limits.body", language))),
        actions=[
            ft.TextButton(content=translate("limits.close", language), on_click=lambda _: close())
        ],
    )


def glossary_dialog(language: Language, close: Callable[[], None]) -> ft.AlertDialog:
    """Every acronym the app shows, spelled out. Reachable from every screen (D-024)."""
    rows: list[ft.Control] = []
    for entry in GLOSSARY:
        term, meaning = entry[language]
        rows.append(
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(term, size=15, weight=ft.FontWeight.BOLD, color=theme.ACCENT),
                    ft.Text(meaning, size=13, color=theme.TEXT),
                ],
            )
        )
    return ft.AlertDialog(
        title=ft.Text(translate("nav.glossary", language)),
        content=ft.Container(width=460, content=ft.Column(spacing=12, tight=True, controls=rows)),
        actions=[
            ft.TextButton(content=translate("glossary.close", language), on_click=lambda _: close())
        ],
    )
