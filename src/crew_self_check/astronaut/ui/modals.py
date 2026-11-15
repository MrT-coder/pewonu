"""Everything that opens on top of the single screen: one modal at a time (UX v2).

The modal is a function of the app state (``state.modal``), so the existing screens keep working
unchanged: the pulse mission, the five faces, the voice log and the share panel call
``actions.rerender`` as before, and the overlay is rebuilt with the new step.
"""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import format_reading, status_label_key
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, Modal, VoiceStage
from crew_self_check.astronaut.summary_model import build_summary
from crew_self_check.astronaut.ui.checkin import build_mood_card, build_pulse_mission
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.astronaut.ui.share import build_share_panel
from crew_self_check.astronaut.ui.system_card import build_system_card, status_chip, trend_controls
from crew_self_check.astronaut.ui.voice import build_voice
from crew_self_check.core.contract import Indicator, Status, System

_WIDTH = 760


def _title(state: AppState) -> str:
    language = state.language
    if state.modal is Modal.ZONE and state.selected_system is not None:
        return translate(f"system.{state.selected_system.value}", language)
    if state.modal is Modal.PULSE:
        return translate("zone.wrist", language)
    if state.modal is Modal.SHARE:
        return translate("share.title", language)
    return translate("bubble.label", language)


def _zone_body(state: AppState) -> ft.Control:
    system = state.selected_system
    assert system is not None
    status = state.system_statuses().get(system)
    return build_system_card(state, system, status, state.resolutions())


def _pulse_tabs(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def choose(event: ft.Event[ft.SegmentedButton]) -> None:
        if next(iter(event.control.selected)) == "hand":
            state.pulse_measure()
        else:
            state.pulse_data()
        actions.rerender()

    return ft.SegmentedButton(
        selected=[state.pulse_tab],
        allow_empty_selection=False,
        segments=[
            ft.Segment(value="data", label=ft.Text(translate("pulse.tab.data", language))),
            ft.Segment(value="hand", label=ft.Text(translate("pulse.tab.hand", language))),
        ],
        on_change=choose,
    )


def _pulse_data(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    resolutions = state.resolutions()
    resolution = resolutions[Indicator.RESTING_HR]
    status = resolution.status
    unit = next(
        (
            m.unit
            for m in reversed(state.visible_measurements())
            if m.indicator is Indicator.RESTING_HR
        ),
        "bpm",
    )
    value = (
        format_reading(Indicator.RESTING_HR, status.latest, unit, language)
        if status.latest is not None
        else "—"
    )

    def measure(_: object) -> None:
        state.pulse_measure()
        actions.rerender()

    todo = ["card.todo.measure", "card.todo.read"]
    if status.status in (Status.WATCH, Status.ACT):
        todo.append("card.todo.escalate")
    return ft.Column(
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        tight=True,
                        spacing=0,
                        controls=[
                            ft.Text(say("pulse.latest"), size=12, color=theme.MUTED),
                            ft.Text(value, size=34, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                        ],
                    ),
                    status_chip(status.status, say(status_label_key(status.status))),
                ],
            ),
            ft.Text(resolution.reason.text(language), size=13, color=theme.MUTED),
            *trend_controls(state, (Indicator.RESTING_HR,), resolutions, Indicator.RESTING_HR),
            card(
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            say("pulse.where_from"),
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT,
                        ),
                        ft.Text(say("intake.source.hand_pulse.what"), size=12, color=theme.MUTED),
                    ],
                )
            ),
            card(
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            say("card.what_to_do"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT,
                        ),
                        *[ft.Text(f"•  {say(key)}", size=13, color=theme.MUTED) for key in todo],
                    ],
                )
            ),
            ft.FilledButton(
                content=say("pulse.take_now"), icon=ft.Icons.FRONT_HAND, height=46, on_click=measure
            ),
        ],
    )


def _pulse_body(state: AppState, actions: Actions) -> ft.Control:
    if state.pulse_tab == "hand" and state.pulse is None:
        state.pulse_data()  # the mission was left: back to the collected data
    content = (
        build_pulse_mission(state, actions)
        if state.pulse_tab == "hand"
        else _pulse_data(state, actions)
    )
    return ft.Column(
        spacing=14,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[_pulse_tabs(state, actions), content],
    )


def _body(state: AppState, actions: Actions) -> ft.Control:
    if state.modal is Modal.ZONE:
        return _zone_body(state)
    if state.modal is Modal.PULSE:
        return _pulse_body(state, actions)
    if state.modal is Modal.SHARE:
        return build_share_panel(state, build_summary(state), actions)
    if state.voice_stage is not VoiceStage.IDLE:
        return build_voice(state, actions)
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[build_mood_card(state, actions)],
    )


def modal_overlay(state: AppState, actions: Actions) -> ft.Control | None:
    """The scrim and the card of the open modal, or ``None`` when nothing is open."""
    if state.modal is Modal.NONE:
        return None

    def close(_: object) -> None:
        state.close_modal()
        actions.rerender()

    body = _body(state, actions)
    accent = (
        _system_color(state, state.selected_system)
        if state.modal is Modal.ZONE and state.selected_system is not None
        else theme.ACCENT
    )
    panel = ft.Container(
        width=_WIDTH,
        padding=ft.Padding.symmetric(horizontal=24, vertical=20),
        border_radius=22,
        bgcolor=ft.Colors.with_opacity(0.94, theme.CARD),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, accent)),
        shadow=ft.BoxShadow(blur_radius=50, color=ft.Colors.with_opacity(0.6, "#000000")),
        on_click=lambda _: None,  # a tap inside does not close it
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            _title(state), size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            tooltip=translate("modal.close", state.language),
                            on_click=close,
                        ),
                    ],
                ),
                body,
            ],
        ),
    )
    return ft.Container(
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.66, "#01040c"),
        blur=ft.Blur(6, 6),
        on_click=close,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Container(height=36), panel, ft.Container(height=36)],
        ),
    )


def _system_color(state: AppState, system: System) -> str:
    status = state.system_statuses().get(system)
    return status_color(status.status if status else None)
