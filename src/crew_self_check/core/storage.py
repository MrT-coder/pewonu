"""Storage port for what the astronaut records (D-017). Pure Python; adapters live elsewhere."""

from __future__ import annotations

from typing import Protocol

from crew_self_check.core.contract import Measurement, VoiceFeatures


class MeasurementStore(Protocol):
    """Where recorded measurements are kept. Order of insertion is preserved."""

    def add(self, measurement: Measurement) -> None: ...

    def all(self) -> tuple[Measurement, ...]: ...

    def for_crew(self, crew_id: str) -> tuple[Measurement, ...]: ...


class VoiceStore(Protocol):
    """Where the numbers of voice notes are kept: never audio, never a transcript."""

    def add(self, note: VoiceFeatures) -> None: ...

    def all(self) -> tuple[VoiceFeatures, ...]: ...

    def for_crew(self, crew_id: str) -> tuple[VoiceFeatures, ...]: ...


class InMemoryVoiceStore:
    def __init__(self) -> None:
        self._items: list[VoiceFeatures] = []

    def add(self, note: VoiceFeatures) -> None:
        self._items.append(note)

    def all(self) -> tuple[VoiceFeatures, ...]:
        return tuple(self._items)

    def for_crew(self, crew_id: str) -> tuple[VoiceFeatures, ...]:
        return tuple(n for n in self._items if n.crew_id == crew_id)


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
