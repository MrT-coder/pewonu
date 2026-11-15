"""G3: the ground view shows only what the astronaut sent, per crew member, in es and en."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from crew_self_check.core.inbox import InMemoryBundleInbox
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import DEFAULT_DELAY_MINUTES, GroundService
from crew_self_check.ground.view_model import build_crew_view

T0 = datetime(2026, 11, 14, 19, 30, tzinfo=UTC)
LATER = T0 + timedelta(minutes=DEFAULT_DELAY_MINUTES)


@pytest.fixture
def service() -> GroundService:
    ground = GroundService(InMemoryBundleInbox())
    ground.set_clock(T0)
    return ground


@pytest.fixture
def client(service: GroundService) -> TestClient:
    return TestClient(create_app(service))


def test_the_view_model_has_a_state_for_every_indicator_that_was_sent(
    service: GroundService, bundle: dict[str, Any]
) -> None:
    service.receive(bundle)
    view = build_crew_view("crew-01", service.visible(LATER))
    assert len(view.states) == 11
    assert {s.status for s in view.states} <= {"ok", "watch", "act", "insufficient_data"}
    assert all(s.reason for s in view.states)
    assert len(view.readings) == 11
    assert view.bundles == 1


def test_the_latest_state_of_an_indicator_wins(
    service: GroundService, bundle: dict[str, Any]
) -> None:
    service.receive(bundle)
    first = build_crew_view("crew-01", service.visible(LATER))
    assert len({(s.indicator, s.environment) for s in first.states}) == len(first.states)


def test_home_says_what_it_is_and_shows_no_crew_before_anything_arrives(
    client: TestClient, bundle: dict[str, Any]
) -> None:
    client.post("/bundles", json=bundle)
    page = client.get("/")
    assert page.status_code == 200
    assert "text/html" in page.headers["content-type"]
    assert "Nothing has arrived yet" in page.text
    assert "crew-01" not in page.text


def test_home_lists_the_crew_once_the_delay_has_passed(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    client.post("/bundles", json=bundle)
    service.set_clock(LATER)
    page = client.get("/")
    assert "crew-01" in page.text
    assert "/crew/crew-01" in page.text


def test_the_crew_page_shows_states_readings_and_the_limits(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    client.post("/bundles", json=bundle)
    service.set_clock(LATER)
    page = client.get("/crew/crew-01")
    assert page.status_code == 200
    assert "Resting heart rate" in page.text
    assert "simulated" in page.text.lower()
    assert "not a diagnosis" in page.text.lower()


def test_the_crew_page_is_empty_for_someone_who_sent_nothing(client: TestClient) -> None:
    assert client.get("/crew/crew-99").status_code == 404


def test_the_crew_page_hides_what_has_not_arrived(
    client: TestClient, bundle: dict[str, Any]
) -> None:
    client.post("/bundles", json=bundle)
    assert client.get("/crew/crew-01").status_code == 404


def test_spanish_is_available_for_every_page(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    client.post("/bundles", json=bundle)
    assert "Aún no ha llegado nada" in client.get("/", params={"lang": "es"}).text
    service.set_clock(LATER)
    page = client.get("/crew/crew-01", params={"lang": "es"})
    assert "no es un diagnóstico" in page.text.lower()
    assert 'lang="es"' in page.text


def test_an_unknown_language_falls_back_to_english(client: TestClient) -> None:
    assert 'lang="en"' in client.get("/", params={"lang": "xx"}).text


def test_text_from_a_bundle_is_escaped(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    status = next(
        e["resource"]
        for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation" and "note" in e["resource"]
    )
    status["note"] = [{"text": "<script>alert(1)</script>"}]
    client.post("/bundles", json=bundle)
    service.set_clock(LATER)
    page = client.get("/crew/crew-01")
    assert "<script>alert(1)</script>" not in page.text
    assert "&lt;script&gt;" in page.text


# --- findings of the QA gate (2026-11-14) -------------------------------------------------------


def _arrived(client: TestClient, service: GroundService, bundle: dict[str, Any]) -> None:
    client.post("/bundles", json=bundle)
    service.set_clock(LATER)


def test_pages_do_not_force_a_timed_refresh(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    """WCAG 2.2.1: no <meta http-equiv=refresh>; the person refreshes with a visible link."""
    _arrived(client, service, bundle)
    for path in ("/", "/crew/crew-01"):
        page = client.get(path).text
        assert "http-equiv" not in page
        assert "Refresh" in page


def test_pages_declare_an_icon_so_the_browser_does_not_ask_for_one(client: TestClient) -> None:
    assert 'rel="icon"' in client.get("/").text


def test_readings_use_the_language_of_the_page(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    _arrived(client, service, bundle)
    page = client.get("/crew/crew-01", params={"lang": "es"}).text
    assert "Sueño" in page  # a reading, not only a state
    assert "Sleep duration" not in page
    assert "Resting heart rate" not in page


def test_times_are_readable_not_raw_iso(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    _arrived(client, service, bundle)
    page = client.get("/crew/crew-01").text
    assert "2026-11-14T07:30:00Z" not in page
    assert "2026-11-14 07:30 UTC" in page


def test_the_origin_of_a_reading_is_labelled_as_simulated(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    _arrived(client, service, bundle)
    assert "Simulated scenario" in client.get("/crew/crew-01").text
    assert "Escenario simulado" in client.get("/crew/crew-01", params={"lang": "es"}).text


def test_one_package_is_not_called_packages(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    _arrived(client, service, bundle)
    assert "1 package received" in client.get("/crew/crew-01").text
    assert "1 paquete recibido" in client.get("/crew/crew-01", params={"lang": "es"}).text


def test_temperature_shows_the_degree_sign(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    _arrived(client, service, bundle)
    assert "36.6 °C" in client.get("/crew/crew-01").text


def test_the_indicator_of_a_coding_is_found_by_loinc_or_by_local_code() -> None:
    from crew_self_check.core.contract import Indicator
    from crew_self_check.core.fhir import LOCAL_INDICATOR, LOINC, indicator_from_coding

    assert indicator_from_coding(LOINC, "8867-4") is Indicator.RESTING_HR
    assert indicator_from_coding(LOCAL_INDICATOR, "sleep_hours") is Indicator.SLEEP_HOURS
    assert indicator_from_coding(LOINC, "0000-0") is None


def test_scrollable_tables_can_be_reached_with_the_keyboard(
    client: TestClient, service: GroundService, bundle: dict[str, Any]
) -> None:
    """WCAG 2.1.1: a region that scrolls at phone width needs focus, a role and a name."""
    _arrived(client, service, bundle)
    page = client.get("/crew/crew-01").text
    assert page.count('class="table-wrap" tabindex="0" role="region"') == 2
    assert 'aria-label="State by indicator"' in page
    assert 'aria-label="Latest readings sent"' in page


def test_an_unknown_crew_page_is_a_readable_page_not_raw_json(client: TestClient) -> None:
    page = client.get("/crew/crew-99")
    assert page.status_code == 404
    assert "text/html" in page.headers["content-type"]
    assert "Nothing from this crew member has arrived" in page.text
    assert 'href="/?lang=en"' in page.text
    assert (
        "Nada de este tripulante ha llegado"
        in client.get("/crew/crew-99", params={"lang": "es"}).text
    )
