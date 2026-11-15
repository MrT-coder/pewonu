"""Check an incoming FHIR Bundle before the ground keeps it (G1, D-018).

The ground only accepts what the astronaut app builds: one fictitious Patient and Observations
about them. Anything else (other resources, names, birth dates) is refused with every reason.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from crew_self_check.core.fhir import LOCAL_CATEGORY, LOCAL_CREW_ID, check_bundle

_ALLOWED_TYPES = frozenset({"Patient", "Observation"})
_IDENTIFYING_FIELDS = ("name", "birthDate", "telecom", "address", "photo")


class InvalidBundle(Exception):
    def __init__(self, problems: list[str]) -> None:
        super().__init__("; ".join(problems))
        self.problems = problems


@dataclass(frozen=True, slots=True)
class BundleParts:
    bundle_id: str
    crew_id: str
    sent_at: datetime
    readings: int
    states: int


def _is_derived_status(observation: dict[str, Any]) -> bool:
    codes = [
        (c.get("system"), c.get("code"))
        for category in observation.get("category", [])
        for c in category.get("coding", [])
    ]
    return (LOCAL_CATEGORY, "derived-status") in codes


def _is_voice(observation: dict[str, Any]) -> bool:
    codes = [
        (c.get("system"), c.get("code"))
        for category in observation.get("category", [])
        for c in category.get("coding", [])
    ]
    return (LOCAL_CATEGORY, "voice-pattern") in codes


def _sent_at(bundle: dict[str, Any]) -> tuple[datetime | None, list[str]]:
    raw = bundle.get("timestamp")
    if not isinstance(raw, str):
        return None, ["timestamp: required"]
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None, [f"timestamp: {raw!r} is not an ISO 8601 date-time"]
    if parsed.tzinfo is None:
        return None, [f"timestamp: {raw!r} needs a time zone"]
    return parsed, []


def inspect_bundle(bundle: dict[str, Any]) -> BundleParts:
    """What the ground needs from ``bundle``; ``InvalidBundle`` lists every problem otherwise."""
    problems = check_bundle(bundle)
    entries = bundle.get("entry") or []
    resources = [e.get("resource") or {} for e in entries]
    for resource in resources:
        kind = resource.get("resourceType")
        if kind not in _ALLOWED_TYPES:
            problems.append(f"resourceType {kind!r} is not accepted (only Patient and Observation)")
    patients = [r for r in resources if r.get("resourceType") == "Patient"]
    crew_id = ""
    if len(patients) != 1:
        problems.append(f"expected exactly one Patient, found {len(patients)}")
    else:
        patient = patients[0]
        problems += [
            f"Patient.{field}: not accepted, the crew is fictitious and anonymous"
            for field in _IDENTIFYING_FIELDS
            if field in patient
        ]
        crew_id = next(
            (
                str(i.get("value"))
                for i in patient.get("identifier", [])
                if i.get("system") == LOCAL_CREW_ID and i.get("value")
            ),
            "",
        )
        if not crew_id:
            problems.append(f"Patient.identifier: needs a value in the system {LOCAL_CREW_ID}")
    sent_at, timestamp_problems = _sent_at(bundle)
    problems += timestamp_problems
    bundle_id = bundle.get("id")
    if not isinstance(bundle_id, str) or not bundle_id:
        problems.append("id: required")
    if problems or sent_at is None or not isinstance(bundle_id, str):
        raise InvalidBundle(problems)
    observations = [r for r in resources if r.get("resourceType") == "Observation"]
    states = sum(1 for o in observations if _is_derived_status(o))
    voices = sum(1 for o in observations if _is_voice(o))
    return BundleParts(
        bundle_id=bundle_id,
        crew_id=crew_id,
        sent_at=sent_at,
        readings=len(observations) - states - voices,
        states=states,
    )
