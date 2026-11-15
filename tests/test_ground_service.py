"""G2: what was sent shows up on the ground only after the (configurable) communication delay."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from crew_self_check.core.inbox import BundleInbox, InMemoryBundleInbox
from crew_self_check.ground.ingest import InvalidBundle
from crew_self_check.ground.service import (
    DEFAULT_DELAY_MINUTES,
    MAX_DELAY_MINUTES,
    GroundService,
)
from crew_self_check.ground.sqlite_inbox import SqliteBundleInbox

SENT = datetime(2026, 11, 14, 19, 30, tzinfo=UTC)


@pytest.fixture(params=["memory", "sqlite"])
def inbox(request: pytest.FixtureRequest, tmp_path: Path) -> BundleInbox:
    if request.param == "memory":
        return InMemoryBundleInbox()
    return SqliteBundleInbox(tmp_path / "ground.db")


def _service(inbox: BundleInbox, now: datetime = SENT) -> GroundService:
    return GroundService(inbox, clock=lambda: now)


def test_the_default_delay_is_inside_the_documented_range(inbox: BundleInbox) -> None:
    assert 3 <= DEFAULT_DELAY_MINUTES <= 22
    assert _service(inbox).delay_minutes == DEFAULT_DELAY_MINUTES


def test_a_received_bundle_is_hidden_until_the_delay_has_passed(
    inbox: BundleInbox, bundle: dict[str, Any]
) -> None:
    service = _service(inbox)
    item = service.receive(bundle)
    assert item.available_at == SENT + timedelta(minutes=DEFAULT_DELAY_MINUTES)
    assert service.visible(SENT) == ()
    assert service.visible(item.available_at - timedelta(seconds=1)) == ()
    assert service.visible(item.available_at) == (item,)


def test_the_delay_is_configurable(inbox: BundleInbox, bundle: dict[str, Any]) -> None:
    service = _service(inbox)
    service.set_delay(3)
    item = service.receive(bundle)
    assert item.available_at == SENT + timedelta(minutes=3)


def test_changing_the_delay_does_not_move_what_is_already_queued(
    inbox: BundleInbox, bundle: dict[str, Any]
) -> None:
    service = _service(inbox)
    first = service.receive(bundle)
    service.set_delay(1)
    assert service.visible(SENT + timedelta(minutes=2)) == ()
    assert first.available_at == SENT + timedelta(minutes=DEFAULT_DELAY_MINUTES)


@pytest.mark.parametrize("minutes", [-1, MAX_DELAY_MINUTES + 1])
def test_a_delay_outside_the_range_is_refused(inbox: BundleInbox, minutes: int) -> None:
    service = _service(inbox)
    with pytest.raises(ValueError, match="delay"):
        service.set_delay(minutes)
    assert service.delay_minutes == DEFAULT_DELAY_MINUTES


def test_zero_delay_is_allowed_for_demos(inbox: BundleInbox, bundle: dict[str, Any]) -> None:
    service = _service(inbox)
    service.set_delay(0)
    assert service.visible_now() == ()
    item = service.receive(bundle)
    assert service.visible(item.available_at) == (item,)


def test_an_invalid_bundle_is_not_stored(inbox: BundleInbox, bundle: dict[str, Any]) -> None:
    service = _service(inbox)
    bundle["entry"] = []
    with pytest.raises(InvalidBundle):
        service.receive(bundle)
    assert service.visible(SENT + timedelta(days=1)) == ()


def test_the_same_bundle_twice_is_stored_once(inbox: BundleInbox, bundle: dict[str, Any]) -> None:
    service = _service(inbox)
    first = service.receive(bundle)
    second = service.receive(bundle)
    assert second == first
    assert len(service.visible(SENT + timedelta(days=1))) == 1


def test_the_clock_can_be_driven_by_the_simulation(
    inbox: BundleInbox, bundle: dict[str, Any]
) -> None:
    service = GroundService(inbox)
    service.set_clock(SENT)
    item = service.receive(bundle)
    assert service.visible_now() == ()
    service.set_clock(item.available_at)
    assert service.visible_now() == (item,)
    service.clear_clock()
    assert service.now() != item.available_at


def test_crews_are_kept_apart(
    inbox: BundleInbox, bundle: dict[str, Any], other_crew_bundle: dict[str, Any]
) -> None:
    service = _service(inbox)
    service.receive(bundle)
    service.receive(other_crew_bundle)
    later = SENT + timedelta(days=1)
    assert {i.crew_id for i in service.visible(later)} == {"crew-01", "crew-02"}
    assert [i.crew_id for i in service.visible(later, crew_id="crew-02")] == ["crew-02"]


def test_what_was_received_survives_a_restart(tmp_path: Path, bundle: dict[str, Any]) -> None:
    path = tmp_path / "ground.db"
    first = SqliteBundleInbox(path)
    item = GroundService(first, clock=lambda: SENT).receive(bundle)
    first.close()
    again = GroundService(SqliteBundleInbox(path), clock=lambda: SENT)
    assert again.visible(item.available_at) == (item,)
