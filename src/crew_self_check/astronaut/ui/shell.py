"""The shell after login: navigation, top bar and the section content."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.body import build_body
from crew_self_check.astronaut.ui.cases import case_card
from crew_self_check.astronaut.ui.checkin import build_checkin
from crew_self_check.astronaut.ui.common import Actions, cabin_background, card, language_switch
from crew_self_check.astronaut.ui.intake import build_intake_view
from crew_self_check.astronaut.ui.journey import journey_bar
from crew_self_check.astronaut.ui.summary import build_summary_view

_SECTIONS = list(Section)

_ICONS = {
    Section.HOME: ft.Icons.HOME_OUTLINED,
    Section.CHECKIN: ft.Icons.MONITOR_HEART_OUTLINED,
    Section.BODY: ft.Icons.ACCESSIBILITY_NEW,
    Section.SUMMARY: ft.Icons.DASHBOARD_OUTLINED,
    Section.DATA: ft.Icons.INPUT,
}

_PARTS = (Section.CHECKIN, Section.DATA, Section.BODY, Section.SUMMARY)


def _part_card(section: Section, state: AppState, actions: Actions) -> ft.Control:
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
                ft.OutlinedButton(
                    content=translate("part.open", language),
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda _: actions.go(section),
                ),
            ],
        )
    )


def _home(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    case = case_card(language, state.profile.crew_id) if state.profile else None
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
            *([case] if case is not None else []),
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
                    ft.Container(content=_part_card(part, state, actions), col={"xs": 12, "md": 3})
                    for part in _PARTS
                ],
            ),
        ],
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
                        icon=ft.Icons.MENU_BOOK_OUTLINED,
                        tooltip=translate("nav.glossary", language),
                        on_click=lambda _: actions.show_glossary(),
                    ),
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

    body: ft.Control
    if state.section is Section.HOME:
        body = _home(state, actions)
    elif state.section is Section.CHECKIN:
        body = build_checkin(state, actions)
    elif state.section is Section.BODY:
        body = build_body(state, actions)
    elif state.section is Section.DATA:
        body = build_intake_view(state, actions)
    else:
        body = build_summary_view(state, actions)
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
                        expand=True,
                        spacing=18,
                        scroll=ft.ScrollMode.AUTO,  # long cards must stay reachable
                        controls=[_top_bar(state, actions), journey_bar(state, actions), body],
                    ),
                ),
            ],
        )
    )
