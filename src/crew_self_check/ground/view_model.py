"""What the ground shows about one crew member, read back out of the bundles they sent (G3).

Pure functions over received bundles. Nothing here reaches for data the astronaut did not send.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from crew_self_check.core.fhir import (
    LOCAL_CATEGORY,
    LOCAL_ENVIRONMENT,
    LOCAL_ORIGIN,
    indicator_from_coding,
)
from crew_self_check.core.inbox import ReceivedBundle


@dataclass(frozen=True, slots=True)
class StateRow:
    indicator: str  # the contract code, for example ``resting_hr``
    environment: str
    status: str  # ok, watch, act or insufficient_data
    reason: str
    reference: str
    escalation: str
    effective: str


@dataclass(frozen=True, slots=True)
class ReadingRow:
    key: str  # the contract code, or the LOINC code when the indicator has one
    indicator: str  # the contract code when the coding is one the app knows, else empty
    label: str
    value: str
    unit: str
    environment: str
    origin: str
    method: str
    effective: str


@dataclass(frozen=True, slots=True)
class CrewView:
    crew_id: str
    bundles: int
    last_arrival: datetime
    states: tuple[StateRow, ...]
    readings: tuple[ReadingRow, ...]


def _tag(resource: dict[str, Any], system: str) -> str:
    for tag in (resource.get("meta") or {}).get("tag", []):
        if tag.get("system") == system:
            return str(tag.get("code", ""))
    return ""


def _is_status(resource: dict[str, Any]) -> bool:
    return any(
        c.get("system") == LOCAL_CATEGORY and c.get("code") == "derived-status"
        for category in resource.get("category", [])
        for c in category.get("coding", [])
    )


def _component(resource: dict[str, Any], code: str) -> str:
    for part in resource.get("component", []):
        codings = (part.get("code") or {}).get("coding", [])
        if any(c.get("code") == code for c in codings):
            values = (part.get("valueCodeableConcept") or {}).get("coding", [])
            return str(values[0].get("code", "")) if values else ""
    return ""


def _state(resource: dict[str, Any]) -> StateRow:
    value = (resource.get("valueCodeableConcept") or {}).get("coding", [{}])[0]
    notes = resource.get("note") or [{}]
    return StateRow(
        indicator=_component(resource, "indicator"),
        environment=_tag(resource, LOCAL_ENVIRONMENT),
        status=str(value.get("code", "")),
        reason=str(notes[0].get("text", "")),
        reference=_component(resource, "reference"),
        escalation=_component(resource, "escalation-suggestion"),
        effective=str(resource.get("effectiveDateTime", "")),
    )


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def _reading(resource: dict[str, Any]) -> ReadingRow:
    coding = (resource.get("code") or {}).get("coding", [{}])[0]
    if "valueQuantity" in resource:
        quantity = resource["valueQuantity"]
        value, unit = _number(quantity.get("value", 0)), str(quantity.get("unit", ""))
    elif "valueBoolean" in resource:
        value, unit = ("yes" if resource["valueBoolean"] else "no"), ""
    else:
        value, unit = str(resource.get("valueInteger", "")), ""
    method = (resource.get("method") or {}).get("coding", [{}])[0].get("code", "")
    known = indicator_from_coding(str(coding.get("system", "")), str(coding.get("code", "")))
    return ReadingRow(
        key=str(coding.get("code", "")),
        indicator=known.value if known else "",
        label=str((resource.get("code") or {}).get("text", coding.get("display", ""))),
        value=value,
        unit=unit,
        environment=_tag(resource, LOCAL_ENVIRONMENT),
        origin=_tag(resource, LOCAL_ORIGIN),
        method=str(method),
        effective=str(resource.get("effectiveDateTime", "")),
    )


def build_crew_view(crew_id: str, received: Iterable[ReceivedBundle]) -> CrewView | None:
    """The newest state and reading of each indicator among what arrived; ``None`` if nothing."""
    mine = sorted((r for r in received if r.crew_id == crew_id), key=lambda r: r.available_at)
    if not mine:
        return None
    states: dict[tuple[str, str], StateRow] = {}
    readings: dict[tuple[str, str], ReadingRow] = {}
    for item in mine:  # oldest arrival first, so the newest overwrites
        for entry in item.bundle.get("entry", []):
            resource = entry.get("resource") or {}
            if resource.get("resourceType") != "Observation":
                continue
            if _is_status(resource):
                row = _state(resource)
                states[(row.indicator, row.environment)] = row
            else:
                reading = _reading(resource)
                readings[(reading.key, reading.environment)] = reading
    return CrewView(
        crew_id=crew_id,
        bundles=len(mine),
        last_arrival=mine[-1].available_at,
        states=tuple(states.values()),
        readings=tuple(readings.values()),
    )


def crew_ids(received: Iterable[ReceivedBundle]) -> tuple[str, ...]:
    return tuple(sorted({r.crew_id for r in received}))
