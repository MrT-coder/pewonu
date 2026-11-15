"""Data contract 0.3 (docs/contrato-datos.md): typed objects with JSON round trip and validation.

Pure Python: no I/O, no framework. Every ``from_dict`` is strict: unknown fields, missing fields
and values outside the contract raise ``ContractError`` naming the field.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Self


class ContractError(ValueError):
    """The payload does not follow the data contract."""


class Environment(StrEnum):
    EARTH = "earth"
    SPACECRAFT = "spacecraft"
    PLANET = "planet"


class Method(StrEnum):
    PALPATION = "palpation"
    DEVICE = "device"
    SURVEY = "survey"


class Indicator(StrEnum):
    RESTING_HR = "resting_hr"
    SYSTOLIC_BP = "systolic_bp"
    DIASTOLIC_BP = "diastolic_bp"
    BLOOD_GLUCOSE = "blood_glucose"
    BODY_TEMP = "body_temp"
    SLEEP_HOURS = "sleep_hours"
    MOOD = "mood"
    SPO2 = "spo2"
    ORTHOSTATIC_HR_DELTA = "orthostatic_hr_delta"
    VESTIBULAR_SYMPTOMS = "vestibular_symptoms"
    TANDEM_WALK_OK = "tandem_walk_ok"


class Source(StrEnum):
    MANUAL = "manual"
    SLEEP_ACCEL = "sleep-accel"
    OFFICIAL_2026 = "official-2026"
    SIMULATED_SCENARIO = "simulated-scenario"


class Status(StrEnum):
    OK = "ok"
    WATCH = "watch"
    ACT = "act"
    INSUFFICIENT_DATA = "insufficient_data"


class Escalation(StrEnum):
    SELF_CARE = "self_care"
    CREW_CMO = "crew_cmo"
    GROUND_SURGEON = "ground_surgeon"


class Reference(StrEnum):
    PERSONAL = "personal"
    TRANSITION = "transition"
    POPULATION = "population"


class System(StrEnum):
    CARDIOVASCULAR = "cardiovascular"
    VESTIBULAR = "vestibular"
    SLEEP_BRAIN = "sleep_brain"
    MOOD = "mood"
    BONE_MUSCLE = "bone_muscle"
    IMMUNE = "immune"


class Sex(StrEnum):
    # [SUPOSICION] the contract only shows "female"; the NHSR nº 41 table (D-014) is by male/female.
    FEMALE = "female"
    MALE = "male"


# --- validation helpers -------------------------------------------------------------------------


def _fail(where: str, message: str) -> ContractError:
    return ContractError(f"{where}: {message}")


def _object(
    data: object, where: str, required: set[str], optional: frozenset[str] = frozenset()
) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise _fail(where, f"expected an object, got {type(data).__name__}")
    unknown = sorted(set(data) - required - optional)
    if unknown:
        raise _fail(where, f"unknown field(s): {', '.join(unknown)}")
    for key in sorted(required):
        if key not in data:
            raise _fail(where, f"missing field '{key}'")
    return data


def _text(value: object, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _fail(where, "expected a non-empty string")
    return value


def _enum[E: StrEnum](cls: type[E], value: object, where: str) -> E:
    if isinstance(value, str):
        try:
            return cls(value)
        except ValueError:
            pass
    allowed = ", ".join(member.value for member in cls)
    raise _fail(where, f"{value!r} is not one of {allowed}")


def _number(value: object, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value):
        raise _fail(where, "expected a finite number")
    return float(value)


def _int(value: object, where: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise _fail(where, f"expected an integer >= {minimum}")
    return value


def _timestamp(value: object, where: str) -> datetime:
    text = _text(value, where)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        raise _fail(where, f"{text!r} is not an ISO 8601 timestamp") from None
    if parsed.tzinfo is None:
        raise _fail(where, f"{text!r} has no timezone (use UTC, e.g. 2026-11-14T07:30:00Z)")
    return parsed.astimezone(UTC)


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _list(value: object, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise _fail(where, "expected a list")
    return value


class _Contract:
    """JSON (de)serialisation shared by every contract object."""

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        raise NotImplementedError

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"))

    @classmethod
    def from_json(cls, text: str) -> Self:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            raise ContractError(f"invalid JSON: {error}") from None
        return cls.from_dict(data)


# --- 1. Measurement -----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Measurement(_Contract):
    crew_id: str
    indicator: Indicator
    value: float
    unit: str
    timestamp: datetime
    source: Source
    environment: Environment
    method: Method | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "crewId": self.crew_id,
            "indicator": self.indicator.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": _iso(self.timestamp),
            "source": self.source.value,
            "environment": self.environment.value,
        }
        if self.method is not None:
            out["method"] = self.method.value
        return out

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        required = {"crewId", "indicator", "value", "unit", "timestamp", "source", "environment"}
        d = _object(data, "Measurement", required, frozenset({"method"}))
        method = d.get("method")
        return cls(
            crew_id=_text(d["crewId"], "crewId"),
            indicator=_enum(Indicator, d["indicator"], "indicator"),
            value=_number(d["value"], "value"),
            unit=_text(d["unit"], "unit"),
            timestamp=_timestamp(d["timestamp"], "timestamp"),
            source=_enum(Source, d["source"], "source"),
            environment=_enum(Environment, d["environment"], "environment"),
            method=None if method is None else _enum(Method, method, "method"),
        )


# --- 2. IndicatorStatus -------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Baseline:
    center: float
    low: float
    high: float
    n_days: int

    def to_dict(self) -> dict[str, Any]:
        return {"center": self.center, "low": self.low, "high": self.high, "nDays": self.n_days}

    @classmethod
    def from_dict(cls, data: object) -> Self:
        d = _object(data, "baseline", {"center", "low", "high", "nDays"})
        low = _number(d["low"], "baseline.low")
        center = _number(d["center"], "baseline.center")
        high = _number(d["high"], "baseline.high")
        if not low <= center <= high:
            raise _fail("baseline", "expected low <= center <= high")
        return cls(center, low, high, _int(d["nDays"], "baseline.nDays", 0))


@dataclass(frozen=True, slots=True)
class TrendPoint:
    timestamp: datetime
    value: float

    def to_dict(self) -> dict[str, Any]:
        return {"timestamp": _iso(self.timestamp), "value": self.value}

    @classmethod
    def from_dict(cls, data: object) -> Self:
        d = _object(data, "trend point", {"timestamp", "value"})
        return cls(
            _timestamp(d["timestamp"], "trend.timestamp"), _number(d["value"], "trend.value")
        )


@dataclass(frozen=True, slots=True)
class IndicatorStatus(_Contract):
    crew_id: str
    indicator: Indicator
    status: Status
    reason: str
    escalation: Escalation
    environment: Environment
    reference: Reference
    trend: tuple[TrendPoint, ...] = ()
    baseline: Baseline | None = None
    latest: float | None = None
    baseline_environment: Environment | None = None

    def __post_init__(self) -> None:
        if self.reference is Reference.TRANSITION and self.baseline_environment is None:
            raise _fail("baselineEnvironment", "required when reference is 'transition'")
        if self.reference is not Reference.TRANSITION and self.baseline_environment is not None:
            raise _fail("baselineEnvironment", "only allowed when reference is 'transition'")

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "crewId": self.crew_id,
            "indicator": self.indicator.value,
            "status": self.status.value,
            "trend": [point.to_dict() for point in self.trend],
            "reason": self.reason,
            "escalation": self.escalation.value,
            "environment": self.environment.value,
            "reference": self.reference.value,
        }
        if self.baseline is not None:
            out["baseline"] = self.baseline.to_dict()
        if self.latest is not None:
            out["latest"] = self.latest
        if self.baseline_environment is not None:
            out["baselineEnvironment"] = self.baseline_environment.value
        return out

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        required = {
            "crewId", "indicator", "status", "trend", "reason", "escalation", "environment",
            "reference",
        }  # fmt: skip
        optional = frozenset({"baseline", "latest", "baselineEnvironment"})
        d = _object(data, "IndicatorStatus", required, optional)
        baseline, latest = d.get("baseline"), d.get("latest")
        previous = d.get("baselineEnvironment")
        return cls(
            crew_id=_text(d["crewId"], "crewId"),
            indicator=_enum(Indicator, d["indicator"], "indicator"),
            status=_enum(Status, d["status"], "status"),
            reason=_text(d["reason"], "reason"),
            escalation=_enum(Escalation, d["escalation"], "escalation"),
            environment=_enum(Environment, d["environment"], "environment"),
            reference=_enum(Reference, d["reference"], "reference"),
            trend=tuple(TrendPoint.from_dict(p) for p in _list(d["trend"], "trend")),
            baseline=None if baseline is None else Baseline.from_dict(baseline),
            latest=None if latest is None else _number(latest, "latest"),
            baseline_environment=(
                None if previous is None else _enum(Environment, previous, "baselineEnvironment")
            ),
        )


# --- 3. SystemStatus ----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SystemStatus(_Contract):
    crew_id: str
    system: System
    status: Status
    indicators: tuple[Indicator, ...]

    def __post_init__(self) -> None:
        if not self.indicators:
            raise _fail("indicators", "expected at least one indicator")

    def to_dict(self) -> dict[str, Any]:
        return {
            "crewId": self.crew_id,
            "system": self.system.value,
            "status": self.status.value,
            "indicators": [indicator.value for indicator in self.indicators],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        d = _object(data, "SystemStatus", {"crewId", "system", "status", "indicators"})
        return cls(
            crew_id=_text(d["crewId"], "crewId"),
            system=_enum(System, d["system"], "system"),
            status=_enum(Status, d["status"], "status"),
            indicators=tuple(
                _enum(Indicator, item, "indicators")
                for item in _list(d["indicators"], "indicators")
            ),
        )


# --- 4. CrewProfile -----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CrewProfile(_Contract):
    """Who the person is. The body data is preflight and simulated (D-030)."""

    crew_id: str
    age: int
    sex: Sex
    baseline_source: str
    weight_kg: float | None = None
    height_cm: float | None = None
    bone_mineral_density: float | None = None  # preflight lumbar-spine DXA, g/cm2

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "crewId": self.crew_id,
            "age": self.age,
            "sex": self.sex.value,
            "baselineSource": self.baseline_source,
        }
        for key, value in (
            ("weightKg", self.weight_kg),
            ("heightCm", self.height_cm),
            ("boneMineralDensity", self.bone_mineral_density),
        ):
            if value is not None:
                out[key] = value
        return out

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        d = _object(
            data,
            "CrewProfile",
            {"crewId", "age", "sex", "baselineSource"},
            frozenset({"weightKg", "heightCm", "boneMineralDensity"}),
        )

        def positive(key: str) -> float | None:
            if key not in d:
                return None
            value = _number(d[key], key)
            if value <= 0:
                raise _fail(key, "expected a number greater than 0")
            return value

        return cls(
            crew_id=_text(d["crewId"], "crewId"),
            age=_int(d["age"], "age", 1),
            sex=_enum(Sex, d["sex"], "sex"),
            baseline_source=_text(d["baselineSource"], "baselineSource"),
            weight_kg=positive("weightKg"),
            height_cm=positive("heightCm"),
            bone_mineral_density=positive("boneMineralDensity"),
        )


# --- 5. VoiceFeatures ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class VoiceFeatures(_Contract):
    """Acoustic numbers only: no emotion labels, no audio, no transcript (D-015, D-019)."""

    crew_id: str
    timestamp: datetime
    environment: Environment
    features: Mapping[str, float]
    mood_survey_score: int

    def __post_init__(self) -> None:
        if not self.features:
            raise _fail("features", "expected at least one measure")

    def to_dict(self) -> dict[str, Any]:
        return {
            "crewId": self.crew_id,
            "timestamp": _iso(self.timestamp),
            "environment": self.environment.value,
            "features": dict(self.features),
            "moodSurveyScore": self.mood_survey_score,
            "experimental": True,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        required = {
            "crewId", "timestamp", "environment", "features", "moodSurveyScore", "experimental",
        }  # fmt: skip
        d = _object(data, "VoiceFeatures", required)
        if d["experimental"] is not True:
            raise _fail("experimental", "must be true: acoustic measures are experimental")
        raw = d["features"]
        if not isinstance(raw, Mapping):
            raise _fail("features", "expected an object of numbers")
        return cls(
            crew_id=_text(d["crewId"], "crewId"),
            timestamp=_timestamp(d["timestamp"], "timestamp"),
            environment=_enum(Environment, d["environment"], "environment"),
            features={_text(k, "features"): _number(v, f"features.{k}") for k, v in raw.items()},
            mood_survey_score=_int(d["moodSurveyScore"], "moodSurveyScore", 0),
        )


# --- 6. SpacecraftProfile -----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Equipment:
    id: str
    measures: tuple[Indicator, ...]
    mode: str  # [HUECO] the closed set of modes is defined with the verified ISS equipment (C7)

    def __post_init__(self) -> None:
        if not self.measures:
            raise _fail("equipment.measures", "expected at least one indicator")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "measures": [m.value for m in self.measures], "mode": self.mode}

    @classmethod
    def from_dict(cls, data: object) -> Self:
        d = _object(data, "equipment", {"id", "measures", "mode"})
        return cls(
            id=_text(d["id"], "equipment.id"),
            measures=tuple(
                _enum(Indicator, m, "equipment.measures") for m in _list(d["measures"], "measures")
            ),
            mode=_text(d["mode"], "equipment.mode"),
        )


@dataclass(frozen=True, slots=True)
class SpacecraftProfile(_Contract):
    id: str
    label: str
    equipment: tuple[Equipment, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "equipment": [item.to_dict() for item in self.equipment],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        d = _object(data, "SpacecraftProfile", {"id", "label", "equipment"})
        return cls(
            id=_text(d["id"], "id"),
            label=_text(d["label"], "label"),
            equipment=tuple(Equipment.from_dict(e) for e in _list(d["equipment"], "equipment")),
        )
