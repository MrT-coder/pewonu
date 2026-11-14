"""Login by unique astronaut code (D-020)."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.access import AccessError
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, cabin_background, card, language_switch

_ERROR_KEYS = {
    AccessError.INVALID_FORMAT: "login.error.invalid_format",
    AccessError.UNKNOWN_CODE: "login.error.unknown_code",
}


def build_login(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    field = ft.TextField(
        label=say("login.code_label"),
        hint_text=say("login.code_hint"),
        autofocus=True,
        capitalization=ft.TextCapitalization.CHARACTERS,
        max_length=8,
        width=340,
        border_radius=12,
        prefix_icon=ft.Icons.BADGE_OUTLINED,
    )

    def submit(_: object) -> None:
        if actions.login(field.value or ""):
            return
        error = state.error
        field.error = say(_ERROR_KEYS[error]) if error else None
        actions.refresh()

    field.on_submit = submit

    demo_codes = ", ".join(state.demo_codes())
    panel = card(
        ft.Column(
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.ROCKET_LAUNCH, size=40, color=theme.ACCENT),
                ft.Text(say("app.name"), size=30, weight=ft.FontWeight.BOLD, color=theme.TEXT),
                ft.Text(say("app.tagline"), size=14, color=theme.MUTED),
                ft.Divider(height=8, color=theme.CARD_BORDER),
                ft.Text(say("login.title"), size=16, weight=ft.FontWeight.W_600, color=theme.TEXT),
                field,
                ft.FilledButton(
                    content=say("login.enter"), icon=ft.Icons.LOGIN, on_click=submit, height=46
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.LOCK_OUTLINE, size=14, color=theme.GOOD),
                        ft.Text(say("login.private"), size=12, color=theme.MUTED),
                    ],
                ),
                ft.Container(
                    padding=12,
                    bgcolor=theme.ACCENT_SOFT,
                    border_radius=12,
                    content=ft.Column(
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(say("login.demo_title"), size=12, color=theme.MUTED),
                            ft.Text(
                                say("login.demo_codes", codes=demo_codes),
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=theme.ACCENT,
                            ),
                        ],
                    ),
                ),
            ],
        ),
        padding=28,
    )
    panel.width = 440

    return cabin_background(
        ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    alignment=ft.Alignment.TOP_RIGHT,
                    padding=16,
                    content=ft.Row(
                        tight=True,
                        spacing=10,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.INFO_OUTLINE,
                                tooltip=say("nav.limits"),
                                on_click=lambda _: actions.show_limits(),
                            ),
                            language_switch(state, actions),
                        ],
                    ),
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(tight=True, controls=[panel]),
                ),
            ],
        )
    )
