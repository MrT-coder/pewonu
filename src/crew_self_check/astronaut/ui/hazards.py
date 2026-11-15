"""The hazards screen: the five NASA HRP hazards, where each applies and what it touches (T1)."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import format_reading, status_label_key
from crew_self_check.astronaut.cases import CASES, HAZARD_URL, Hazard
from crew_self_check.astronaut.hazards import HazardCard, HazardIndicator, HazardMode, build_hazards
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.core.contract import Status
from crew_self_check.core.reasons import Language

_ICONS = {
    Hazard.RADIATION: ft.Icons.FLARE,
    Hazard.ISOLATION: ft.Icons.GROUPS,
    Hazard.DISTANCE: ft.Icons.SATELLITE_ALT,
    Hazard.GRAVITY: ft.Icons.FITNESS_CENTER,
    Hazard.ENVIRONMENT: ft.Icons.AIR,
}


def _dot(color: str, size: int = 12) -> ft.Control:
    return ft.Container(width=size, height=size, border_radius=size // 2, bgcolor=color)


def _text(value: str, size: int = 13, color: str = theme.TEXT, bold: bool = False) -> ft.Text:
    weight = ft.FontWeight.W_600 if bold else ft.FontWeight.NORMAL
    return ft.Text(value, size=size, color=color, weight=weight)


def _worst_color(worst: Status | None) -> str:
    return status_color(worst) if worst is not None else theme.STATUS_NONE


def _worst_label(worst: Status | None, language: Language) -> str:
    if worst is None:
        return translate("hazards.not_measured", language)
    if worst in (Status.WATCH, Status.ACT):
        return translate("hazards.state.flagged", language)
    if worst is Status.OK:
        return translate("hazards.state.ok", language)
    return translate("hazards.state.unknown", language)


def _status_line(item: HazardCard, language: Language) -> str:
    if item.mode is HazardMode.COMMUNICATION:
        return translate("hazards.state.comm", language)
    return _worst_label(item.worst, language)


def _strip(cards: tuple[HazardCard, ...], language: Language) -> ft.Control:
    """Five chips: the whole picture at a glance."""
    chips: list[ft.Control] = []
    for item in cards:
        color = _worst_color(item.worst)
        chips.append(
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=18,
                border=ft.Border.all(1, color),
                content=ft.Row(
                    spacing=8,
                    tight=True,
                    controls=[
                        ft.Icon(_ICONS[item.hazard], size=18, color=color),
                        _text(translate(f"hazard.{item.hazard.value}", language), 12),
                        _dot(color, 10),
                    ],
                ),
            )
        )
    return ft.Row(wrap=True, spacing=8, run_spacing=8, controls=chips)


def _indicator_chip(item: HazardIndicator, language: Language) -> ft.Control:
    color = status_color(item.status)
    name = translate(f"indicator.{item.indicator.value}", language)
    value = (
        format_reading(item.indicator, item.latest, item.unit, language)
        if item.latest is not None
        else translate("card.no_reading", language)
    )
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
        border_radius=14,
        border=ft.Border.all(1, color),
        content=ft.Row(
            spacing=6,
            tight=True,
            controls=[
                _dot(color, 10),
                _text(f"{name} · {value}", 12),
                _text(translate(status_label_key(item.status), language), 11, theme.MUTED),
            ],
        ),
    )


def _hazard_card(item: HazardCard, state: AppState) -> ft.Control:
    language = state.language
    color = _worst_color(item.worst)
    name = translate(f"hazard.{item.hazard.value}", language)
    body: list[ft.Control] = [
        ft.Row(
            spacing=12,
            controls=[
                ft.Icon(_ICONS[item.hazard], size=30, color=color),
                ft.Column(
                    spacing=0,
                    expand=True,
                    controls=[
                        ft.Text(name, size=17, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                        _text(_status_line(item, language), 12, color),
                    ],
                ),
            ],
        ),
        _text(translate(f"hazard.{item.hazard.value}.what", language), 12, theme.MUTED),
        _text(translate("hazards.here", language), 12, theme.GOLD, bold=True),
        _text(translate(item.here_key, language), 14),
    ]
    if item.mode is HazardMode.NOT_MEASURED:
        body += [
            _text(translate("hazards.not_measured", language), 12, theme.ACCENT, bold=True),
            _text(translate(f"hazards.not_measured.{item.hazard.value}", language)),
        ]
    elif item.mode is HazardMode.COMMUNICATION:
        body += [
            _text(translate("hazards.comm", language, minutes=item.delay_minutes)),
            _text(translate("hazards.comm.what", language), 12, theme.MUTED),
        ]
    else:
        body += [
            _text(translate("hazards.touches", language), 12, theme.ACCENT, bold=True),
            ft.Row(
                wrap=True,
                spacing=8,
                run_spacing=8,
                controls=[_indicator_chip(i, language) for i in item.indicators],
            ),
        ]
    for code, crew_id in state.demo_cases():
        case = CASES.get(crew_id)
        if case is not None and case.hazard is item.hazard:
            body.append(
                _text(translate("hazards.stressed_by", language, code=code), 11, theme.MUTED)
            )
    return card(ft.Column(spacing=8, controls=body), border_color=color)


def build_hazards_view(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    cards = build_hazards(state)
    place = translate(f"env.{state.environment.value}", language)
    header = card(
        ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    translate("hazards.title", language),
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT,
                ),
                _text(translate("hazards.intro", language), 13, theme.MUTED),
                _text(translate("hazards.you_are", language, place=place), 14, theme.GOLD, True),
                _strip(cards, language),
                ft.Row(
                    wrap=True,
                    spacing=12,
                    controls=[
                        _text(translate("hazard.source", language), 11, theme.MUTED),
                        ft.TextButton(
                            content=translate("card.source_open", language),
                            url=HAZARD_URL,
                            icon=ft.Icons.OPEN_IN_NEW,
                        ),
                    ],
                ),
                _text(translate("hazards.assumption", language), 11, theme.MUTED),
            ],
        )
    )
    grid = ft.ResponsiveRow(
        spacing=14,
        run_spacing=14,
        controls=[
            ft.Container(content=_hazard_card(item, state), col={"xs": 12, "md": 6})
            for item in cards
        ],
    )
    return ft.Column(
        spacing=14, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=[header, grid]
    )
