"""Entry point of the astronaut app: wires the state to the views."""

from __future__ import annotations

import os
from pathlib import Path

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.share_model import OutboxItem
from crew_self_check.astronaut.sqlite_store import SqliteMeasurementStore
from crew_self_check.astronaut.state import AppState, Section
from crew_self_check.astronaut.ui.common import Actions, glossary_dialog, limits_dialog
from crew_self_check.astronaut.ui.login import build_login
from crew_self_check.astronaut.ui.share import package_dialog
from crew_self_check.astronaut.ui.shell import build_shell
from crew_self_check.core.contract import System
from crew_self_check.core.reasons import Language

PORT = 8550
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
DB_ENV = "CREW_SELF_CHECK_DB"
DEFAULT_DB = Path("data") / "crew-self-check.db"  # data/ is git-ignored (AGENTS.md section 8)

_store: SqliteMeasurementStore | None = None


def _shared_store() -> SqliteMeasurementStore:
    """One local database for every browser session of this run."""
    global _store
    if _store is None:
        _store = SqliteMeasurementStore(Path(os.environ.get(DB_ENV, DEFAULT_DB)))
    return _store


def main(page: ft.Page) -> None:
    state = AppState(simulated_directory(), store=_shared_store())
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

    def set_day(index: int) -> None:
        state.set_day(max(0, min(index, len(state.scenario.days) - 1)))
        render()

    def select_system(system: System | None) -> None:
        state.select_system(system)
        render()

    def show_package(item: OutboxItem) -> None:
        page.show_dialog(package_dialog(item, state.language, close_limits))

    def close_limits() -> None:
        page.pop_dialog()

    def show_limits() -> None:
        page.show_dialog(limits_dialog(state.language, close_limits))

    def show_glossary() -> None:
        page.show_dialog(glossary_dialog(state.language, close_limits))

    actions = Actions(
        login=login,
        set_language=set_language,
        go=go,
        logout=logout,
        show_limits=show_limits,
        show_glossary=show_glossary,
        set_day=set_day,
        select_system=select_system,
        show_package=show_package,
        refresh=page.update,
        rerender=render,
    )
    render()


def run() -> None:
    """Serve the app on this computer only. ``no_cdn`` keeps it working without internet (A1)."""
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        host="127.0.0.1",
        port=PORT,
        no_cdn=True,
        assets_dir=str(ASSETS_DIR),
    )
