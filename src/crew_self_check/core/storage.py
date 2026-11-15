"""Storage port for what the astronaut records (D-017). Pure Python; adapters live elsewhere."""

from __future__ import annotations

from typing import Protocol

from crew_self_check.core.contract import Measurement


class MeasurementStore(Protocol):
    """Where recorded measurements are kept. Order of insertion is preserved."""

    def add(self, measurement: Measurement) -> None: ...

    def all(self) -> tuple[Measurement, ...]: ...

    def for_crew(self, crew_id: str) -> tuple[Measurement, ...]: ...


class InMemoryMeasurementStore:
    """Default adapter: nothing survives a restart. Also the test double."""

    def __init__(self) -> None:
        self._items: list[Measurement] = []

    def add(self, measurement: Measurement) -> None:
        self._items.append(measurement)

    def all(self) -> tuple[Measurement, ...]:
        return tuple(self._items)

    def for_crew(self, crew_id: str) -> tuple[Measurement, ...]:
        return tuple(m for m in self._items if m.crew_id == crew_id)
