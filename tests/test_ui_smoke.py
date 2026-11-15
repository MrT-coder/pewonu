"""Part 1: the views build and show the right texts in both languages."""

import dataclasses

import pytest

ft = pytest.importorskip("flet")

from crew_self_check.astronaut.access import simulated_directory  # noqa: E402
from crew_self_check.astronaut.body_model import reference_text  # noqa: E402
from crew_self_check.astronaut.cases import CASES  # noqa: E402
from crew_self_check.astronaut.i18n import translate  # noqa: E402
from crew_self_check.astronaut.state import AppState, Section  # noqa: E402
from crew_self_check.astronaut.ui.common import Actions, glossary_dialog  # noqa: E402
from crew_self_check.astronaut.ui.login import build_login  # noqa: E402
from crew_self_check.astronaut.ui.share import package_dialog  # noqa: E402
from crew_self_check.astronaut.ui.shell import build_shell  # noqa: E402
from crew_self_check.core.contract import Indicator, System  # noqa: E402
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
            show_glossary=lambda: self._log("glossary"),
            set_day=lambda index: self._log(f"day:{index}"),
            select_system=lambda system: self._log(f"system:{system}"),
            show_package=lambda item: self._log(f"package:{item.day_label}"),
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
    state = state_in(language, logged_in=True)
    state.open_pulse()
    state.pulse_measure()
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
    assert translate("pulse.count.body", language, seconds=30) in texts


@pytest.mark.parametrize("language", list(Language))
def test_the_count_station_asks_for_the_beats_instead_of_a_tap_button(language: Language) -> None:
    state = mission_state(language, 3)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("pulse.beats_label", language, seconds=30) in texts
    assert translate("pulse.calculate", language) in texts
    assert translate("pulse.timer_start", language, seconds=30) in texts  # optional helper
    state.pulse.set_interval(60)  # type: ignore[union-attr]
    again = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("pulse.beats_label", language, seconds=60) in again


def test_there_is_no_tap_counting_left_in_the_texts() -> None:
    from crew_self_check.astronaut.i18n import STRINGS

    assert "pulse.tap" not in STRINGS
    assert "pulse.begin_count" not in STRINGS


def finish(state: AppState, beats: int) -> None:
    assert state.pulse is not None
    state.pulse.submit_count(beats)


@pytest.mark.parametrize("language", list(Language))
def test_a_valid_result_shows_the_formula_the_badge_and_the_save_button(
    language: Language,
) -> None:
    state = mission_state(language, 3)
    finish(state, 35)
    view = build_shell(state, Recorder().actions())
    texts = collect_texts(view)
    assert translate("pulse.formula_30", language, beats=35, bpm=70) in texts
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


# --- the mood faces -----------------------------------------------------------------------------


# --- the glossary -------------------------------------------------------------------------------


@pytest.mark.parametrize("language", list(Language))
def test_the_glossary_dialog_lists_every_term_with_its_meaning(language: Language) -> None:
    from crew_self_check.astronaut.i18n import GLOSSARY

    texts = collect_texts(glossary_dialog(language, lambda: None))
    assert translate("nav.glossary", language) in texts
    for entry in GLOSSARY:
        term, definition = entry[language]
        assert term in texts
        assert definition in texts
    assert translate("glossary.close", language) in texts


def test_the_language_switch_shows_names_not_acronyms() -> None:
    texts = collect_texts(build_login(state_in(Language.EN, logged_in=False), Recorder().actions()))
    assert "English" in texts
    assert "Español" in texts
    assert "EN" not in texts
    assert "ES" not in texts


# --- the journey bar and the body view -----------------------------------------------------------


def body_state(
    language: Language, label: str = "R+3", system: System | None = None, code: str = "AST-0001"
) -> AppState:
    state = AppState(simulated_directory())
    state.set_language(language)
    state.login(code)
    state.set_day(next(d.index for d in state.scenario.days if d.label == label))
    state.go(Section.BODY)
    if system is not None:
        state.open_zone(system)
    return state


@pytest.mark.parametrize("language", list(Language))
def test_a_selected_system_explains_itself_with_its_reason_reference_and_source(
    language: Language,
) -> None:
    state = body_state(language, "R+3", System.CARDIOVASCULAR)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    pulse = state.resolutions()[Indicator.RESTING_HR]
    assert translate("system.cardiovascular.what", language) in texts
    assert translate("system.cardiovascular.why", language) in texts
    assert pulse.reason.text(language) in texts
    assert (
        translate("card.compared", language, what=reference_text(pulse.status, language)) in texts
    )
    assert translate("card.source", language) in texts
    assert translate("escalation.crew_cmo", language) in texts
    assert translate("card.nothing_sent", language) in texts
    assert translate("card.todo.escalate", language) in texts
    assert translate("indicator.resting_hr", language) in texts


def test_the_trend_shows_a_chart_when_there_are_readings_and_a_message_when_there_are_not() -> None:
    with_data = collect_texts(
        build_shell(body_state(Language.EN, "R+3", System.CARDIOVASCULAR), Recorder().actions())
    )
    assert translate("card.trend", Language.EN) in with_data
    assert translate("card.trend_empty", Language.EN) not in with_data
    none = collect_texts(
        build_shell(
            body_state(Language.EN, "E-14", System.CARDIOVASCULAR, "AST-0002"), Recorder().actions()
        )
    )
    assert translate("card.trend_empty", Language.EN) in none


@pytest.mark.parametrize("language", list(Language))
def test_a_system_with_nothing_measured_says_so_and_offers_no_chart(language: Language) -> None:
    state = body_state(language, "R+3", System.BONE_MUSCLE)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("system.bone_muscle.what", language) in texts
    assert translate("system.bone_muscle.why", language) in texts
    assert translate("card.trend", language) not in texts


def test_the_card_of_a_green_system_does_not_push_to_escalate() -> None:
    state = body_state(Language.EN, "E-1", System.SLEEP_BRAIN)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("escalation.self_care", Language.EN) in texts
    assert translate("escalation.crew_cmo", Language.EN) not in texts
    assert translate("card.todo.escalate", Language.EN) not in texts


# --- the summary ---------------------------------------------------------------------------------


# --- sharing with the ground team ----------------------------------------------------------------


def summary_state(language: Language, label: str, code: str = "AST-0001") -> AppState:
    """A person on a given day with the share modal open (the share panel lives there now)."""
    state = body_state(language, label, None, code)
    state.open_share()
    return state


def controls_of(node: object, kind: type) -> list[object]:
    """Every control of a given type found by walking the control tree."""
    found: list[object] = []
    if isinstance(node, kind):
        found.append(node)
    if dataclasses.is_dataclass(node) and not isinstance(node, type):
        for field in dataclasses.fields(node):
            found.extend(controls_of(getattr(node, field.name, None), kind))
    elif isinstance(node, list | tuple):
        for item in node:
            found.extend(controls_of(item, kind))
    return found


def send_button(view: object, language: Language) -> ft.FilledButton:
    label = translate("share.send", language)
    (button,) = [b for b in controls_of(view, ft.FilledButton) if b.content == label]  # type: ignore[attr-defined]
    return button  # type: ignore[return-value]


def confirm_box(view: object, language: Language) -> ft.Checkbox:
    label = translate("share.confirm", language)
    (box,) = [b for b in controls_of(view, ft.Checkbox) if b.label == label]  # type: ignore[attr-defined]
    return box  # type: ignore[return-value]


@pytest.mark.parametrize("language", list(Language))
def test_the_share_panel_states_the_rule_and_offers_the_shortcuts(language: Language) -> None:
    texts = collect_texts(build_shell(summary_state(language, "R+3"), Recorder().actions()))
    for key in (
        "share.title",
        "share.note",
        "share.attention",
        "share.all",
        "share.clear",
        "share.nothing",
        "share.confirm",
        "share.send",
        "share.sent_title",
        "share.sent_empty",
        "share.sim_note",
    ):
        assert translate(key, language) in texts, key


def test_there_is_a_checkbox_per_reading_and_sending_starts_disabled() -> None:
    state = summary_state(Language.EN, "R+3")
    view = build_shell(state, Recorder().actions())
    assert len(controls_of(view, ft.Checkbox)) == len(state.shareable()) + 1  # + the confirmation
    assert send_button(view, Language.EN).disabled is True
    assert confirm_box(view, Language.EN).disabled is True  # nothing selected yet


def test_sending_needs_a_selection_and_a_confirmation() -> None:
    state = summary_state(Language.EN, "R+3")
    state.toggle_share(Indicator.RESTING_HR)
    view = build_shell(state, Recorder().actions())
    assert confirm_box(view, Language.EN).disabled is False
    assert confirm_box(view, Language.EN).value is False
    assert send_button(view, Language.EN).disabled is True  # not confirmed yet
    assert translate("share.summary", Language.EN, readings=1, states=1) in collect_texts(view)
    state.set_share_confirmed(True)
    ready = build_shell(state, Recorder().actions())
    assert confirm_box(ready, Language.EN).value is True
    assert send_button(ready, Language.EN).disabled is False


def test_the_chosen_readings_are_the_checked_boxes() -> None:
    state = summary_state(Language.EN, "R+3")
    state.select_attention()
    view = build_shell(state, Recorder().actions())
    checked = [b for b in controls_of(view, ft.Checkbox) if b.value]  # type: ignore[attr-defined]
    assert len(checked) == len(state.share_selection)


def test_a_sent_package_is_listed_in_transit_and_then_delivered() -> None:
    state = summary_state(Language.EN, "R+1")
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    state.send_to_ground()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("share.sent_line", Language.EN, label="R+1", readings=1, states=1) in texts
    minutes = state.ground_delay_minutes
    assert translate("share.in_transit", Language.EN, minutes=minutes) in texts
    assert translate("share.show_data", Language.EN) in texts
    assert translate("share.sent_empty", Language.EN) not in texts
    state.advance()
    later = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("share.delivered", Language.EN) in later


def test_the_package_dialog_shows_the_fhir_data_that_was_sent() -> None:
    state = summary_state(Language.EN, "R+3")
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    texts = collect_texts(package_dialog(item, Language.EN, lambda: None))
    assert translate("share.data_title", Language.EN) in texts
    assert any('"resourceType": "Bundle"' in text for text in texts)
    assert any("8867-4" in text for text in texts)  # the LOINC code of the pulse


# --- the three cases, the data intake and the pulse guidance -------------------------------


@pytest.mark.parametrize("language", list(Language))
def test_the_login_lists_the_three_cases_and_the_hazard_each_stresses(language: Language) -> None:
    texts = collect_texts(build_login(state_in(language, logged_in=False), Recorder().actions()))
    for crew_id, case in CASES.items():
        assert any(translate(case.title_key, language) in text for text in texts), crew_id
        assert any(translate(f"hazard.{case.hazard.value}", language) in text for text in texts)


@pytest.mark.parametrize("language", list(Language))
@pytest.mark.parametrize("code", ["AST-0001", "AST-0002", "AST-0003"])
def test_the_home_shows_the_case_of_the_person_in_session(language: Language, code: str) -> None:
    state = AppState(simulated_directory())
    state.set_language(language)
    state.login(code)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert state.profile is not None
    case = CASES[state.profile.crew_id]
    for key in (case.title_key, case.story_key, case.system_key, "hazard.source"):
        assert translate(key, language) in texts, key
    assert translate(f"hazard.{case.hazard.value}", language) in texts


@pytest.mark.parametrize("language", list(Language))
def test_the_pulse_result_says_what_it_means_and_what_to_do_before_saving(
    language: Language,
) -> None:
    state = AppState(simulated_directory())
    state.set_language(language)
    state.login("AST-0001")
    state.open_pulse()
    state.pulse_measure()
    assert state.pulse is not None
    for _ in range(3):
        state.pulse.complete_station()
    state.pulse.set_interval(60)
    state.pulse.submit_count(110)  # far above this person's usual 60
    texts = collect_texts(build_shell(state, Recorder().actions()))
    for key in (
        "pulse.meaning_title",
        "pulse.todo_title",
        "pulse.outside_one",
        "pulse.todo.single",
    ):
        assert translate(key, language) in texts, key
    assert translate("pulse.todo.rest", language) in texts
    assert translate("pulse.save", language) in texts
    assert state.own_measurements() == ()  # explained, not saved yet


# --- the voice log -------------------------------------------------------------------------------


def voice_state(language: Language, code: str = "AST-0003", day: str = "T+8") -> AppState:
    from crew_self_check.astronaut.voice_capture import SyntheticVoiceRecorder

    state = AppState(simulated_directory(), voice_recorder=SyntheticVoiceRecorder())
    state.set_language(language)
    state.login(code)
    state.set_day(next(d.index for d in state.scenario.days if d.label == day))
    state.open_mood()  # the voice log opens inside the mood bubble
    return state


@pytest.mark.parametrize("language", list(Language))
def test_the_voice_screen_shows_an_open_question_and_says_nothing_is_kept(
    language: Language,
) -> None:
    state = voice_state(language)
    state.new_voice_prompt()
    state.open_voice()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("voice.intro", language) in texts
    assert translate(state.voice_prompt, language) in texts
    assert translate("voice.start", language) in texts
    assert translate("voice.another", language) in texts


@pytest.mark.parametrize("language", list(Language))
def test_without_a_microphone_the_screen_offers_the_labelled_sample(language: Language) -> None:
    state = voice_state(language)
    state._voice_recorder = None
    state.open_voice()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("voice.no_mic", language) in texts
    assert translate("voice.use_sample", language) in texts


@pytest.mark.parametrize("language", list(Language))
def test_the_result_compares_with_the_usual_and_says_the_audio_is_gone(language: Language) -> None:
    from crew_self_check.astronaut.voice_capture import SyntheticVoiceRecorder  # noqa: F401

    state = voice_state(language, day="E-1")
    state.open_voice()
    state.start_voice()
    state.stop_voice()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("voice.result_title", language) in texts
    assert translate("voice.discarded", language) in texts
    assert translate("voice.not_a_diagnosis", language) in texts
    assert translate("voice.synthetic", language) in texts
    assert (
        translate("voice.level.usual", language) in texts
        or translate("voice.level.different", language) in texts
    )


@pytest.mark.parametrize("language", list(Language))
def test_a_person_without_history_sees_the_baseline_building(language: Language) -> None:
    state = voice_state(language, code="AST-0002", day="E-1")
    state.open_voice()
    state.start_voice()
    state.stop_voice()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert any(
        "1" in text and translate("voice.building", language, n=1, needed=5) == text
        for text in texts
    )


# --- the single screen (UX v2) --------------------------------------------------------------------


@pytest.mark.parametrize("language", list(Language))
@pytest.mark.parametrize("section", [s for s in Section if s is not Section.HAZARDS])
def test_the_single_screen_shows_the_ring_the_body_and_the_data_in_both_languages(
    language: Language, section: Section
) -> None:
    state = state_in(language, logged_in=True, section=section)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    for key in ("nav.body", "nav.hazards", "nav.logout", "journey.title", "stage.hint"):
        assert translate(key, language) in texts, (key, language)
    assert state.current_day.label in texts
    assert translate("stage.data_title", language) in texts
    assert translate("intake.sources_title", language) in texts
    assert any("AST-0001" in text for text in texts)


@pytest.mark.parametrize("language", list(Language))
def test_the_hazards_are_the_second_screen(language: Language) -> None:
    state = state_in(language, logged_in=True, section=Section.HAZARDS)
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("hazards.title", language) in texts
    assert translate("journey.title", language) not in texts  # the ring belongs to the body screen


@pytest.mark.parametrize("language", list(Language))
def test_the_body_labels_every_zone_with_its_name_and_a_short_state(language: Language) -> None:
    texts = collect_texts(build_shell(body_state(language), Recorder().actions()))
    for key in (
        "system.sleep_brain",
        "system.vestibular",
        "system.cardiovascular",
        "system.immune",
        "system.bone_muscle",
        "zone.wrist",
    ):
        assert translate(key, language) in texts, key
    assert translate("summary.short.nothing", language) in texts  # bone and muscle: not measured


@pytest.mark.parametrize("language", list(Language))
def test_the_ring_shows_the_place_the_crew_is_in(language: Language) -> None:
    state = body_state(language, label="T+4")
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert "T+4" in texts
    assert translate("env.spacecraft.short", language) in texts
    assert translate("journey.play", language) in texts


@pytest.mark.parametrize("language", list(Language))
def test_the_wrist_opens_the_pulse_with_its_collected_data_and_the_way_to_measure(
    language: Language,
) -> None:
    state = body_state(language)
    state.open_pulse()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("zone.wrist", language) in texts
    assert translate("pulse.tab.data", language) in texts
    assert translate("pulse.tab.hand", language) in texts
    assert translate("pulse.latest", language) in texts
    assert translate("pulse.take_now", language) in texts


def test_after_saving_the_pulse_the_modal_shows_the_new_reading() -> None:
    state = mission_state(Language.EN, 3)
    finish(state, 35)
    state.save_pulse()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("pulse.latest", Language.EN) in texts
    assert any("70" in text for text in texts)


@pytest.mark.parametrize("language", list(Language))
def test_the_mood_bubble_opens_the_five_faces_and_offers_the_voice_log_next(
    language: Language,
) -> None:
    state = state_in(language, logged_in=True)
    state.open_mood()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("mood.prompt", language) in texts
    for level in range(1, 6):
        assert translate(f"mood.level.{level}", language) in texts
    assert translate("bubble.save_continue", language) in texts


def test_reopening_the_faces_says_which_one_was_saved_last() -> None:
    state = state_in(Language.ES, logged_in=True)
    state.choose_mood(4)
    state.save_mood()
    state.open_mood()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    label = translate("mood.level.4", Language.ES)
    assert translate("mood.last", Language.ES, label=label) in texts


@pytest.mark.parametrize("language", list(Language))
def test_the_share_modal_states_the_rule(language: Language) -> None:
    state = state_in(language, logged_in=True)
    state.open_share()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("share.note", language) in texts
    assert translate("share.send", language) in texts


def test_nothing_floats_over_the_screen_when_no_modal_is_open_except_the_bubble() -> None:
    state = state_in(Language.EN, logged_in=True)
    view = build_shell(state, Recorder().actions())
    assert state.modal.value == "none"
    # the bubble is there (tooltip) and no modal title is
    texts = collect_texts(view)
    assert translate("modal.close", Language.EN) not in texts


# --- PeWoNu: the pillars, the workout and the food (D-030) ------------------------------------


@pytest.mark.parametrize("language", list(Language))
def test_the_home_screen_shows_the_three_pillars(language: Language) -> None:
    view = build_shell(state_in(language, logged_in=True), Recorder().actions())
    texts = collect_texts(view)
    for key in ("pewonu.peace", "pewonu.wod", "pewonu.nutrition"):
        assert translate(key, language) in texts, (key, language)


@pytest.mark.parametrize("language", list(Language))
def test_the_workout_modal_lists_the_blocks_the_disclaimer_and_the_bone_note(
    language: Language,
) -> None:
    state = state_in(language, logged_in=True)
    state.open_wod()
    texts = collect_texts(build_shell(state, Recorder().actions()))
    plan = state.wod_plan()
    assert plan is not None
    assert translate(f"wod.kind.{plan.kind}", language) in texts
    assert translate("wod.disclaimer", language) in texts
    assert any("g/cm²" in text for text in texts)


@pytest.mark.parametrize("language", list(Language))
def test_the_nutrition_modal_logs_a_food_and_shows_the_totals(language: Language) -> None:
    state = state_in(language, logged_in=True)
    state.open_nutrition()
    assert translate("nutrition.empty", language) in collect_texts(
        build_shell(state, Recorder().actions())
    )
    state.add_meal("oatmeal")
    texts = collect_texts(build_shell(state, Recorder().actions()))
    assert translate("food.oatmeal", language) in texts
    assert translate("nutrition.disclaimer", language) in texts
    assert not any("kg of" in t and "supplement" in t.lower() for t in texts)
