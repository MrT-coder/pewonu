"""The data intake view model (A17): what came in, from which source, and when. Pure logic.

In real use the readings would arrive by themselves from the crew's devices (D-011); the demo
replays a simulated scenario instead. This model only *describes* what the person has received so
far, by source and by day, so the screen can show that the data is in the system and where it
comes from. It computes no state and no threshold: the colors come from the engine (``state``).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Indicator, Measurement, Method, Source

FEED_DAYS = 7


class SourceKind(StrEnum):
    WEARABLE = "wearable"  # delivered by a device (the simulated watch and band)
    SURVEY = "survey"  # short questions answered in the app or imported with the scenario
    HAND_PULSE = "hand_pulse"  # the resting pulse counted by hand
    ENTERED = "entered"  # entered by the astronaut in this app


_ORDER = tuple(SourceKind)


@dataclass(frozen=True, slots=True)
class SourceRow:
    kind: SourceKind
    indicators: tuple[Indicator, ...]
    readings: int
    last: datetime


@dataclass(frozen=True, slots=True)
class FeedDay:
    label: str  # E-n, T+n or R+n
    total: int
    counts: dict[SourceKind, int]


@dataclass(frozen=True, slots=True)
class Intake:
    total_readings: int
    indicators_covered: int
    indicators_total: int
    sources: tuple[SourceRow, ...]
    feed: tuple[FeedDay, ...]  # newest day first
    origins: frozenset[Source]

    @property
    def simulated(self) -> bool:
        return Source.SIMULATED_SCENARIO in self.origins


def _kind(measurement: Measurement) -> SourceKind:
    if measurement.source is Source.MANUAL:
        return SourceKind.ENTERED
    if measurement.method is Method.DEVICE:
        return SourceKind.WEARABLE
    if measurement.method is Method.SURVEY:
        return SourceKind.SURVEY
    return SourceKind.HAND_PULSE


def build_intake(state: AppState) -> Intake:
    received = state.visible_measurements()
    if not received:
        return Intake(0, 0, len(Indicator), (), (), frozenset())

    by_kind: dict[SourceKind, list[Measurement]] = {}
    for measurement in received:
        by_kind.setdefault(_kind(measurement), []).append(measurement)
    sources = tuple(
        SourceRow(
            kind=kind,
            indicators=tuple(i for i in Indicator if any(m.indicator is i for m in by_kind[kind])),
            readings=len(by_kind[kind]),
            last=max(m.timestamp for m in by_kind[kind]),
        )
        for kind in _ORDER
        if kind in by_kind
    )

    label_of_date = {d.timestamp.date(): d.label for d in state.scenario.days}
    index_of_date = {d.timestamp.date(): d.index for d in state.scenario.days}
    per_day: dict[object, dict[SourceKind, int]] = {}
    for measurement in received:
        counts = per_day.setdefault(measurement.timestamp.date(), {})
        kind = _kind(measurement)
        counts[kind] = counts.get(kind, 0) + 1
    newest_first = sorted(per_day, key=lambda date: index_of_date[date], reverse=True)  # type: ignore[index]
    feed = tuple(
        FeedDay(label_of_date[date], sum(per_day[date].values()), per_day[date])  # type: ignore[index]
        for date in newest_first[:FEED_DAYS]
    )

    return Intake(
        total_readings=len(received),
        indicators_covered=len({m.indicator for m in received}),
        indicators_total=len(Indicator),
        sources=sources,
        feed=feed,
        origins=frozenset(m.source for m in received),
    )
