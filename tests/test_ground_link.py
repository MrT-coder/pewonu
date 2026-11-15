"""A10 + G1: the app sends the confirmed package to the ground; if it cannot, nothing is lost."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.ground_client import GroundRejected, GroundUnreachable
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.fhir import ConsentRequired


class FakeLink:
    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []
        self.clocks: list[datetime] = []
        self.down = False
        self.refuse: list[str] | None = None
        self.delay = timedelta(minutes=7)

    def sync_clock(self, moment: datetime) -> None:
        if self.down:
            raise GroundUnreachable("down")
        self.clocks.append(moment)

    def send(self, bundle: dict[str, Any]) -> datetime:
        if self.down:
            raise GroundUnreachable("down")
        if self.refuse is not None:
            raise GroundRejected(self.refuse)
        self.sent.append(bundle)
        return self.clocks[-1] + self.delay


def _state(link: FakeLink) -> AppState:
    state = AppState(simulated_directory(), ground_link=link)
    state.login(state.demo_codes()[0])
    state.select_all()
    state.set_share_confirmed(True)
    return state


def test_a_confirmed_package_goes_to_the_ground_with_its_real_arrival_time() -> None:
    link = FakeLink()
    state = _state(link)
    item = state.send_to_ground()
    assert link.sent == [item.bundle]
    assert item.arrives_at == item.sent_at + timedelta(minutes=7)  # the ground decides
    assert state.ground_error is None


def test_the_ground_clock_follows_the_journey() -> None:
    link = FakeLink()
    state = _state(link)
    state.advance()
    assert link.clocks[-1] == state.journey_time()


def test_nothing_is_sent_without_confirmation() -> None:
    link = FakeLink()
    state = _state(link)
    state.set_share_confirmed(False)
    with pytest.raises(ConsentRequired):
        state.send_to_ground()
    assert link.sent == []


def test_if_the_ground_is_unreachable_the_package_is_kept_and_the_error_is_shown() -> None:
    link = FakeLink()
    link.down = True
    state = _state(link)
    item = state.send_to_ground()
    assert state.ground_error == "unreachable"
    assert item in state.outbox
    assert state.unsent_to_ground() == (item,)


def test_the_package_is_sent_again_when_the_ground_comes_back() -> None:
    link = FakeLink()
    link.down = True
    state = _state(link)
    item = state.send_to_ground()
    link.down = False
    state.advance()
    assert link.sent == [item.bundle]
    assert state.unsent_to_ground() == ()
    assert state.ground_error is None


def test_a_package_the_ground_refuses_is_reported_and_not_queued() -> None:
    link = FakeLink()
    link.refuse = ["timestamp: required"]
    state = _state(link)
    with pytest.raises(RuntimeError, match="timestamp: required"):
        state.send_to_ground()
    assert state.outbox == []


def test_without_a_link_the_simulated_inbox_still_works() -> None:
    state = AppState(simulated_directory())
    state.login(state.demo_codes()[0])
    state.select_all()
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    assert item.arrives_at == item.sent_at + timedelta(minutes=state.ground_delay_minutes)
    assert state.ground_error is None
