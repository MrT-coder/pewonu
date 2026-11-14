"""Entry point of the astronaut app: wires the state to the views."""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.common import Actions, limits_dialog
from crew_self_check.astronaut.ui.login import build_login
from crew_self_check.astronaut.ui.shell import build_shell
from crew_self_check.core.reasons import Language

PORT = 8550


def main(page: ft.Page) -> None:
    state = AppState(simulated_directory())
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = theme.BG_BOTTOM
    page.padding = 0

    def render() -> None:
        page.title = translate("app.name", state.language)
        view = build_shell(state, actions) if state.logged_in else build_login(state, actions)
        page.controls.clear()
        page.add(view)
        page.update()

    def login(code: str) -> bool:
        ok = state.login(code)
        if ok:
            render()
        return ok

    def set_language(language: Language) -> None:
        state.set_language(language)
        render()

    def go(section: Section) -> None:
        state.go(section)
        render()

    def logout() -> None:
        state.logout()
        render()

    def close_limits() -> None:
        page.pop_dialog()

    def show_limits() -> None:
        page.show_dialog(limits_dialog(state.language, close_limits))

    actions = Actions(
        login=login,
        set_language=set_language,
        go=go,
        logout=logout,
        show_limits=show_limits,
        refresh=page.update,
    )
    render()


def run() -> None:
    """Serve the app on this computer only. ``no_cdn`` keeps it working without internet (A1)."""
    ft.run(main, view=ft.AppView.WEB_BROWSER, host="127.0.0.1", port=PORT, no_cdn=True)
