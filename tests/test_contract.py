"""C1: contract 0.3 types. The payloads are the examples of docs/contrato-datos.md."""

import copy
import json
from typing import Any

import pytest

from crew_self_check.core.contract import (
    ContractError,
    CrewProfile,
    IndicatorStatus,
    Measurement,
    SpacecraftProfile,
    SystemStatus,
    VoiceFeatures,
)

MEASUREMENT: dict[str, Any] = {
    "crewId": "crew-01",
    "indicator": "resting_hr",
    "value": 62,
    "unit": "bpm",
    "timestamp": "2026-11-14T07:30:00Z",
    "source": "manual",
    "environment": "earth",
    "method": "palpation",
}

INDICATOR_STATUS: dict[str, Any] = {
    "crewId": "crew-01",
    "indicator": "resting_hr",
    "status": "watch",
    "baseline": {"center": 60, "low": 55, "high": 66, "nDays": 9},
    "latest": 71,
    "trend": [{"timestamp": "2026-11-06T07:30:00Z", "value": 59}],
    "reason": "3 consecutive readings above personal range",
    "escalation": "crew_cmo",
    "environment": "spacecraft",
    "reference": "personal",
}

SYSTEM_STATUS: dict[str, Any] = {
    "crewId": "crew-01",
    "system": "cardiovascular",
    "status": "watch",
    "indicators": ["resting_hr", "systolic_bp", "diastolic_bp"],
}

CREW_PROFILE: dict[str, Any] = {
    "crewId": "crew-01",
    "age": 38,
    "sex": "female",
    "baselineSource": "simulated-clinical-history",
}

VOICE_FEATURES: dict[str, Any] = {
    "crewId": "crew-01",
    "timestamp": "2026-11-20T19:10:00Z",
    "environment": "spacecraft",
    "features": {"pitchMeanHz": 182.4, "jitter": 0.012, "shimmer": 0.061, "speechRate": 3.8},
    "moodSurveyScore": 3,
    "experimental": True,
}

SPACECRAFT_PROFILE: dict[str, Any] = {
    "id": "iss-analog",
    "label": "ISS (analog)",
    "equipment": [{"id": "bp-cuff", "measures": ["systolic_bp", "diastolic_bp"], "mode": "manual"}],
}

CASES: list[tuple[Any, dict[str, Any]]] = [
    (Measurement, MEASUREMENT),
    (IndicatorStatus, INDICATOR_STATUS),
    (SystemStatus, SYSTEM_STATUS),
    (CrewProfile, CREW_PROFILE),
    (VoiceFeatures, VOICE_FEATURES),
    (SpacecraftProfile, SPACECRAFT_PROFILE),
]
IDS = [cls.__name__ for cls, _ in CASES]


@pytest.mark.parametrize(("cls", "payload"), CASES, ids=IDS)
def test_dict_round_trip(cls: Any, payload: dict[str, Any]) -> None:
    assert cls.from_dict(payload).to_dict() == payload


@pytest.mark.parametrize(("cls", "payload"), CASES, ids=IDS)
def test_json_round_trip(cls: Any, payload: dict[str, Any]) -> None:
    obj = cls.from_json(json.dumps(payload))
    assert cls.from_json(obj.to_json()) == obj
    assert json.loads(obj.to_json()) == payload


def test_enum_field_with_a_non_string_is_a_contract_error() -> None:
    with pytest.raises(ContractError, match="environment"):
        Measurement.from_dict({**MEASUREMENT, "environment": 5})


@pytest.mark.parametrize(("cls", "payload"), CASES, ids=IDS)
def test_unknown_field_is_rejected(cls: Any, payload: dict[str, Any]) -> None:
    with pytest.raises(ContractError, match="unknown"):
        cls.from_dict({**payload, "surprise": 1})


@pytest.mark.parametrize(("cls", "payload"), CASES, ids=IDS)
def test_missing_field_is_rejected(cls: Any, payload: dict[str, Any]) -> None:
    for key in payload:
        if cls is Measurement and key == "method":
            continue  # optional, see test_measurement_method_is_optional
        if cls is IndicatorStatus and key in {"baseline", "latest"}:
            continue  # absent while the baseline is not mature, see below
        broken = {k: v for k, v in payload.items() if k != key}
        with pytest.raises(ContractError, match=key):
            cls.from_dict(broken)


def mutated(payload: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    target = out
    *parents, leaf = path.split(".")
    for part in parents:
        target = target[int(part)] if isinstance(target, list) else target[part]
    target[leaf] = value
    return out


INVALID: list[tuple[Any, dict[str, Any], str, Any]] = [
    (Measurement, MEASUREMENT, "environment", "mars"),  # the case named in tareas.md
    (Measurement, MEASUREMENT, "indicator", "heart_vibes"),
    (Measurement, MEASUREMENT, "source", "guess"),
    (Measurement, MEASUREMENT, "method", "telepathy"),
    (Measurement, MEASUREMENT, "value", "62"),
    (Measurement, MEASUREMENT, "value", True),
    (Measurement, MEASUREMENT, "timestamp", "2026-11-14T07:30:00"),  # no timezone
    (Measurement, MEASUREMENT, "timestamp", "yesterday"),
    (Measurement, MEASUREMENT, "crewId", ""),
    (IndicatorStatus, INDICATOR_STATUS, "status", "green"),
    (IndicatorStatus, INDICATOR_STATUS, "escalation", "call_mom"),
    (IndicatorStatus, INDICATOR_STATUS, "reference", "vibes"),
    (IndicatorStatus, INDICATOR_STATUS, "environment", "mars"),
    (IndicatorStatus, INDICATOR_STATUS, "baseline.low", 70),  # low above high
    (IndicatorStatus, INDICATOR_STATUS, "baseline.nDays", -1),
    (IndicatorStatus, INDICATOR_STATUS, "reason", ""),
    (SystemStatus, SYSTEM_STATUS, "system", "liver"),
    (SystemStatus, SYSTEM_STATUS, "indicators", []),
    (SystemStatus, SYSTEM_STATUS, "indicators", ["resting_hr", "nope"]),
    (CrewProfile, CREW_PROFILE, "age", 0),
    (CrewProfile, CREW_PROFILE, "age", "38"),
    (CrewProfile, CREW_PROFILE, "sex", "robot"),
    (VoiceFeatures, VOICE_FEATURES, "features", {"emotion": "sad"}),  # numbers only
    (VoiceFeatures, VOICE_FEATURES, "features", {"jitter": True}),
    (VoiceFeatures, VOICE_FEATURES, "features", {}),
    (VoiceFeatures, VOICE_FEATURES, "experimental", False),
    (VoiceFeatures, VOICE_FEATURES, "environment", "mars"),
    (SpacecraftProfile, SPACECRAFT_PROFILE, "equipment.0.measures", ["nope"]),
    (SpacecraftProfile, SPACECRAFT_PROFILE, "equipment.0.measures", []),
    (SpacecraftProfile, SPACECRAFT_PROFILE, "id", ""),
]


@pytest.mark.parametrize(
    ("cls", "payload", "path", "value"),
    INVALID,
    ids=[f"{c.__name__}.{p}={v!r}" for c, _, p, v in INVALID],
)
def test_invalid_value_is_rejected(
    cls: Any, payload: dict[str, Any], path: str, value: Any
) -> None:
    with pytest.raises(ContractError):
        cls.from_dict(mutated(payload, path, value))


def test_error_names_the_field_and_the_allowed_values() -> None:
    with pytest.raises(ContractError, match=r"environment.*earth.*spacecraft.*planet"):
        Measurement.from_dict({**MEASUREMENT, "environment": "mars"})


def test_non_object_is_rejected() -> None:
    with pytest.raises(ContractError):
        Measurement.from_dict([1, 2])  # type: ignore[arg-type]
    with pytest.raises(ContractError):
        Measurement.from_json("not json")


def test_measurement_method_is_optional() -> None:
    no_method = {k: v for k, v in MEASUREMENT.items() if k != "method"}
    parsed = Measurement.from_dict(no_method)
    assert parsed.method is None
    assert "method" not in parsed.to_dict()


def test_timestamp_is_normalised_to_utc() -> None:
    parsed = Measurement.from_dict({**MEASUREMENT, "timestamp": "2026-11-14T09:30:00+02:00"})
    assert parsed.to_dict()["timestamp"] == "2026-11-14T07:30:00Z"


def test_indicator_status_gray_has_no_baseline() -> None:
    gray = {
        "crewId": "crew-01",
        "indicator": "mood",
        "status": "insufficient_data",
        "trend": [],
        "reason": "not enough data yet",
        "escalation": "self_care",
        "environment": "planet",
        "reference": "personal",
    }
    parsed = IndicatorStatus.from_dict(gray)
    assert parsed.baseline is None
    assert parsed.latest is None
    assert parsed.to_dict() == gray


def test_transition_reference_needs_the_previous_environment() -> None:
    transition = {**INDICATOR_STATUS, "reference": "transition"}
    with pytest.raises(ContractError, match="baselineEnvironment"):
        IndicatorStatus.from_dict(transition)
    ok = IndicatorStatus.from_dict({**transition, "baselineEnvironment": "earth"})
    assert ok.to_dict()["baselineEnvironment"] == "earth"


def test_baseline_environment_only_goes_with_transition() -> None:
    with pytest.raises(ContractError, match="baselineEnvironment"):
        IndicatorStatus.from_dict({**INDICATOR_STATUS, "baselineEnvironment": "earth"})


def test_core_contract_stays_pure() -> None:
    import crew_self_check.core.contract as module

    source = open(module.__file__, encoding="utf-8").read()  # noqa: SIM115
    for forbidden in (
        "flet",
        "fastapi",
        "sqlite3",
        "crew_self_check.astronaut",
        "crew_self_check.ground",
    ):
        assert forbidden not in source
