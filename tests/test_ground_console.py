"""T3: the ground console puts what needs attention first and shows trends with the usual band."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.inbox import InMemoryBundleInbox
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import DEFAULT_DELAY_MINUTES, GroundService
from crew_self_check.ground.view_model import build_crew_view, system_levels

T0 = datetime(2026, 12, 1, 12, 0, tzinfo=UTC)
LATER = T0 + timedelta(minutes=DEFAULT_DELAY_MINUTES)


def bundle_at(code: str, day: str) -> dict[str, Any]:
    state = AppState(simulated_directory())
    state.login(code)
    state.set_day(next(d.index for d in state.scenario.days if d.label == day))
    state.select_all()
    state.set_share_confirmed(True)
    return state.send_to_ground().bundle  # type: ignore[no-any-return]


@pytest.fixture
def service() -> GroundService:
    ground = GroundService(InMemoryBundleInbox())
    ground.set_clock(T0)
    return ground


@pytest.fixture
def client(service: GroundService) -> TestClient:
    return TestClient(create_app(service))


def _send(client: TestClient, service: GroundService, *bundles: dict[str, Any]) -> None:
    for bundle in bundles:
        client.post("/bundles", json=bundle)
    service.set_clock(LATER)


def test_the_status_carries_the_usual_band_and_the_recent_trend(service: GroundService) -> None:
    service.receive(bundle_at("AST-0001", "E-1"))
    view = build_crew_view("crew-01", service.visible(LATER))
    assert view is not None
    pulse = next(s for s in view.states if s.indicator == "resting_hr")
    assert pulse.low is not None and pulse.high is not None and pulse.low < pulse.high
    assert len(pulse.trend) == 3
    assert all(isinstance(value, float) for _, value in pulse.trend)


def test_a_state_without_a_baseline_has_no_band(service: GroundService) -> None:
    service.receive(bundle_at("AST-0002", "R+2"))
    view = build_crew_view("crew-02", service.visible(LATER))
    assert view is not None
    pulse = next(s for s in view.states if s.indicator == "resting_hr")
    assert pulse.low is None and pulse.high is None


def test_the_crew_page_draws_a_trend_with_the_band_and_a_text_alternative(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0001", "E-1"))
    page = client.get("/crew/crew-01").text
    assert "<svg" in page
    assert 'role="img"' in page
    assert "usual range" in page.lower()


def test_the_trend_is_in_spanish_too(client: TestClient, service: GroundService) -> None:
    _send(client, service, bundle_at("AST-0001", "E-1"))
    page = client.get("/crew/crew-01", params={"lang": "es"}).text
    assert "rango habitual" in page.lower()


def test_the_system_levels_use_the_worst_indicator_of_each_system(service: GroundService) -> None:
    service.receive(bundle_at("AST-0003", "T+6"))
    view = build_crew_view("crew-03", service.visible(LATER))
    assert view is not None
    levels = system_levels(view)
    assert levels["sleep_brain"] == "watch"
    assert levels["mood"] == "watch"
    assert levels["cardiovascular"] in ("ok", "insufficient_data")
    assert "bone_muscle" not in levels  # nothing measured for it


def test_the_home_shows_the_systems_of_each_crew_member_and_who_needs_attention_first(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0001", "E-1"), bundle_at("AST-0002", "R+2"))
    page = client.get("/").text
    assert "Needs attention" in page
    assert page.index("crew-02") < page.index("crew-01")  # the red one comes first
    assert "Flight surgeon review" in page  # the suggestion the astronaut app made


def test_a_crew_member_in_range_is_not_pushed_up(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0001", "E-1"))
    page = client.get("/").text
    assert "Nothing outside the usual range" in page


def test_the_crew_page_leads_with_what_needs_attention_and_why(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0002", "R+2"))
    page = client.get("/crew/crew-02").text
    assert page.index("Needs attention") < page.index("State by indicator")
    assert "Red" in page
    assert "Flight surgeon review" in page


def test_the_alert_names_each_crew_member_only_under_its_own_level(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0001", "R+2"), bundle_at("AST-0002", "R+2"))
    page = client.get("/").text
    assert "Flight surgeon review suggested for crew-02" in page
    assert "Crew medical officer suggested for crew-01" in page
    assert "Flight surgeon review suggested for crew-02, crew-01" not in page


def test_when_everyone_is_in_range_the_alert_says_so(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0001", "E-1"))
    assert "Everyone is within their usual range." in client.get("/").text


def test_the_home_has_the_indicator_strip_of_the_whole_crew(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0001", "E-1"), bundle_at("AST-0002", "R+2"))
    page = client.get("/").text
    for label in ("Crew members", "Need attention", "Packages received", "Communication delay"):
        assert label in page
    assert page.count('class="glass kpi"') == 5


def test_every_crew_member_has_the_body_figure_with_a_text_alternative(
    client: TestClient, service: GroundService
) -> None:
    _send(client, service, bundle_at("AST-0003", "T+6"))
    page = client.get("/crew/crew-03").text
    assert 'class="figure"' in page
    assert "Sleep and brain: outside" in page  # the aria-label of the figure
    assert "Bone and muscle: not measured" in page
    assert "Cardiovascular: in range" in page


def test_the_figure_is_in_spanish_too(client: TestClient, service: GroundService) -> None:
    _send(client, service, bundle_at("AST-0003", "T+6"))
    page = client.get("/crew/crew-03", params={"lang": "es"}).text
    assert "Sueño y cerebro: fuera de rango" in page
    assert "Hueso y músculo: sin medir" in page
