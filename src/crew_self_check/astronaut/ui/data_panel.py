"""The data panel of the single screen: everything the astronaut has, in one place (UX v2).

It replaces the old Data and Summary sections: the readings that came in with their state, where
they come from, and the way to share them. Values and colors come from the engine and the intake
model; this view only lays them out.
"""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import format_reading
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.intake import SourceKind, build_intake
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.core.contract import Indicator, System
from crew_self_check.core.status import SYSTEM_INDICATORS

_SOURCE_ICONS = {
    SourceKind.WEARABLE: ft.Icons.WATCH,
    SourceKind.SURVEY: ft.Icons.FACT_CHECK_OUTLINED,
    SourceKind.HAND_PULSE: ft.Icons.FRONT_HAND_OUTLINED,
    SourceKind.ENTERED: ft.Icons.EDIT_NOTE,
}


def _system_of(indicator: Indicator) -> System | None:
    for system, indicators in SYSTEM_INDICATORS.items():
        if indicator in indicators:
            return system
    return None


def _units(state: AppState) -> dict[Indicator, str]:
    units: dict[Indicator, str] = {}
    for measurement in state.visible_measurements():
        units[measurement.indicator] = measurement.unit
    return units


def _open_indicator(state: AppState, actions: Actions, indicator: Indicator) -> None:
    if indicator is Indicator.RESTING_HR:
        state.open_pulse()
    elif indicator is Indicator.MOOD:
        state.open_mood()
    else:
        system = _system_of(indicator)
        if system is None:
            return
        state.open_zone(system)
    actions.rerender()


def _row(
    state: AppState, actions: Actions, indicator: Indicator, units: dict[Indicator, str]
) -> ft.Control:
    resolution = state.resolutions()[indicator]
    latest = resolution.status.latest
    value = (
        format_reading(indicator, latest, units.get(indicator, ""), state.language)
        if latest is not None
        else "—"
    )
    return ft.Container(
        ink=True,
        border_radius=10,
        padding=ft.Padding.symmetric(horizontal=8, vertical=6),
        on_click=lambda _: _open_indicator(state, actions, indicator),
        content=ft.Row(
            spacing=10,
            controls=[
                ft.Container(
                    width=10,
                    height=10,
                    border_radius=5,
                    bgcolor=status_color(resolution.status.status),
                ),
                ft.Text(
                    translate(f"indicator.{indicator.value}", state.language),
                    size=13,
                    color=theme.TEXT,
                    expand=True,
                ),
                ft.Text(value, size=13, color=theme.TEXT),
            ],
        ),
    )


def _sources(state: AppState) -> ft.Control:
    intake = build_intake(state)
    counts = {row.kind: row.readings for row in intake.sources}
    tiles: list[ft.Control] = [
        ft.Container(
            expand=True,
            padding=ft.Padding.symmetric(vertical=8),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.6, "#06101f"),
            border=ft.Border.all(1, theme.CARD_BORDER),
            tooltip=translate(f"intake.source.{kind.value}", state.language),
            content=ft.Column(
                tight=True,
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(_SOURCE_ICONS[kind], size=18, color=theme.ACCENT),
                    ft.Text(
                        str(counts.get(kind, 0)),
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=theme.TEXT,
                    ),
                    ft.Text(
                        translate(f"intake.short.{kind.value}", state.language),
                        size=10,
                        color=theme.MUTED,
                    ),
                ],
            ),
        )
        for kind in SourceKind
    ]
    return ft.Row(spacing=8, controls=tiles)


def build_data_panel(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    intake = build_intake(state)
    units = _units(state)
    totals = translate(
        "intake.totals",
        language,
        n=intake.total_readings,
        covered=intake.indicators_covered,
        total=intake.indicators_total,
    )

    def share(_: object) -> None:
        state.open_share()
        actions.rerender()

    return card(
        ft.Column(
            spacing=10,
            expand=True,
            controls=[
                ft.Text(
                    translate("stage.data_title", language),
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=theme.MUTED,
                ),
                ft.Text(totals, size=13, weight=ft.FontWeight.W_600, color=theme.GOOD),
                ft.Text(
                    translate("intake.origin_simulated", language) if intake.simulated else "",
                    size=11,
                    color=theme.GOLD,
                ),
                ft.Column(
                    spacing=0,
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[_row(state, actions, indicator, units) for indicator in Indicator],
                ),
                ft.Text(
                    translate("intake.sources_title", language),
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=theme.MUTED,
                ),
                _sources(state),
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.FilledButton(
                            content=translate("share.title", language),
                            icon=ft.Icons.SEND,
                            on_click=share,
                        ),
                        ft.OutlinedButton(
                            content=translate("nav.hazards", language),
                            icon=ft.Icons.WARNING_AMBER,
                            on_click=lambda _: actions.go(Section.HAZARDS),
                        ),
                    ],
                ),
            ],
        )
    )
