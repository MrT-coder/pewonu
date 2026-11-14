"""The shell after login: navigation, top bar and the section content."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.common import Actions, cabin_background, card, language_switch

_SECTIONS = list(Section)

_ICONS = {
    Section.HOME: ft.Icons.HOME_OUTLINED,
    Section.CHECKIN: ft.Icons.MONITOR_HEART_OUTLINED,
    Section.BODY: ft.Icons.ACCESSIBILITY_NEW,
    Section.SUMMARY: ft.Icons.DASHBOARD_OUTLINED,
}

_PARTS = (Section.CHECKIN, Section.BODY, Section.SUMMARY)


def _coming_chip(language_text: str) -> ft.Container:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=3),
        border_radius=20,
        bgcolor=theme.ACCENT_SOFT,
        content=ft.Text(language_text, size=11, color=theme.ACCENT),
    )


def _part_card(section: Section, state: AppState) -> ft.Control:
    language = state.language
    return card(
        ft.Column(
            spacing=10,
            controls=[
                ft.Icon(_ICONS[section], size=30, color=theme.ACCENT),
                ft.Text(
                    translate(f"part.{section.value}.title", language),
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=theme.TEXT,
                ),
                ft.Text(
                    translate(f"part.{section.value}.body", language), size=13, color=theme.MUTED
                ),
                _coming_chip(translate("part.coming", language)),
            ],
        )
    )


def _home(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    return ft.Column(
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            card(
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            say("home.greeting", code=state.code),
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=theme.TEXT,
                        ),
                        ft.Text(say("home.subtitle"), size=14, color=theme.MUTED),
                        ft.Container(height=6),
                        ft.FilledButton(
                            content=say("home.cta"),
                            icon=ft.Icons.MONITOR_HEART_OUTLINED,
                            height=44,
                            on_click=lambda _: actions.go(Section.CHECKIN),
                        ),
                    ],
                )
            ),
            card(
                ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Icon(ft.Icons.LOCK_OUTLINE, size=26, color=theme.GOOD),
                        ft.Column(
                            spacing=4,
                            expand=True,
                            controls=[
                                ft.Text(
                                    say("home.privacy_title"),
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.TEXT,
                                ),
                                ft.Text(say("home.privacy_body"), size=13, color=theme.MUTED),
                            ],
                        ),
                    ],
                ),
                border_color=theme.GOOD,
            ),
            ft.Text(say("home.parts_title"), size=16, weight=ft.FontWeight.W_600, color=theme.TEXT),
            ft.ResponsiveRow(
                spacing=14,
                run_spacing=14,
                controls=[
                    ft.Container(content=_part_card(part, state), col={"xs": 12, "md": 4})
                    for part in _PARTS
                ],
            ),
        ],
    )


def _placeholder(section: Section, state: AppState) -> ft.Control:
    return ft.Container(
        alignment=ft.Alignment.TOP_LEFT,
        content=ft.Container(content=_part_card(section, state), width=520),
    )


def _top_bar(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text(
                translate(f"nav.{state.section.value}", language),
                size=22,
                weight=ft.FontWeight.BOLD,
                color=theme.TEXT,
            ),
            ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20,
                        bgcolor=theme.ACCENT_SOFT,
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=theme.ACCENT),
                                ft.Text(state.code or "", size=13, color=theme.ACCENT),
                            ],
                        ),
                    ),
                    language_switch(state, actions),
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINE,
                        tooltip=translate("nav.limits", language),
                        on_click=lambda _: actions.show_limits(),
                    ),
                    ft.OutlinedButton(
                        content=translate("nav.logout", language),
                        icon=ft.Icons.LOGOUT,
                        on_click=lambda _: actions.logout(),
                    ),
                ],
            ),
        ],
    )


def build_shell(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def changed(event: ft.Event[ft.NavigationRail]) -> None:
        actions.go(_SECTIONS[event.control.selected_index or 0])

    rail = ft.NavigationRail(
        selected_index=_SECTIONS.index(state.section),
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=theme.CARD,
        min_width=88,
        leading=ft.Container(
            padding=ft.Padding.symmetric(vertical=14),
            content=ft.Icon(ft.Icons.ROCKET_LAUNCH, size=28, color=theme.ACCENT),
        ),
        destinations=[
            ft.NavigationRailDestination(
                icon=_ICONS[section], label=translate(f"nav.{section.value}", language)
            )
            for section in _SECTIONS
        ],
        on_change=changed,
    )

    body = (
        _home(state, actions)
        if state.section is Section.HOME
        else _placeholder(state.section, state)
    )
    return cabin_background(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[
                rail,
                ft.VerticalDivider(width=1, color=theme.CARD_BORDER),
                ft.Container(
                    expand=True,
                    padding=24,
                    content=ft.Column(
                        expand=True, spacing=18, controls=[_top_bar(state, actions), body]
                    ),
                ),
            ],
        )
    )
