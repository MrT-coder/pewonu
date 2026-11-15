"""G1: the ground receives only a valid, consented FHIR bundle and says clearly what is wrong."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from crew_self_check.ground.ingest import InvalidBundle, inspect_bundle


def test_a_real_bundle_is_accepted(bundle: dict[str, Any]) -> None:
    parts = inspect_bundle(bundle)
    assert parts.crew_id == "crew-01"
    assert parts.sent_at == datetime(2026, 11, 14, 19, 30, tzinfo=UTC)
    assert parts.readings == 11
    assert parts.states == 11
    assert parts.bundle_id == bundle["id"]


def _problems(bundle: dict[str, Any]) -> list[str]:
    with pytest.raises(InvalidBundle) as caught:
        inspect_bundle(bundle)
    return caught.value.problems


def test_something_that_is_not_a_bundle_is_rejected() -> None:
    assert any("Bundle" in p for p in _problems({"resourceType": "Patient"}))


def test_an_empty_bundle_is_rejected(bundle: dict[str, Any]) -> None:
    bundle["entry"] = []
    assert any("empty" in p for p in _problems(bundle))


def test_a_bundle_without_a_patient_is_rejected(bundle: dict[str, Any]) -> None:
    bundle["entry"] = [e for e in bundle["entry"] if e["resource"]["resourceType"] != "Patient"]
    assert any("Patient" in p for p in _problems(bundle))


def test_two_patients_are_rejected(bundle: dict[str, Any]) -> None:
    bundle["entry"].append(bundle["entry"][0])
    assert any("exactly one Patient" in p for p in _problems(bundle))


def test_a_patient_with_a_name_or_birth_date_is_rejected(bundle: dict[str, Any]) -> None:
    bundle["entry"][0]["resource"]["name"] = [{"family": "Doe"}]
    bundle["entry"][0]["resource"]["birthDate"] = "1990-01-01"
    problems = _problems(bundle)
    assert any("name" in p for p in problems)
    assert any("birthDate" in p for p in problems)


def test_a_resource_type_the_astronaut_never_sends_is_rejected(bundle: dict[str, Any]) -> None:
    bundle["entry"].append(
        {"fullUrl": "urn:uuid:x", "resource": {"resourceType": "DocumentReference", "id": "x"}}
    )
    assert any("DocumentReference" in p for p in _problems(bundle))


def test_a_bundle_without_a_timestamp_is_rejected(bundle: dict[str, Any]) -> None:
    del bundle["timestamp"]
    assert any("timestamp" in p for p in _problems(bundle))


def test_a_timestamp_without_a_zone_is_rejected(bundle: dict[str, Any]) -> None:
    bundle["timestamp"] = "2026-11-14T19:30:00"
    assert any("timestamp" in p for p in _problems(bundle))


def test_an_observation_about_someone_else_is_rejected(bundle: dict[str, Any]) -> None:
    observation = next(e for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation")
    observation["resource"]["subject"]["reference"] = "urn:uuid:not-in-this-bundle"
    assert any("does not resolve" in p for p in _problems(bundle))


def test_every_problem_is_reported_not_only_the_first(bundle: dict[str, Any]) -> None:
    del bundle["timestamp"]
    bundle["entry"][0]["resource"]["name"] = [{"family": "Doe"}]
    assert len(_problems(bundle)) >= 2
