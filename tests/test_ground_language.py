"""The ground base shows one language at a time: bundle texts are localized when rendered."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.inbox import InMemoryBundleInbox
from crew_self_check.core.reasons import Language, localize_reason
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import DEFAULT_DELAY_MINUTES, GroundService

T0 = datetime(2026, 12, 1, 12, 0, tzinfo=UTC)
LATER = T0 + timedelta(minutes=DEFAULT_DELAY_MINUTES)


def test_a_reason_without_parameters_is_translated_both_ways() -> None:
    assert (
        localize_reason("Within your personal range.", Language.ES)
        == "Dentro de tu rango personal."
    )
    assert (
        localize_reason("Dentro de tu rango personal.", Language.EN)
        == "Within your personal range."
    )


def test_a_reason_with_parameters_keeps_its_values() -> None:
    text = "No recent reading: the latest is 6 days old."
    assert localize_reason(text, Language.ES) == "Sin lectura reciente: la última tiene 6 días."
    assert localize_reason("3 consecutive readings above personal range", Language.ES) == (
        "3 lecturas seguidas por encima de tu rango personal"
    )


def test_an_environment_inside_a_reason_is_translated_too() -> None:
    en = "Within your previous baseline (Earth); your own baseline here is still building."
    assert "(Tierra)" in localize_reason(en, Language.ES)


def test_an_unknown_text_is_left_alone() -> None:
    assert localize_reason("Something else entirely", Language.ES) == "Something else entirely"


@pytest.fixture
def client() -> TestClient:
    service = GroundService(InMemoryBundleInbox())
    service.set_clock(T0)
    state = AppState(simulated_directory())
    state.login("AST-0001")
    state.set_day(next(d.index for d in state.scenario.days if d.label == "E-1"))
    state.select_all()
    state.set_share_confirmed(True)
    service.receive(state.send_to_ground().bundle)
    service.set_clock(LATER)
    return TestClient(create_app(service))


ENGLISH_LEFTOVERS = ("Within your personal range", "beats/minute", " hours", "No recent reading")


def test_the_spanish_page_has_no_english_fragments(client: TestClient) -> None:
    page = client.get("/crew/crew-01?lang=es").text
    for fragment in ENGLISH_LEFTOVERS:
        assert fragment not in page, fragment
    assert "Dentro de tu rango personal" in page
    assert "latidos/min" in page
    assert ">sí<" in page or "sí " in page


def test_the_english_page_keeps_english_units(client: TestClient) -> None:
    page = client.get("/crew/crew-01?lang=en").text
    assert "Within your personal range" in page
    assert "beats/minute" in page
    assert "Dentro de tu rango" not in page
