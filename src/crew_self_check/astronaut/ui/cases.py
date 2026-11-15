"""Presentation of the three demo cases: a list on the login screen and a card on the home."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.cases import HAZARD_URL, case_for
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.ui.common import card
from crew_self_check.core.reasons import Language


def case_card(language: Language, crew_id: str) -> ft.Control | None:
    """What this demo astronaut is about, the NASA hazard it stresses and how the system copes."""
    case = case_for(crew_id)
    if case is None:
        return None

    def say(key: str) -> str:
        return translate(key, language)

    return card(
        ft.Column(
            spacing=8,
            controls=[
                ft.Text(say("case.your_case"), size=12, color=theme.MUTED),
                ft.Text(say(case.title_key), size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                ft.Text(say(case.story_key), size=13, color=theme.TEXT),
                ft.Text(
                    say("case.hazard_label"), size=12, weight=ft.FontWeight.W_600, color=theme.GOLD
                ),
                ft.Text(
                    say(f"hazard.{case.hazard.value}"),
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=theme.TEXT,
                ),
                ft.Text(say(f"hazard.{case.hazard.value}.what"), size=12, color=theme.MUTED),
                ft.Text(
                    say("case.system_label"),
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=theme.ACCENT,
                ),
                ft.Text(say(case.system_key), size=13, color=theme.TEXT),
                ft.Row(
                    wrap=True,
                    spacing=12,
                    controls=[
                        ft.Text(say("hazard.source"), size=11, color=theme.MUTED),
                        ft.TextButton(
                            content=say("card.source_open"),
                            url=HAZARD_URL,
                            icon=ft.Icons.OPEN_IN_NEW,
                        ),
                    ],
                ),
                ft.Text(say("case.simulated"), size=11, color=theme.MUTED),
            ],
        ),
        border_color=theme.ACCENT,
    )


def demo_case_rows(
    language: Language, pairs: tuple[tuple[str, str], ...], pick: Callable[[str], None]
) -> list[ft.Control]:
    """One tappable row per demo code: the code, the case and the hazard it stresses."""
    rows: list[ft.Control] = []
    for code, crew_id in pairs:
        case = case_for(crew_id)
        if case is None:
            continue
        label = (
            f"{code} · {translate(case.title_key, language)}"
            f" · {translate(f'hazard.{case.hazard.value}', language)}"
        )
        rows.append(
            ft.TextButton(content=label, on_click=lambda _, c=code: pick(c), icon=ft.Icons.PERSON)
        )
    return rows
