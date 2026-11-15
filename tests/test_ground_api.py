"""G1/G2 over HTTP: post a bundle, get a clear error for a bad one, see it after the delay."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from crew_self_check.core.inbox import InMemoryBundleInbox
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import DEFAULT_DELAY_MINUTES, GroundService

T0 = datetime(2026, 11, 14, 19, 30, tzinfo=UTC)


@pytest.fixture
def service() -> GroundService:
    ground = GroundService(InMemoryBundleInbox(), clock=lambda: T0)
    ground.set_clock(T0)
    return ground


@pytest.fixture
def client(service: GroundService) -> TestClient:
    return TestClient(create_app(service))


def _arrives(minutes: int = DEFAULT_DELAY_MINUTES) -> str:
    return (T0 + timedelta(minutes=minutes)).isoformat()


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok", "system": "ground"}


def test_a_valid_bundle_is_accepted_and_told_when_it_arrives(
    client: TestClient, bundle: dict[str, Any]
) -> None:
    response = client.post("/bundles", json=bundle)
    assert response.status_code == 202
    body = response.json()
    assert body["id"] == bundle["id"]
    assert body["crewId"] == "crew-01"
    assert body["availableAt"] == _arrives()
    assert body["delayMinutes"] == DEFAULT_DELAY_MINUTES


def test_an_invalid_bundle_is_rejected_with_every_reason(
    client: TestClient, bundle: dict[str, Any]
) -> None:
    del bundle["timestamp"]
    bundle["entry"][0]["resource"]["name"] = [{"family": "Doe"}]
    response = client.post("/bundles", json=bundle)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["message"] == "invalid FHIR bundle"
    assert len(detail["problems"]) >= 2


def test_a_body_that_is_not_an_object_is_rejected(client: TestClient) -> None:
    assert client.post("/bundles", json=[1, 2]).status_code == 422
    assert client.post("/bundles", content="not json").status_code == 422


def test_nothing_is_listed_before_the_delay_and_it_is_after(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    client.post("/bundles", json=bundle)
    assert client.get("/bundles").json() == []
    assert client.get(f"/bundles/{bundle['id']}").status_code == 404
    service.set_clock(T0 + timedelta(minutes=DEFAULT_DELAY_MINUTES))
    listed = client.get("/bundles").json()
    assert [b["id"] for b in listed] == [bundle["id"]]
    assert listed[0]["readings"] == 11
    assert client.get(f"/bundles/{bundle['id']}").json() == bundle


def test_the_list_can_be_filtered_by_crew(
    client: TestClient,
    service: GroundService,
    bundle: dict[str, Any],
    other_crew_bundle: dict[str, Any],
) -> None:
    client.post("/bundles", json=bundle)
    client.post("/bundles", json=other_crew_bundle)
    service.set_clock(T0 + timedelta(days=1))
    assert len(client.get("/bundles").json()) == 2
    assert [b["crewId"] for b in client.get("/bundles", params={"crew": "crew-02"}).json()] == [
        "crew-02"
    ]


def test_the_delay_is_configurable_over_http(client: TestClient, bundle: dict[str, Any]) -> None:
    assert client.get("/config").json() == {"delayMinutes": DEFAULT_DELAY_MINUTES}
    assert client.put("/config", json={"delayMinutes": 3}).json() == {"delayMinutes": 3}
    assert client.post("/bundles", json=bundle).json()["availableAt"] == _arrives(3)


@pytest.mark.parametrize("minutes", [-1, 61, "ten"])
def test_a_bad_delay_is_rejected_and_nothing_changes(client: TestClient, minutes: object) -> None:
    assert client.put("/config", json={"delayMinutes": minutes}).status_code == 422
    assert client.get("/config").json() == {"delayMinutes": DEFAULT_DELAY_MINUTES}


def test_the_simulated_clock_can_be_set_and_cleared(
    client: TestClient, service: GroundService
) -> None:
    moment = "2026-12-01T08:00:00+00:00"
    assert client.put("/clock", json={"now": moment}).json() == {"now": moment, "simulated": True}
    assert service.now() == datetime(2026, 12, 1, 8, 0, tzinfo=UTC)
    assert client.delete("/clock").json()["simulated"] is False


def test_a_clock_without_a_zone_is_rejected(client: TestClient) -> None:
    assert client.put("/clock", json={"now": "2026-12-01T08:00:00"}).status_code == 422
