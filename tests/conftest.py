"""Shared fixtures: a real bundle, built by the astronaut flow exactly as the app sends it."""

from __future__ import annotations

import copy
from typing import Any

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.state import AppState


def _sent_item(code_index: int = 0) -> Any:
    state = AppState(simulated_directory())
    state.login(state.demo_codes()[code_index])
    if code_index:  # crew-02 has no history: it only has readings late in the journey
        state.set_day(len(state.scenario.days) - 1)
    state.select_all()
    state.set_share_confirmed(True)
    return state.send_to_ground()


@pytest.fixture
def sent_item() -> Any:
    return _sent_item()


@pytest.fixture
def bundle(sent_item: Any) -> dict[str, Any]:
    return copy.deepcopy(sent_item.bundle)  # type: ignore[no-any-return]


@pytest.fixture
def other_crew_bundle() -> dict[str, Any]:
    return copy.deepcopy(_sent_item(1).bundle)  # type: ignore[no-any-return]
