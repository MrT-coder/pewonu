"""Export to HL7 FHIR R4 (C8; D-006, D-010, D-018, D-021, D-022). Pure Python: no I/O, no library.

What travels to the ground base is a FHIR ``Bundle`` of ``Observation`` resources about one
fictitious crew member, and **only what the astronaut confirmed**: a ``ShareSelection`` cannot even
be created without an explicit ``confirmed=True``.

- Resting pulse, body temperature and oxygen saturation follow the HL7 R4 vital-signs profiles,
  checked on 2026-11-14 against https://hl7.org/fhir/R4/heartrate.html, ``bodytemp.html`` and
  ``oxygensat.html`` (LOINC code, UCUM unit, category ``vital-signs``).
- Every other indicator, and the derived state, use **documented local codes** (``urn:crew-self-
  check:...``) instead of invented standard ones. [HUECO] LOINC for blood pressure, glucose and
  sleep is not verified yet.
- Every resource is tagged with where the data comes from (``simulated-scenario``, ``manual``...)
  and where it was taken. The patient is fictitious and has no name or birth date.
- Ids are derived from the content (UUID v5), so sending the same selection twice is idempotent.

``check_bundle`` is our own structure check. The official HL7 validator (D-022) is the second
opinion: ``tests/test_fhir.py`` runs it when ``HL7_VALIDATOR_JAR`` points to ``validator_cli.jar``.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from crew_self_check.core.contract import (
    CrewProfile,
    Indicator,
    IndicatorStatus,
    Measurement,
    Method,
    Status,
)

LOINC = "http://loinc.org"
UCUM = "http://unitsofmeasure.org"
CATEGORY_SYSTEM = "http://terminology.hl7.org/CodeSystem/observation-category"
PROFILE_BASE = "http://hl7.org/fhir/StructureDefinition/"

LOCAL_INDICATOR = "urn:crew-self-check:indicator"
LOCAL_METHOD = "urn:crew-self-check:observation-method"
LOCAL_STATUS = "urn:crew-self-check:indicator-status"
LOCAL_REFERENCE = "urn:crew-self-check:status-reference"
LOCAL_ESCALATION = "urn:crew-self-check:escalation"
LOCAL_ENVIRONMENT = "urn:crew-self-check:environment"
LOCAL_ORIGIN = "urn:crew-self-check:data-origin"
LOCAL_CATEGORY = "urn:crew-self-check:observation-category"
LOCAL_CODE = "urn:crew-self-check:observation-code"
LOCAL_CREW_ID = "urn:crew-self-check:crew-id"

# Fixed, so the same content always gets the same ids.
_NAMESPACE = uuid.UUID("6f1d2a0e-3b1c-4b7a-9c53-2f5c0a8f7e11")

_CATEGORY_DISPLAY = {
    "vital-signs": "Vital Signs",
    "exam": "Exam",
    "laboratory": "Laboratory",
    "survey": "Survey",
    "activity": "Activity",
}
_LOCAL_CATEGORY_DISPLAY = {"derived-status": "Status derived by the app"}


@dataclass(frozen=True, slots=True)
class _Spec:
    display: str
    category: str
    ucum: str | None  # ``None`` unless the value is a quantity
    unit: str
    loinc: tuple[str, str] | None = None
    profile: str | None = None
    kind: str = "quantity"  # ``quantity``, ``integer`` (a score) or ``boolean`` (yes or no)


_SPECS: dict[Indicator, _Spec] = {
    Indicator.RESTING_HR: _Spec(
        "Resting heart rate",
        "vital-signs",
        "/min",
        "beats/minute",
        ("8867-4", "Heart rate"),
        "heartrate",
    ),
    Indicator.BODY_TEMP: _Spec(
        "Body temperature", "vital-signs", "Cel", "C", ("8310-5", "Body temperature"), "bodytemp"
    ),
    Indicator.SPO2: _Spec(
        "Oxygen saturation",
        "vital-signs",
        "%",
        "%",
        ("2708-6", "Oxygen saturation in Arterial blood"),
        "oxygensat",
    ),
    Indicator.SYSTOLIC_BP: _Spec("Systolic blood pressure", "exam", "mm[Hg]", "mmHg"),
    Indicator.DIASTOLIC_BP: _Spec("Diastolic blood pressure", "exam", "mm[Hg]", "mmHg"),
    Indicator.BLOOD_GLUCOSE: _Spec("Blood glucose", "laboratory", "mg/dL", "mg/dL"),
    Indicator.SLEEP_HOURS: _Spec("Sleep duration", "activity", "h", "hours"),
    Indicator.MOOD: _Spec(
        "Mood (self-reported, five-face scale)", "survey", None, "score", kind="integer"
    ),
    Indicator.ORTHOSTATIC_HR_DELTA: _Spec(
        "Heart-rate change on standing (standing minus lying)", "exam", "/min", "beats/minute"
    ),
    Indicator.VESTIBULAR_SYMPTOMS: _Spec(
        "Vestibular symptoms", "survey", None, "score", kind="integer"
    ),
    Indicator.TANDEM_WALK_OK: _Spec("Tandem walk completed", "exam", None, "", kind="boolean"),
}

_METHOD_DISPLAY = {
    Method.PALPATION: "Palpation (counted by hand)",
    Method.DEVICE: "Device reading",
    Method.SURVEY: "Self-reported survey",
}

_STATUS_DISPLAY = {
    Status.OK: "Green: within the range it was compared with",
    Status.WATCH: "Amber: outside the range it was compared with",
    Status.ACT: "Red: far outside the range it was compared with",
    Status.INSUFFICIENT_DATA: "Gray: not enough data to say",
}

# What the HL7 profiles fix, used by ``check_bundle``: (LOINC code, allowed UCUM codes).
_PROFILE_RULES: dict[str, tuple[str, tuple[str, ...]]] = {
    "heartrate": ("8867-4", ("/min",)),
    "bodytemp": ("8310-5", ("Cel", "[degF]")),
    "oxygensat": ("2708-6", ("%",)),
}


class ConsentRequired(Exception):
    """Something was about to be exported without the astronaut's explicit confirmation."""


@dataclass(frozen=True, slots=True)
class ShareSelection:
    """What one astronaut confirmed to share. It cannot exist without ``confirmed=True``."""

    profile: CrewProfile
    confirmed: bool  # set only from the astronaut's own confirmation in the interface
    confirmed_at: datetime
    measurements: tuple[Measurement, ...]
    statuses: tuple[IndicatorStatus, ...]

    def __post_init__(self) -> None:
        if self.confirmed is not True:
            raise ConsentRequired("nothing leaves the astronaut without their confirmation (D-006)")
        if self.confirmed_at.tzinfo is None:
            raise ValueError("confirmed_at needs a timezone")
        owners = [m.crew_id for m in self.measurements] + [s.crew_id for s in self.statuses]
        for owner in owners:
            if owner != self.profile.crew_id:
                raise ValueError(
                    f"{owner} is not {self.profile.crew_id}: "
                    "only the data of the person who confirmed can be shared"
                )
        if not self.measurements and not self.statuses:
            raise ValueError("there is nothing to share")


# --- helpers ----------------------------------------------------------------------------------


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _uuid(*parts: object) -> str:
    return str(uuid.uuid5(_NAMESPACE, "|".join(str(p) for p in parts)))


def _number(value: float) -> int | float:
    return int(value) if float(value).is_integer() else value


def _coding(system: str, code: str, display: str) -> dict[str, str]:
    return {"system": system, "code": code, "display": display}


def _concept(system: str, code: str, display: str) -> dict[str, Any]:
    return {"coding": [_coding(system, code, display)]}


def _category(code: str) -> list[dict[str, Any]]:
    if code in _CATEGORY_DISPLAY:
        return [_concept(CATEGORY_SYSTEM, code, _CATEGORY_DISPLAY[code])]
    return [_concept(LOCAL_CATEGORY, code, _LOCAL_CATEGORY_DISPLAY[code])]


def patient_id(crew_id: str) -> str:
    return _uuid("patient", crew_id)


def patient_ref(crew_id: str) -> str:
    return f"urn:uuid:{patient_id(crew_id)}"


def indicator_from_coding(system: str, code: str) -> Indicator | None:
    """The indicator an Observation code stands for, by LOINC or by the local indicator code."""
    for indicator, spec in _SPECS.items():
        if system == LOINC and spec.loinc is not None and spec.loinc[0] == code:
            return indicator
        if system == LOCAL_INDICATOR and indicator.value == code:
            return indicator
    return None


# --- resources --------------------------------------------------------------------------------


def patient_resource(profile: CrewProfile) -> dict[str, Any]:
    """A fictitious crew member: an id and a gender, never a name or a birth date."""
    return {
        "resourceType": "Patient",
        "id": patient_id(profile.crew_id),
        "meta": {"tag": [_coding(LOCAL_ORIGIN, "fictitious-crew", "Fictitious crew member")]},
        "identifier": [{"system": LOCAL_CREW_ID, "value": profile.crew_id}],
        "active": True,
        "gender": profile.sex.value,
    }


def observation_resource(measurement: Measurement, subject: str) -> dict[str, Any]:
    spec = _SPECS[measurement.indicator]
    coding = (
        _coding(LOINC, *spec.loinc)
        if spec.loinc
        else _coding(LOCAL_INDICATOR, measurement.indicator.value, spec.display)
    )
    meta: dict[str, Any] = {
        "tag": [
            _coding(LOCAL_ORIGIN, measurement.source.value, "Where the data comes from"),
            _coding(LOCAL_ENVIRONMENT, measurement.environment.value, "Where it was taken"),
        ]
    }
    if spec.profile:
        meta["profile"] = [PROFILE_BASE + spec.profile]
    resource: dict[str, Any] = {
        "resourceType": "Observation",
        "id": _uuid(
            "obs",
            measurement.crew_id,
            measurement.indicator,
            measurement.environment,
            _iso(measurement.timestamp),
            measurement.value,
            measurement.method,
            measurement.source,
        ),
        "meta": meta,
        "status": "final",
        "category": _category(spec.category),
        "code": {"coding": [coding], "text": spec.display},
        "subject": {"reference": subject},
        "effectiveDateTime": _iso(measurement.timestamp),
    }
    if spec.kind == "boolean":
        if measurement.value not in (0, 1):
            raise ValueError(f"{measurement.indicator.value} must be 0 or 1")
        resource["valueBoolean"] = measurement.value == 1
    elif spec.kind == "integer":
        # A score is a whole number: no unit, so no made-up UCUM annotation like {score}.
        if not float(measurement.value).is_integer():
            raise ValueError(f"{measurement.indicator.value} must be a whole number")
        resource["valueInteger"] = int(measurement.value)
    else:
        resource["valueQuantity"] = {
            "value": _number(measurement.value),
            "unit": spec.unit,
            "system": UCUM,
            "code": spec.ucum,
        }
    if measurement.method is not None:
        resource["method"] = _concept(
            LOCAL_METHOD, measurement.method.value, _METHOD_DISPLAY[measurement.method]
        )
    return resource


def status_resource(status: IndicatorStatus, subject: str, effective: datetime) -> dict[str, Any]:
    """The derived state of one indicator, with its reason and what it was compared against."""

    def part(code: str, system: str, value: str, display: str) -> dict[str, Any]:
        return {
            "code": _concept(LOCAL_CODE, code, code),
            "valueCodeableConcept": _concept(system, value, display),
        }

    components = [
        part(
            "indicator", LOCAL_INDICATOR, status.indicator.value, _SPECS[status.indicator].display
        ),
        part("reference", LOCAL_REFERENCE, status.reference.value, status.reference.value),
        part(
            "escalation-suggestion",
            LOCAL_ESCALATION,
            status.escalation.value,
            status.escalation.value,
        ),
    ]
    if status.baseline_environment is not None:
        components.append(
            part(
                "baseline-environment",
                LOCAL_ENVIRONMENT,
                status.baseline_environment.value,
                status.baseline_environment.value,
            )
        )
    return {
        "resourceType": "Observation",
        "id": _uuid(
            "status",
            status.crew_id,
            status.indicator,
            status.environment,
            status.status,
            status.reference,
            status.baseline_environment,
            _iso(effective),
            status.reason,
        ),
        "meta": {
            "tag": [
                _coding(LOCAL_ORIGIN, "derived-by-app", "Derived by the app, not measured"),
                _coding(LOCAL_ENVIRONMENT, status.environment.value, "Where it applies"),
            ]
        },
        "status": "final",
        "category": _category("derived-status"),
        "code": {"coding": [_coding(LOCAL_CODE, "indicator-status", "Indicator status")]},
        "subject": {"reference": subject},
        "effectiveDateTime": _iso(effective),
        "valueCodeableConcept": _concept(
            LOCAL_STATUS, status.status.value, _STATUS_DISPLAY[status.status]
        ),
        "note": [{"text": status.reason}],
        "component": components,
    }


def build_bundle(selection: ShareSelection) -> dict[str, Any]:
    """A ``collection`` Bundle with the patient and exactly what was selected."""
    subject = patient_ref(selection.profile.crew_id)
    resources: list[dict[str, Any]] = [patient_resource(selection.profile)]
    resources += [observation_resource(m, subject) for m in selection.measurements]
    resources += [status_resource(s, subject, selection.confirmed_at) for s in selection.statuses]
    return {
        "resourceType": "Bundle",
        "id": _uuid("bundle", selection.profile.crew_id, *(r["id"] for r in resources)),
        "type": "collection",
        "timestamp": _iso(selection.confirmed_at),
        "entry": [{"fullUrl": f"urn:uuid:{r['id']}", "resource": r} for r in resources],
    }


def bundle_json(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2, ensure_ascii=False) + "\n"


# --- our own structure check ------------------------------------------------------------------


def check_bundle(bundle: dict[str, Any]) -> list[str]:
    """Problems found in the structure of ``bundle`` (empty if none). Not a full FHIR validation."""
    problems: list[str] = []
    if bundle.get("resourceType") != "Bundle":
        problems.append("resourceType: expected Bundle")
    if bundle.get("type") != "collection":
        problems.append(f"type: expected collection, got {bundle.get('type')!r}")
    entries = bundle.get("entry") or []
    if not entries:
        problems.append("entry: the bundle is empty")
    urls: list[str] = [str(e.get("fullUrl")) for e in entries]
    for url in sorted({u for u in urls if urls.count(u) > 1}):
        problems.append(f"duplicate fullUrl: {url}")
    known = set(urls)
    for index, entry in enumerate(entries):
        resource = entry.get("resource") or {}
        if resource.get("resourceType") == "Observation":
            problems += _check_observation(f"entry[{index}]", resource, known)
    return problems


def _check_observation(where: str, obs: dict[str, Any], known: set[str]) -> list[str]:
    problems = [
        f"{where}: missing {key}"
        for key in ("status", "code", "subject", "effectiveDateTime")
        if key not in obs
    ]
    if not any(
        key in obs
        for key in ("valueQuantity", "valueBoolean", "valueInteger", "valueCodeableConcept")
    ):
        problems.append(f"{where}: missing value[x]")
    reference = (obs.get("subject") or {}).get("reference")
    if reference is not None and reference not in known:
        problems.append(f"{where}: reference {reference} does not resolve inside the bundle")
    for profile in (obs.get("meta") or {}).get("profile", []):
        name = str(profile).removeprefix(PROFILE_BASE)
        if name in _PROFILE_RULES:
            problems += _check_profile(where, name, obs)
    return problems


def _check_profile(where: str, name: str, obs: dict[str, Any]) -> list[str]:
    loinc, units = _PROFILE_RULES[name]
    problems: list[str] = []
    codings = (obs.get("code") or {}).get("coding", [])
    if not any(c.get("system") == LOINC and c.get("code") == loinc for c in codings):
        problems.append(f"{where}: {name} needs the LOINC code {loinc}")
    quantity = obs.get("valueQuantity") or {}
    if quantity.get("system") != UCUM:
        problems.append(f"{where}: {name} needs the UCUM system {UCUM}")
    if quantity.get("code") not in units:
        problems.append(f"{where}: {name} needs the UCUM code {' or '.join(units)}")
    category = [c.get("code") for cat in obs.get("category", []) for c in cat.get("coding", [])]
    if "vital-signs" not in category:
        problems.append(f"{where}: {name} needs the category vital-signs")
    return problems
