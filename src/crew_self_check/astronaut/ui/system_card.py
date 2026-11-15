"""The card of one body system: what it shows, how it is doing, why, and what to do (A4).

Everything on it is educational and comes with its source. There is no diagnosis, no dose and no
clinical step: the color is a comparison and the suggestion only says who could be told.
"""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import (
    chart_series,
    format_reading,
    reference_text,
    status_label_key,
)
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.chart import trend_chart
from crew_self_check.astronaut.ui.common import card, status_color
from crew_self_check.core.contract import Indicator, Status, System, SystemStatus
from crew_self_check.core.status import SYSTEM_INDICATORS, IndicatorResolution, escalation_for

HRP_RISKS_URL = "https://www.nasa.gov/hrp/risks/"
_SEVERITY = {Status.OK: 0, Status.WATCH: 1, Status.ACT: 2}


def status_chip(status: Status | None, label: str) -> ft.Control:
    color = status_color(status)
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
        border=ft.Border.all(1, color),
        content=ft.Row(
            tight=True,
            spacing=6,
            controls=[
                ft.Container(width=10, height=10, border_radius=5, bgcolor=color),
                ft.Text(label, size=12, color=theme.TEXT),
            ],
        ),
    )


def _driver(
    indicators: tuple[Indicator, ...], resolutions: dict[Indicator, IndicatorResolution]
) -> Indicator | None:
    """The indicator that explains the system's color: the worst one that has a state."""
    with_state = [i for i in indicators if resolutions[i].status.status in _SEVERITY]
    return max(with_state, key=lambda i: _SEVERITY[resolutions[i].status.status], default=None)


def build_system_card(
    state: AppState,
    system: System,
    system_status: SystemStatus | None,
    resolutions: dict[Indicator, IndicatorResolution],
) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    status = system_status.status if system_status else None
    indicators = SYSTEM_INDICATORS[system]
    lines: list[ft.Control] = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    say(f"system.{system.value}"),
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT,
                ),
                status_chip(status, say(status_label_key(status))),
            ],
        ),
        ft.Text(say(f"system.{system.value}.what"), size=13, color=theme.MUTED),
    ]

    driver = _driver(indicators, resolutions) if indicators else None
    if driver is not None:
        reference = reference_text(resolutions[driver].status, language)
        lines.append(ft.Text(say("card.compared", what=reference), size=13, color=theme.ACCENT))

    if indicators:
        lines.append(
            ft.Text(say("card.indicators"), size=14, weight=ft.FontWeight.W_600, color=theme.TEXT)
        )
        for indicator in indicators:
            lines.append(_indicator_row(state, indicator, resolutions[indicator]))
        lines += _trend(state, indicators, resolutions, driver)

    suggestion = escalation_for(status) if status is not None else escalation_for(Status.OK)
    lines += [
        ft.Divider(height=8, color=theme.CARD_BORDER),
        ft.Text(say("card.suggestion"), size=14, weight=ft.FontWeight.W_600, color=theme.TEXT),
        ft.Text(say(f"escalation.{suggestion.value}"), size=13, color=theme.TEXT),
        ft.Text(say("card.nothing_sent"), size=12, color=theme.MUTED),
    ]
    if indicators:
        lines.append(
            ft.Text(say("card.what_to_do"), size=14, weight=ft.FontWeight.W_600, color=theme.TEXT)
        )
        todo = ["card.todo.measure", "card.todo.read"]
        if status in (Status.WATCH, Status.ACT):
            todo.append("card.todo.escalate")
        lines += [
            ft.Row(
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text("•", size=13, color=theme.MUTED),
                    ft.Text(say(key), size=13, color=theme.MUTED, expand=True),
                ],
            )
            for key in todo
        ]

    lines += [
        ft.Divider(height=8, color=theme.CARD_BORDER),
        ft.Text(say(f"system.{system.value}.why"), size=13, color=theme.TEXT),
        ft.Text(say("card.source"), size=12, color=theme.MUTED),
        ft.TextButton(
            content=say("card.source_open"), icon=ft.Icons.OPEN_IN_NEW, url=HRP_RISKS_URL
        ),
    ]
    return card(ft.Column(spacing=10, controls=lines), border_color=status_color(status))


def _indicator_row(
    state: AppState,
    indicator: Indicator,
    resolution: IndicatorResolution,
) -> ft.Control:
    language = state.language
    status = resolution.status
    unit = next(
        (m.unit for m in reversed(state.visible_measurements()) if m.indicator is indicator), ""
    )
    latest = (
        translate("card.no_reading", language)
        if status.latest is None
        else translate(
            "card.latest", language, value=format_reading(indicator, status.latest, unit, language)
        )
    )
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=4),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Container(
                    width=10,
                    height=10,
                    border_radius=5,
                    bgcolor=status_color(status.status),
                    margin=ft.Margin.only(top=5),
                ),
                ft.Column(
                    expand=True,
                    spacing=1,
                    controls=[
                        ft.Row(
                            wrap=True,
                            spacing=8,
                            controls=[
                                ft.Text(
                                    translate(f"indicator.{indicator.value}", language),
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.TEXT,
                                ),
                                ft.Text(latest, size=13, color=theme.ACCENT),
                            ],
                        ),
                        ft.Text(resolution.reason.text(language), size=12, color=theme.MUTED),
                    ],
                ),
            ],
        ),
    )


def _trend(
    state: AppState,
    indicators: tuple[Indicator, ...],
    resolutions: dict[Indicator, IndicatorResolution],
    driver: Indicator | None,
) -> list[ft.Control]:
    language = state.language
    visible = state.visible_measurements()
    candidates = [driver] if driver is not None else []
    candidates += [i for i in indicators if i is not driver]
    for indicator in candidates:
        series = chart_series(visible, indicator)
        if len(series) < 2:
            continue
        baseline = resolutions[indicator].status.baseline
        chart = trend_chart(
            [m.value for m in series],
            baseline.low if baseline else None,
            baseline.high if baseline else None,
            status_color(resolutions[indicator].status.status),
        )
        if chart is not None:
            title = ft.Row(
                wrap=True,
                spacing=8,
                controls=[
                    ft.Text(translate("card.trend", language), size=13, color=theme.MUTED),
                    ft.Text(
                        translate(f"indicator.{indicator.value}", language),
                        size=13,
                        weight=ft.FontWeight.W_600,
                        color=theme.TEXT,
                    ),
                ],
            )
            return [title, chart]
    return [ft.Text(translate("card.trend_empty", language), size=12, color=theme.MUTED)]


trend_controls = _trend  # the pulse modal draws the same trend
