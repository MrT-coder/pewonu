"""What the ground base has received (D-018). Pure Python: the adapters live in ``ground``."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ReceivedBundle:
    """A valid FHIR Bundle the astronaut chose to send, with when it becomes visible."""

    bundle_id: str
    crew_id: str
    sent_at: datetime  # the Bundle's own timestamp: when the astronaut confirmed
    received_at: datetime  # when the ground service took it in
    available_at: datetime  # received_at + the communication delay
    bundle: dict[str, Any]
    readings: int
    states: int


class BundleInbox(Protocol):
    def add(self, item: ReceivedBundle) -> None: ...

    def get(self, bundle_id: str) -> ReceivedBundle | None: ...

    def all(self) -> tuple[ReceivedBundle, ...]: ...


class InMemoryBundleInbox:
    """Default adapter and test double: nothing survives a restart."""

    def __init__(self) -> None:
        self._items: dict[str, ReceivedBundle] = {}

    def add(self, item: ReceivedBundle) -> None:
        self._items.setdefault(item.bundle_id, item)

    def get(self, bundle_id: str) -> ReceivedBundle | None:
        return self._items.get(bundle_id)

    def all(self) -> tuple[ReceivedBundle, ...]:
        return tuple(self._items.values())
