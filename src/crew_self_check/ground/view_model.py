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
from crew_self_check.core.status import SYSTEM_INDICATORS


@dataclass(frozen=True, slots=True)
class StateRow:
    indicator: str  # the contract code, for example ``resting_hr``
    environment: str
    status: str  # ok, watch, act or insufficient_data
    reason: str
    reference: str
    escalation: str
    effective: str
    low: float | None = None  # the person's usual band, when the app had one
    high: float | None = None
    center: float | None = None
    unit: str = ""
    trend: tuple[tuple[str, float], ...] = ()  # (time, value) of the recent readings


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
class VoiceRow:
    """One voice note: only how it compares with the person's own usual, never what was said."""

    effective: str
    environment: str
    level: str  # usual, different or building
    changed: tuple[tuple[str, str], ...]  # (measure, direction) of what moved
    reference: str  # personal or transition
    baseline_environment: str  # the previous place when the reference is a transition


@dataclass(frozen=True, slots=True)
class CrewView:
    crew_id: str
    bundles: int
    last_arrival: datetime
    states: tuple[StateRow, ...]
    readings: tuple[ReadingRow, ...]
    voice: tuple[VoiceRow, ...] = ()


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


def _quantity(part: dict[str, Any]) -> tuple[float | None, str]:
    quantity = part.get("valueQuantity") or {}
    value = quantity.get("value")
    return (float(value) if value is not None else None), str(quantity.get("unit", ""))


def _state(resource: dict[str, Any]) -> StateRow:
    bands: dict[str, float] = {}
    trend: list[tuple[str, float]] = []
    unit = ""
    for part in resource.get("component", []):
        name = str(((part.get("code") or {}).get("coding") or [{}])[0].get("code", ""))
        value, part_unit = _quantity(part)
        if value is None:
            continue
        unit = part_unit or unit
        if name in ("baseline-low", "baseline-high", "baseline-center"):
            bands[name] = value
        elif name == "trend-point":
            when = next((e.get("valueDateTime", "") for e in part.get("extension", [])), "")
            trend.append((str(when), value))
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
        low=bands.get("baseline-low"),
        high=bands.get("baseline-high"),
        center=bands.get("baseline-center"),
        unit=unit,
        trend=tuple(trend),
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


def _is_voice(resource: dict[str, Any]) -> bool:
    return any(
        c.get("system") == LOCAL_CATEGORY and c.get("code") == "voice-pattern"
        for category in resource.get("category", [])
        for c in category.get("coding", [])
    )


def _voice(resource: dict[str, Any]) -> VoiceRow:
    level = ((resource.get("valueCodeableConcept") or {}).get("coding") or [{}])[0]
    changed: list[tuple[str, str]] = []
    reference, previous = "personal", ""
    for part in resource.get("component", []):
        name = str(((part.get("code") or {}).get("coding") or [{}])[0].get("code", ""))
        concept = ((part.get("valueCodeableConcept") or {}).get("coding") or [{}])[0]
        if name.endswith("-direction"):
            changed.append((name.removesuffix("-direction"), str(concept.get("code", ""))))
        elif name == "reference":
            reference = str(concept.get("code", "personal"))
        elif name == "baseline-environment":
            previous = str(concept.get("code", ""))
    return VoiceRow(
        effective=str(resource.get("effectiveDateTime", "")),
        environment=_tag(resource, LOCAL_ENVIRONMENT),
        level=str(level.get("code", "building")),
        changed=tuple(changed),
        reference=reference,
        baseline_environment=previous,
    )


def build_crew_view(crew_id: str, received: Iterable[ReceivedBundle]) -> CrewView | None:
    """The newest state and reading of each indicator among what arrived; ``None`` if nothing."""
    mine = sorted((r for r in received if r.crew_id == crew_id), key=lambda r: r.available_at)
    if not mine:
        return None
    states: dict[tuple[str, str], StateRow] = {}
    readings: dict[tuple[str, str], ReadingRow] = {}
    voice: list[VoiceRow] = []
    for item in mine:  # oldest arrival first, so the newest overwrites
        for entry in item.bundle.get("entry", []):
            resource = entry.get("resource") or {}
            if resource.get("resourceType") != "Observation":
                continue
            if _is_voice(resource):
                voice.append(_voice(resource))
            elif _is_status(resource):
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
        voice=tuple(sorted(voice, key=lambda v: v.effective)),
    )


def crew_ids(received: Iterable[ReceivedBundle]) -> tuple[str, ...]:
    return tuple(sorted({r.crew_id for r in received}))


_SEVERITY = {"ok": 0, "insufficient_data": 1, "watch": 2, "act": 3}
_ESCALATION_RANK = {"self_care": 0, "crew_cmo": 1, "ground_surgeon": 2}


def system_levels(view: CrewView) -> dict[str, str]:
    """The worst state of each body system among what was sent (a system with no data is absent)."""
    by_indicator: dict[str, str] = {}
    for row in view.states:
        old = by_indicator.get(row.indicator)
        if old is None or _SEVERITY.get(row.status, 1) >= _SEVERITY.get(old, 1):
            by_indicator[row.indicator] = row.status
    levels: dict[str, str] = {}
    for system, indicators in SYSTEM_INDICATORS.items():
        found = [by_indicator[i.value] for i in indicators if i.value in by_indicator]
        if found:
            levels[system.value] = max(found, key=lambda status: _SEVERITY.get(status, 1))
    return levels


def attention_rows(view: CrewView) -> tuple[StateRow, ...]:
    """What the astronaut's own app flagged amber or red, red first."""
    flagged = [s for s in view.states if s.status in ("watch", "act")]
    return tuple(sorted(flagged, key=lambda s: -_SEVERITY[s.status]))


def worst_status(view: CrewView) -> str:
    return max((s.status for s in view.states), key=lambda s: _SEVERITY.get(s, 1), default="ok")


def top_escalation(view: CrewView) -> str:
    """The strongest suggestion the astronaut's app made for what it flagged."""
    return max(
        (s.escalation for s in attention_rows(view)),
        key=lambda e: _ESCALATION_RANK.get(e, 0),
        default="self_care",
    )


def attention_order(view: CrewView) -> tuple[int, str]:
    """Sort key: the crew member with the most severe flag first, then by id."""
    return (-_SEVERITY.get(worst_status(view), 0), view.crew_id)
