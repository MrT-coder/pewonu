"""A10: sharing with the ground team. Nothing leaves without confirmation (D-006)."""

from datetime import timedelta

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.share_model import DeliveryState, delivery_state
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Indicator
from crew_self_check.core.fhir import ConsentRequired, check_bundle


def start(code: str = "AST-0001", label: str = "R+3") -> AppState:
    state = AppState(simulated_directory())
    state.login(code)
    state.set_day(next(d.index for d in state.scenario.days if d.label == label))
    return state


def kinds(bundle: dict) -> list[str]:  # type: ignore[type-arg]
    return [e["resource"]["resourceType"] for e in bundle["entry"]]


def test_nothing_is_selected_and_nothing_was_sent_at_the_start() -> None:
    state = start()
    assert state.share_selection == set()
    assert not state.share_confirmed
    assert state.outbox == []
    assert state.ground_inbox == []


def test_the_astronaut_chooses_indicators_one_by_one() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.toggle_share(Indicator.MOOD)
    assert state.share_selection == {Indicator.RESTING_HR, Indicator.MOOD}
    state.toggle_share(Indicator.RESTING_HR)
    assert state.share_selection == {Indicator.MOOD}


def test_an_indicator_without_a_reading_cannot_be_chosen() -> None:
    state = start()  # R+3: no glucose reading on the planet
    with pytest.raises(ValueError, match="blood_glucose"):
        state.toggle_share(Indicator.BLOOD_GLUCOSE)
    assert state.share_selection == set()


def test_there_is_nothing_to_share_without_a_session() -> None:
    state = AppState(simulated_directory())
    state.toggle_share(Indicator.RESTING_HR)  # ignored: nobody is signed in
    assert state.share_selection == set()
    assert state.shareable() == ()


def test_the_shortcuts_select_what_needs_attention_or_everything() -> None:
    state = start()
    state.select_attention()
    assert Indicator.RESTING_HR in state.share_selection
    assert Indicator.SYSTOLIC_BP not in state.share_selection
    state.select_all()
    assert state.share_selection == set(state.shareable())
    assert Indicator.BLOOD_GLUCOSE not in state.share_selection
    state.clear_share()
    assert state.share_selection == set()


def test_changing_the_selection_withdraws_the_confirmation() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    assert state.share_confirmed
    state.toggle_share(Indicator.MOOD)
    assert not state.share_confirmed
    state.set_share_confirmed(True)
    state.select_all()
    assert not state.share_confirmed


def test_without_a_confirmation_nothing_is_built_or_sent() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    with pytest.raises(ConsentRequired):
        state.send_to_ground()
    assert state.outbox == []
    assert state.ground_inbox == []
    assert state.share_selection == {Indicator.RESTING_HR}  # nothing was lost


def test_an_empty_selection_is_refused_even_if_confirmed() -> None:
    state = start()
    state.set_share_confirmed(True)
    with pytest.raises(ValueError, match="nothing"):
        state.send_to_ground()
    assert state.outbox == []


def test_a_confirmed_send_packs_exactly_what_was_chosen_as_a_valid_bundle() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.toggle_share(Indicator.ORTHOSTATIC_HR_DELTA)
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    assert state.outbox == [item]
    assert check_bundle(item.bundle) == []
    assert kinds(item.bundle) == ["Patient"] + ["Observation"] * 4  # 2 readings + 2 states
    assert (item.readings, item.states) == (2, 2)
    assert set(item.indicators) == {Indicator.RESTING_HR, Indicator.ORTHOSTATIC_HR_DELTA}
    text = str(item.bundle)
    assert "systolic_bp" not in text  # what was not chosen is not in the package
    assert "mood" not in text


def test_the_package_is_about_the_person_who_confirmed_and_nobody_else() -> None:
    state = start("AST-0002", "R+2")
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    patient = item.bundle["entry"][0]["resource"]
    assert patient["identifier"][0]["value"] == "crew-02"
    assert item.crew_id == "crew-02"


def test_after_sending_the_selection_and_the_confirmation_are_cleared() -> None:
    state = start()
    state.select_attention()
    state.set_share_confirmed(True)
    state.send_to_ground()
    assert state.share_selection == set()
    assert not state.share_confirmed


def test_the_package_is_stamped_with_the_simulated_time_and_a_delay() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    assert item.sent_at == state.journey_time()
    assert item.arrives_at == item.sent_at + timedelta(minutes=state.ground_delay_minutes)
    assert 3 <= state.ground_delay_minutes <= 22  # the range of D-018
    assert item.bundle["timestamp"].startswith(item.sent_at.strftime("%Y-%m-%dT%H:%M"))


def test_a_package_is_in_transit_until_the_simulated_time_reaches_its_arrival() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    assert delivery_state(item, item.sent_at) is DeliveryState.IN_TRANSIT
    assert delivery_state(item, item.arrives_at - timedelta(seconds=1)) is DeliveryState.IN_TRANSIT
    assert delivery_state(item, item.arrives_at) is DeliveryState.DELIVERED
    assert state.ground_inbox == []


def test_advancing_the_journey_delivers_it_to_the_ground_inbox() -> None:
    state = start(label="R+1")
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    assert state.delivered() == ()
    state.advance()
    assert state.delivered() == (item,)
    assert state.ground_inbox == [item]
    state.advance()  # it is delivered once, not again
    assert state.ground_inbox == [item]


def test_each_astronaut_only_sees_their_own_packages() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    state.send_to_ground()
    assert len(state.own_outbox()) == 1
    state.logout()
    state.login("AST-0002")
    assert state.own_outbox() == ()


def test_logging_out_forgets_an_unsent_selection() -> None:
    state = start()
    state.toggle_share(Indicator.RESTING_HR)
    state.set_share_confirmed(True)
    state.logout()
    assert state.share_selection == set()
    assert not state.share_confirmed
    assert state.outbox == []
