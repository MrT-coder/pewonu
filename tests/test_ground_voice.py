"""T2 on the ground: the voice pattern as change versus the person's own usual."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from crew_self_check.core.contract import CrewProfile, Environment, Sex, VoiceFeatures
from crew_self_check.core.fhir import ShareSelection, build_bundle
from crew_self_check.core.inbox import InMemoryBundleInbox
from crew_self_check.core.voice_baseline import compare
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import DEFAULT_DELAY_MINUTES, GroundService
from crew_self_check.ground.view_model import build_crew_view

PROFILE = CrewProfile("crew-03", 33, Sex.MALE, "simulated-clinical-history")
T0 = datetime(2026, 11, 22, 12, 0, tzinfo=UTC)
LATER = T0 + timedelta(minutes=DEFAULT_DELAY_MINUTES)
USUAL = {
    "durationSeconds": 45.0,
    "pitchMeanHz": 118.0,
    "pitchVariation": 2.4,
    "speechRate": 4.5,
    "pauseRatio": 0.22,
    "loudnessDb": -23.0,
}
SLOW = {**USUAL, "speechRate": 3.0, "pauseRatio": 0.4}


def _bundle(features: dict[str, float], day: int = 0) -> dict[str, Any]:
    earlier = [
        VoiceFeatures(
            "crew-03", datetime(2026, 11, 1 + i, 12, tzinfo=UTC), Environment.EARTH, USUAL, 4
        )
        for i in range(8)
    ]
    note = VoiceFeatures("crew-03", T0 + timedelta(days=day), Environment.SPACECRAFT, features, 3)
    selection = ShareSelection(
        PROFILE, True, T0 + timedelta(days=day), (), (), voice=((note, compare(earlier, note)),)
    )
    return build_bundle(selection)


@pytest.fixture
def service() -> GroundService:
    ground = GroundService(InMemoryBundleInbox())
    ground.set_clock(T0)
    return ground


@pytest.fixture
def client(service: GroundService) -> TestClient:
    return TestClient(create_app(service))


def test_the_view_model_reads_the_level_the_place_and_what_changed(service: GroundService) -> None:
    service.receive(_bundle(SLOW))
    view = build_crew_view("crew-03", service.visible(LATER))
    assert view is not None
    (row,) = view.voice
    assert row.level == "different"
    assert row.environment == "spacecraft"
    assert row.reference == "transition"
    assert row.baseline_environment == "earth"
    assert dict(row.changed) == {"speechRate": "down", "pauseRatio": "up"}


def test_a_crew_member_with_only_a_voice_note_still_has_a_page(
    client: TestClient, service: GroundService
) -> None:
    client.post("/bundles", json=_bundle(SLOW))
    service.set_clock(LATER)
    page = client.get("/crew/crew-03")
    assert page.status_code == 200
    assert "Voice pattern" in page.text
    assert "slower" in page.text and "more pauses" in page.text


def test_the_page_says_it_is_numbers_only_and_experimental(
    client: TestClient, service: GroundService
) -> None:
    client.post("/bundles", json=_bundle(SLOW))
    service.set_clock(LATER)
    text = client.get("/crew/crew-03").text.lower()
    assert "experimental" in text
    assert "never sent" in text
    assert "emotion" in text  # only to say that none is inferred
    assert "sad" not in text and "anxious" not in text and "depress" not in text


def test_the_page_is_in_spanish_too(client: TestClient, service: GroundService) -> None:
    client.post("/bundles", json=_bundle(SLOW))
    service.set_clock(LATER)
    page = client.get("/crew/crew-03", params={"lang": "es"}).text
    assert "Patrón de voz" in page
    assert "más lento" in page and "más pausas" in page


def test_a_usual_note_says_usual(client: TestClient, service: GroundService) -> None:
    client.post("/bundles", json=_bundle(USUAL))
    service.set_clock(LATER)
    page = client.get("/crew/crew-03").text
    assert "Like their usual" in page


def test_the_voice_notes_are_listed_oldest_first(service: GroundService) -> None:
    service.receive(_bundle(SLOW, day=2))
    service.receive(_bundle(USUAL, day=0))
    view = build_crew_view("crew-03", service.visible(T0 + timedelta(days=5)))
    assert view is not None
    assert [r.level for r in view.voice] == ["usual", "different"]


def test_voice_does_not_appear_among_the_readings(
    client: TestClient, service: GroundService
) -> None:
    client.post("/bundles", json=_bundle(SLOW))
    service.set_clock(LATER)
    view = build_crew_view("crew-03", service.visible(LATER))
    assert view is not None
    assert view.readings == ()
    assert view.states == ()
