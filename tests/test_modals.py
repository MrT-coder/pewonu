"""T5: the single-screen UX opens everything in modals driven by the app state."""

from __future__ import annotations

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.state import AppState, Modal, VoiceStage
from crew_self_check.astronaut.voice_capture import SyntheticVoiceRecorder
from crew_self_check.core.contract import System


def _state() -> AppState:
    state = AppState(simulated_directory(), voice_recorder=SyntheticVoiceRecorder())
    state.login("AST-0001")
    return state


def test_nothing_is_open_at_first() -> None:
    assert _state().modal is Modal.NONE


def test_a_zone_opens_its_system_and_closing_forgets_it() -> None:
    state = _state()
    state.open_zone(System.CARDIOVASCULAR)
    assert state.modal is Modal.ZONE
    assert state.selected_system is System.CARDIOVASCULAR
    state.close_modal()
    assert state.modal is Modal.NONE
    assert state.selected_system is None


def test_the_wrist_opens_the_pulse_on_the_collected_data_tab() -> None:
    state = _state()
    state.open_pulse()
    assert state.modal is Modal.PULSE
    assert state.pulse_tab == "data"
    assert state.pulse is None


def test_measuring_by_hand_starts_the_mission_inside_the_same_modal() -> None:
    state = _state()
    state.open_pulse()
    state.pulse_measure()
    assert state.modal is Modal.PULSE
    assert state.pulse_tab == "hand"
    assert state.pulse is not None


def test_saving_the_pulse_goes_back_to_the_data_tab() -> None:
    state = _state()
    state.open_pulse()
    state.pulse_measure()
    assert state.pulse is not None
    for _ in range(3):
        state.pulse.complete_station()
    state.pulse.set_interval(60)
    state.pulse.submit_count(66)
    state.save_pulse()
    assert state.pulse_tab == "data"
    assert state.modal is Modal.PULSE


def test_closing_the_pulse_modal_abandons_an_unfinished_mission() -> None:
    state = _state()
    state.open_pulse()
    state.pulse_measure()
    state.close_modal()
    assert state.pulse is None
    assert state.modal is Modal.NONE


def test_the_mood_bubble_starts_with_the_faces_and_the_voice_follows_in_the_same_modal() -> None:
    state = _state()
    state.open_mood()
    assert state.modal is Modal.MOOD
    assert state.voice_stage is VoiceStage.IDLE
    state.choose_mood(4)
    state.save_mood_and_continue()
    assert state.modal is Modal.MOOD
    assert state.voice_stage is VoiceStage.PROMPT
    assert state.own_measurements()[-1].value == 4


def test_leaving_the_voice_step_closes_the_whole_modal() -> None:
    state = _state()
    state.open_mood()
    state.choose_mood(3)
    state.save_mood_and_continue()
    state.cancel_voice()
    assert state.modal is Modal.NONE
    assert state.voice_stage is VoiceStage.IDLE


def test_skipping_the_voice_keeps_the_mood_that_was_saved() -> None:
    state = _state()
    state.open_mood()
    state.choose_mood(2)
    state.save_mood_and_continue()
    state.close_modal()
    assert state.last_mood() is not None
    assert state.last_mood().value == 2  # type: ignore[union-attr]


def test_the_share_modal_opens_and_closes() -> None:
    state = _state()
    state.open_share()
    assert state.modal is Modal.SHARE
    state.close_modal()
    assert state.modal is Modal.NONE


def test_only_one_modal_is_open_at_a_time() -> None:
    state = _state()
    state.open_share()
    state.open_zone(System.MOOD)
    assert state.modal is Modal.ZONE


def test_nothing_opens_without_a_session() -> None:
    state = AppState(simulated_directory())
    with pytest.raises(RuntimeError):
        state.open_share()


def test_signing_out_closes_everything() -> None:
    state = _state()
    state.open_mood()
    state.logout()
    assert state.modal is Modal.NONE


def test_the_bubble_can_be_dragged_and_stays_on_screen() -> None:
    state = _state()
    start = state.bubble_offset
    state.move_bubble(-40, -25)  # dragging left and up moves it away from the right/bottom edges
    assert state.bubble_offset == (start[0] + 40, start[1] + 25)
    state.move_bubble(5000, 5000)  # far past the edge: it keeps a margin
    assert state.bubble_offset == (8, 8)
