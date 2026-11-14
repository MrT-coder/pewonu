"""The summary per astronaut: a few human numbers, what needs attention and the latest readings."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import format_reading, reference_text, status_label_key
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.summary_model import Summary, build_summary
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.astronaut.ui.share import build_share_panel
from crew_self_check.astronaut.ui.system_card import status_chip
from crew_self_check.core.contract import Status
from crew_self_check.core.status import IndicatorResolution


def _tile(title: str, controls: list[ft.Control]) -> ft.Control:
    return card(
        ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, size=13, weight=ft.FontWeight.W_600, color=theme.MUTED),
                *controls,
            ],
        )
    )


def _count_chip(count: int, label: str, color: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
        border=ft.Border.all(1, color),
        content=ft.Row(
            tight=True,
            spacing=6,
            controls=[
                ft.Container(width=10, height=10, border_radius=5, bgcolor=color),
                ft.Text(f"{count}", size=14, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                ft.Text(label, size=12, color=theme.MUTED),
            ],
        ),
    )


def _kpis(state: AppState, summary: Summary) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    counts = summary.counts
    systems = _tile(
        say("summary.systems"),
        [
            ft.Row(
                wrap=True,
                spacing=6,
                run_spacing=6,
                controls=[
                    _count_chip(counts.ok, say("summary.short.ok"), status_color(Status.OK)),
                    _count_chip(
                        counts.watch, say("summary.short.watch"), status_color(Status.WATCH)
                    ),
                    _count_chip(counts.act, say("summary.short.act"), status_color(Status.ACT)),
                    _count_chip(
                        counts.gray,
                        say("summary.short.insufficient_data"),
                        status_color(Status.INSUFFICIENT_DATA),
                    ),
                    _count_chip(counts.nothing, say("summary.short.nothing"), status_color(None)),
                ],
            )
        ],
    )

    def done(flag: bool, yes: str, no: str) -> ft.Control:
        return ft.Row(
            spacing=6,
            controls=[
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if flag else ft.Icons.RADIO_BUTTON_UNCHECKED,
                    size=18,
                    color=theme.GOOD if flag else theme.MUTED,
                ),
                ft.Text(say(yes if flag else no), size=13, color=theme.TEXT),
            ],
        )

    checkin = _tile(
        say("summary.checkin"),
        [
            done(summary.checked_in.pulse, "summary.pulse_done", "summary.pulse_todo"),
            done(summary.checked_in.mood, "summary.mood_done", "summary.mood_todo"),
        ],
    )
    regularity = _tile(
        say("summary.regularity"),
        [
            ft.Text(
                say("summary.days", n=summary.days_measured),
                size=18,
                weight=ft.FontWeight.BOLD,
                color=theme.TEXT,
            ),
            ft.Text(say("summary.regularity_note"), size=12, color=theme.MUTED),
        ],
    )
    baseline = summary.baseline
    baseline_text = (
        say("summary.baseline_value", ready=baseline.ready, total=baseline.total)
        if baseline.total
        else say("summary.baseline_none")
    )
    knows = _tile(
        say("summary.baseline"),
        [
            ft.Text(baseline_text, size=16, weight=ft.FontWeight.BOLD, color=theme.TEXT),
            ft.Text(say("summary.baseline_note"), size=12, color=theme.MUTED),
        ],
    )
    return ft.ResponsiveRow(
        spacing=14,
        run_spacing=14,
        controls=[
            ft.Container(content=tile, col={"xs": 12, "md": 6, "xl": 3})
            for tile in (systems, checkin, regularity, knows)
        ],
    )


def _attention(state: AppState, summary: Summary, actions: Actions) -> ft.Control:
    language = state.language
    lines: list[ft.Control] = [
        ft.Text(
            translate("summary.attention", language),
            size=16,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
        )
    ]
    if not summary.attention:
        lines.append(
            ft.Text(translate("summary.attention_none", language), size=13, color=theme.MUTED)
        )
    for item in summary.attention:
        lines.append(_attention_item(state, item))
    lines.append(
        ft.TextButton(
            content=translate("summary.open_body", language),
            icon=ft.Icons.ACCESSIBILITY_NEW,
            on_click=lambda _: actions.go(Section.BODY),
        )
    )
    return card(ft.Column(spacing=10, controls=lines))


def _attention_item(state: AppState, item: IndicatorResolution) -> ft.Control:
    language = state.language
    status = item.status
    unit = next(
        (m.unit for m in reversed(state.visible_measurements()) if m.indicator is status.indicator),
        "",
    )
    latest = (
        format_reading(status.indicator, status.latest, unit, language)
        if status.latest is not None
        else ""
    )
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=6),
        content=ft.Column(
            spacing=3,
            controls=[
                ft.Row(
                    wrap=True,
                    spacing=10,
                    controls=[
                        ft.Text(
                            translate(f"indicator.{status.indicator.value}", language),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT,
                        ),
                        ft.Text(latest, size=14, color=theme.ACCENT),
                        status_chip(
                            status.status, translate(status_label_key(status.status), language)
                        ),
                    ],
                ),
                ft.Text(item.reason.text(language), size=12, color=theme.MUTED),
                ft.Text(
                    translate(f"escalation.{status.escalation.value}", language),
                    size=12,
                    color=theme.TEXT,
                ),
            ],
        ),
    )


def _latest(state: AppState, summary: Summary) -> ft.Control:
    language = state.language

    def header(key: str, width: int | None = None) -> ft.Control:
        return ft.Container(
            width=width,
            expand=width is None,
            content=ft.Text(
                translate(key, language), size=12, weight=ft.FontWeight.W_600, color=theme.MUTED
            ),
        )

    rows: list[ft.Control] = [
        ft.Text(
            translate("summary.latest", language),
            size=16,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
        ),
        ft.Row(
            controls=[
                header("summary.col.indicator", 240),
                header("summary.col.latest", 130),
                header("summary.col.state", 150),
                header("summary.col.compared"),
            ]
        ),
        ft.Divider(height=1, color=theme.CARD_BORDER),
    ]
    for row in summary.rows:
        status = row.status
        rows.append(
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        width=240,
                        content=ft.Text(
                            translate(f"indicator.{row.indicator.value}", language),
                            size=13,
                            color=theme.TEXT,
                        ),
                    ),
                    ft.Container(
                        width=130,
                        content=ft.Text(
                            format_reading(row.indicator, row.value, row.unit, language),
                            size=13,
                            color=theme.ACCENT,
                        ),
                    ),
                    ft.Container(
                        width=150,
                        content=ft.Row(
                            tight=True,
                            spacing=6,
                            controls=[
                                ft.Container(
                                    width=10,
                                    height=10,
                                    border_radius=5,
                                    bgcolor=status_color(status.status),
                                ),
                                ft.Text(
                                    translate(f"summary.short.{status.status.value}", language),
                                    size=12,
                                    color=theme.TEXT,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Text(
                            reference_text(status, language), size=12, color=theme.MUTED
                        ),
                    ),
                ],
            )
        )
    return card(ft.Column(spacing=8, controls=rows))


def build_summary_view(state: AppState, actions: Actions) -> ft.Control:
    summary = build_summary(state)
    return ft.Column(
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            _kpis(state, summary),
            _attention(state, summary, actions),
            _latest(state, summary),
            build_share_panel(state, summary, actions),
        ],
    )
