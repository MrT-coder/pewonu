"""The two systems together over real HTTP: astronaut app state -> ground service -> ground view."""

from __future__ import annotations

import socket
import threading
import time
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest
import uvicorn

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.ground_client import (
    GroundRejected,
    GroundUnreachable,
    HttpGroundLink,
)
from crew_self_check.astronaut.state import AppState
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import GroundService
from crew_self_check.ground.sqlite_inbox import SqliteBundleInbox


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture
def ground(tmp_path: Path) -> Iterator[str]:
    service = GroundService(SqliteBundleInbox(tmp_path / "ground.db"))
    port = _free_port()
    server = uvicorn.Server(
        uvicorn.Config(create_app(service), host="127.0.0.1", port=port, log_level="error")
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    assert server.started, "the ground server did not start"
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)


def test_the_whole_journey_of_a_package(ground: str) -> None:
    state = AppState(simulated_directory(), ground_link=HttpGroundLink(ground))
    state.login(state.demo_codes()[0])
    state.select_all()
    state.set_share_confirmed(True)
    item = state.send_to_ground()
    assert state.ground_error is None

    # In transit: the ground sees nothing yet.
    assert httpx.get(f"{ground}/bundles").json() == []
    assert "Nothing has arrived yet" in httpx.get(f"{ground}/").text

    # The journey moves on past the delay: the package is on the ground.
    for _ in range(3):
        state.advance()
    listed = httpx.get(f"{ground}/bundles").json()
    assert [b["id"] for b in listed] == [item.bundle["id"]]
    page = httpx.get(f"{ground}/crew/crew-01", params={"lang": "es"})
    assert page.status_code == 200
    assert "Pulso en reposo" in page.text


def test_a_down_ground_is_reported_as_unreachable() -> None:
    link = HttpGroundLink(f"http://127.0.0.1:{_free_port()}", timeout=0.5)
    with pytest.raises(GroundUnreachable):
        link.sync_clock(datetime.now(UTC))


def test_a_refused_bundle_carries_the_reasons(ground: str) -> None:
    with pytest.raises(GroundRejected) as caught:
        HttpGroundLink(ground).send({"resourceType": "Bundle", "type": "collection", "entry": []})
    assert caught.value.problems
