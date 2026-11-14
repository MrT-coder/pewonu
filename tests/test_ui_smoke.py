"""Part 1: the views build and show the right texts in both languages."""

import dataclasses

import pytest

ft = pytest.importorskip("flet")

from crew_self_check.astronaut.access import simulated_directory  # noqa: E402
from crew_self_check.astronaut.i18n import translate  # noqa: E402
from crew_self_check.astronaut.state import AppState, Section  # noqa: E402
from crew_self_check.astronaut.ui.common import Actions  # noqa: E402
from crew_self_check.astronaut.ui.login import build_login  # noqa: E402
from crew_self_check.astronaut.ui.shell import build_shell  # noqa: E402
from crew_self_check.core.reasons import Language  # noqa: E402

_TEXT_FIELDS = {"label", "content", "title", "hint_text", "error", "helper"}


def collect_texts(node: object) -> list[str]:
    """Every string shown by ``Text`` controls and labels, found by walking the control tree."""
    found: list[str] = []
    if isinstance(node, ft.Text) and node.value:
        found.append(str(node.value))
    if isinstance(node, str):
        return found
    if dataclasses.is_dataclass(node) and not isinstance(node, type):
        for field in dataclasses.fields(node):
            value = getattr(node, field.name, None)
            if field.name in _TEXT_FIELDS and isinstance(value, str):
                found.append(value)
            found.extend(collect_texts(value))
    elif isinstance(node, list | tuple):
        for item in node:
            found.extend(collect_texts(item))
    return found


class Recorder:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def actions(self) -> Actions:
        return Actions(
            login=lambda code: self._log(f"login:{code}") or True,
            set_language=lambda lang: self._log(f"lang:{lang.value}"),
            go=lambda section: self._log(f"go:{section.value}"),
            logout=lambda: self._log("logout"),
            show_limits=lambda: self._log("limits"),
            refresh=lambda: self._log("refresh"),
            rerender=lambda: self._log("rerender"),
        )

    def _log(self, call: str) -> None:
        self.calls.append(call)


def state_in(language: Language, *, logged_in: bool, section: Section = Section.HOME) -> AppState:
    state = AppState(simulated_directory())
    state.set_language(language)
    if logged_in:
        state.login("AST-0001")
        state.go(section)
    return state


@pytest.mark.parametrize("language", list(Language))
def test_login_view_shows_its_texts_in_the_language(language: Language) -> None:
    view = build_login(state_in(language, logged_in=False), Recorder().actions())
    assert isinstance(view, ft.Control)
    texts = collect_texts(view)
    for key in ("app.name", "login.title", "login.code_label", "login.enter", "login.private"):
        assert translate(key, language) in texts, (key, language)
    assert any("AST-0001" in text for text in texts)  # the demo hint


@pytest.mark.parametrize("language", list(Language))
@pytest.mark.parametrize("section", list(Section))
def test_shell_builds_every_section_in_both_languages(language: Language, section: Section) -> None:
    state = state_in(language, logged_in=True, section=section)
    view = build_shell(state, Recorder().actions())
    assert isinstance(view, ft.Control)
    texts = collect_texts(view)
    for key in ("nav.home", "nav.checkin", "nav.body", "nav.summary", "nav.logout"):
        assert translate(key, language) in texts, (key, language)
    assert any("AST-0001" in text for text in texts)  # who is logged in
    if section is Section.HOME:
        assert translate("home.greeting", language, code="AST-0001") in texts
        assert translate("home.privacy_body", language) in texts
    elif section is Section.CHECKIN:
        assert translate("checkin.subtitle", language) in texts
        assert translate("pulse.start", language) in texts
    else:
        assert translate(f"part.{section.value}.body", language) in texts


def test_spanish_view_has_no_english_navigation() -> None:
    view = build_shell(state_in(Language.ES, logged_in=True), Recorder().actions())
    texts = collect_texts(view)
    assert "Sign out" not in texts
    assert "Salir" in texts


# --- the pulse mission screens ---------------------------------------------------------------


def image_sources(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, ft.Image) and node.src:
        found.append(str(node.src))
    if dataclasses.is_dataclass(node) and not isinstance(node, type):
        for field in dataclasses.fields(node):
            found.extend(image_sources(getattr(node, field.name, None)))
    elif isinstance(node, list | tuple):
        for item in node:
            found.extend(image_sources(item))
    return found


def mission_state(language: Language, steps_confirmed: int) -> AppState:
    state = state_in(language, logged_in=True, section=Section.CHECKIN)
    state.start_pulse()
    assert state.pulse is not None
    for _ in range(steps_confirmed):
        state.pulse.complete_station()
    return state


@pytest.mark.parametrize("language", list(Language))
@pytest.mark.parametrize(("confirmed", "key"), [(0, "rest"), (1, "locate"), (2, "pressure")])
def test_each_step_shows_its_text_and_its_own_illustration(
    language: Language, confirmed: int, key: str
) -> None:
    state = mission_state(language, confirmed)
    view = build_shell(state, Recorder().actions())
    texts = collect_texts(view)
    assert translate(f"pulse.{key}.title", language) in texts
    assert translate(f"pulse.{key}.body", language) in texts
    assert translate("pulse.next", language) in texts
    assert f"pulse/{language.value}-step{confirmed + 1}.jpg" in image_sources(view)
    assert translate("pulse.points", language, points=confirmed * 10) in texts


@pytest.mark.parametrize("language", list(Language))
def test_the_count_station_offers_both_intervals(language: Language) -> None:
    state = mission_state(language, 3)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("pulse.interval_30", language) in texts
    assert translate("pulse.interval_60", language) in texts
    assert translate("pulse.begin_count", language) in texts
    assert translate("pulse.count.body", language, seconds=30) in texts


def finish(state: AppState, taps: int) -> None:
    assert state.pulse is not None
    state.pulse.start_count(0.0)
    for i in range(taps):
        state.pulse.tap(i * 0.5)
    state.pulse.finish(30.0)


@pytest.mark.parametrize("language", list(Language))
def test_a_valid_result_shows_the_formula_the_badge_and_the_save_button(
    language: Language,
) -> None:
    state = mission_state(language, 3)
    finish(state, 35)
    view = build_shell(state, Recorder().actions())
    texts = collect_texts(view)
    assert translate("pulse.formula_30", language, taps=35, bpm=70) in texts
    assert translate("pulse.badge", language) in texts
    assert translate("pulse.points_note", language) in texts
    assert translate("pulse.save", language) in texts
    assert f"pulse/{language.value}-step4.jpg" in image_sources(view)


@pytest.mark.parametrize("language", list(Language))
def test_an_implausible_result_asks_for_a_recount_and_cannot_be_saved(language: Language) -> None:
    state = mission_state(language, 3)
    finish(state, 2)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("pulse.recount_body", language) in texts
    assert translate("pulse.recount", language) in texts
    assert translate("pulse.save", language) not in texts
    assert translate("pulse.badge", language) not in texts


def test_the_hub_shows_the_last_pulse_after_saving() -> None:
    state = mission_state(Language.EN, 3)
    finish(state, 35)
    state.save_pulse()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("pulse.last", Language.EN, bpm=70) in texts
