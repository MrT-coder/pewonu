"""T8: the crew profile carries the body data that WOD and Nutrition use (simulated, preflight)."""

from __future__ import annotations

import pytest

from crew_self_check.core.contract import ContractError, CrewProfile, Sex
from crew_self_check.core.scenario import CREW


def test_the_profile_keeps_its_old_shape_when_there_is_no_body_data() -> None:
    profile = CrewProfile("crew-09", 40, Sex.FEMALE, "simulated-no-history")
    assert profile.to_dict() == {
        "crewId": "crew-09",
        "age": 40,
        "sex": "female",
        "baselineSource": "simulated-no-history",
    }
    assert profile.weight_kg is None and profile.height_cm is None
    assert CrewProfile.from_dict(profile.to_dict()) == profile


def test_body_data_round_trips_through_the_contract() -> None:
    profile = CrewProfile("crew-09", 40, Sex.MALE, "x", 80.5, 178.0, 1.12)
    data = profile.to_dict()
    assert data["weightKg"] == 80.5
    assert data["heightCm"] == 178.0
    assert data["boneMineralDensity"] == 1.12
    assert CrewProfile.from_dict(data) == profile


@pytest.mark.parametrize("field", ["weightKg", "heightCm", "boneMineralDensity"])
@pytest.mark.parametrize("bad", [0, -1, "heavy"])
def test_body_data_must_be_a_positive_number(field: str, bad: object) -> None:
    data = CrewProfile("crew-09", 40, Sex.MALE, "x", 80.0, 178.0, 1.1).to_dict()
    data[field] = bad
    with pytest.raises(ContractError):
        CrewProfile.from_dict(data)


def test_every_demo_astronaut_has_simulated_body_data() -> None:
    for profile in CREW:
        assert profile.weight_kg is not None and 40 < profile.weight_kg < 150
        assert profile.height_cm is not None and 140 < profile.height_cm < 210
        assert profile.bone_mineral_density is not None and 0.6 < profile.bone_mineral_density < 1.6
        assert "simulated" in profile.baseline_source


def test_the_three_demo_astronauts_are_different_bodies() -> None:
    assert len({(p.weight_kg, p.height_cm, p.bone_mineral_density) for p in CREW}) == 3
