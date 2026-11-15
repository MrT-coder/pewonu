"""The data intake screen: what came in, from where, and what it shows (A17)."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import status_label_key
from crew_self_check.astronaut.cases import HAZARD_URL
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.intake import FeedDay, Intake, SourceKind, SourceRow, build_intake
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.core.reasons import Language

_ICONS = {
    SourceKind.WEARABLE: ft.Icons.WATCH,
    SourceKind.SURVEY: ft.Icons.FACT_CHECK_OUTLINED,
    SourceKind.HAND_PULSE: ft.Icons.FRONT_HAND_OUTLINED,
    SourceKind.ENTERED: ft.Icons.EDIT_NOTE,
}


def _title(text: str) -> ft.Control:
    return ft.Text(text, size=15, weight=ft.FontWeight.W_600, color=theme.TEXT)


def _source_row(row: SourceRow, language: Language) -> ft.Control:
    names = ", ".join(translate(f"indicator.{i.value}", language) for i in row.indicators)
    return ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=12,
        controls=[
            ft.Icon(_ICONS[row.kind], size=24, color=theme.ACCENT),
            ft.Column(
                spacing=2,
                expand=True,
                controls=[
                    ft.Text(
                        translate(f"intake.source.{row.kind.value}", language),
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=theme.TEXT,
                    ),
                    ft.Text(
                        translate(f"intake.source.{row.kind.value}.what", language),
                        size=12,
                        color=theme.MUTED,
                    ),
                    ft.Text(
                        translate(
                            "intake.readings",
                            language,
                            n=row.readings,
                            last=row.last.strftime("%Y-%m-%d"),
                        ),
                        size=12,
                        color=theme.GOOD,
                    ),
                    ft.Text(names, size=12, color=theme.TEXT),
                ],
            ),
        ],
    )


def _feed_row(entry: FeedDay, language: Language) -> ft.Control:
    parts = [
        f"{count} {translate(f'intake.short.{kind.value}', language)}"
        for kind, count in entry.counts.items()
    ]
    return ft.Row(
        spacing=12,
        controls=[
            ft.Container(
                width=56,
                content=ft.Text(
                    entry.label, size=13, weight=ft.FontWeight.W_600, color=theme.ACCENT
                ),
            ),
            ft.Text(
                translate("intake.feed_line", language, total=entry.total, parts=" · ".join(parts)),
                size=13,
                color=theme.TEXT,
                expand=True,
            ),
        ],
    )


def _shows_now(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    chips: list[ft.Control] = []
    for system, status in state.system_statuses().items():
        level = status.status if status else None
        chips.append(
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                border_radius=16,
                border=ft.Border.all(1, status_color(level)),
                content=ft.Row(
                    spacing=6,
                    tight=True,
                    controls=[
                        ft.Container(
                            width=10,
                            height=10,
                            border_radius=5,
                            bgcolor=status_color(level),
                        ),
                        ft.Text(
                            f"{translate(f'system.{system.value}', language)}: "
                            f"{translate(status_label_key(level), language)}",
                            size=12,
                            color=theme.TEXT,
                        ),
                    ],
                ),
            )
        )
    return card(
        ft.Column(
            spacing=10,
            controls=[
                _title(translate("intake.shows_title", language)),
                ft.Text(translate("intake.shows_body", language), size=12, color=theme.MUTED),
                ft.Row(wrap=True, spacing=8, run_spacing=8, controls=chips),
                ft.OutlinedButton(
                    content=translate("intake.open_body", language),
                    icon=ft.Icons.ACCESSIBILITY_NEW,
                    on_click=lambda _: actions.go(Section.BODY),
                ),
            ],
        )
    )


def _origin(intake: Intake, language: Language) -> ft.Control:
    lines: list[ft.Control] = [
        _title(translate("intake.origin_title", language)),
        ft.Text(
            translate(
                "intake.origin_simulated" if intake.simulated else "intake.origin_other", language
            ),
            size=13,
            color=theme.GOLD if intake.simulated else theme.TEXT,
        ),
        ft.Text(translate("intake.origin_real", language), size=12, color=theme.MUTED),
        ft.Row(
            wrap=True,
            spacing=12,
            controls=[
                ft.Text(translate("hazard.source", language), size=11, color=theme.MUTED),
                ft.TextButton(
                    content=translate("card.source_open", language),
                    url=HAZARD_URL,
                    icon=ft.Icons.OPEN_IN_NEW,
                ),
            ],
        ),
    ]
    return card(ft.Column(spacing=8, controls=lines))


def build_intake_view(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    intake = build_intake(state)
    if intake.total_readings == 0:
        return card(ft.Text(translate("intake.empty", language), size=14, color=theme.MUTED))

    header = card(
        ft.Column(
            spacing=8,
            controls=[
                _title(translate("intake.title", language)),
                ft.Text(translate("intake.intro", language), size=13, color=theme.MUTED),
                ft.Text(
                    translate(
                        "intake.totals",
                        language,
                        n=intake.total_readings,
                        covered=intake.indicators_covered,
                        total=intake.indicators_total,
                    ),
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=theme.GOOD,
                ),
            ],
        )
    )
    sources = card(
        ft.Column(
            spacing=14,
            controls=[
                _title(translate("intake.sources_title", language)),
                *[_source_row(row, language) for row in intake.sources],
            ],
        )
    )
    feed = card(
        ft.Column(
            spacing=8,
            controls=[
                _title(translate("intake.feed_title", language)),
                *[_feed_row(entry, language) for entry in intake.feed],
            ],
        )
    )
    return ft.Column(
        spacing=14,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[header, sources, feed, _shows_now(state, actions), _origin(intake, language)],
    )
