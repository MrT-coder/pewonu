"""What the astronaut sends to the ground team, and where it is on its way (A10, D-006, D-018).

The package is a FHIR ``Bundle`` built by ``core.fhir`` and only from what the astronaut chose and
confirmed. The delay between sending and arriving is simulated (the real trip would be DTN, D-008).
The ground base does not exist yet (G1): "delivered" only moves the package to a local inbox.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any

from crew_self_check.core.contract import Indicator

# [SUPOSICION] one value inside the 3 to 22 minutes of D-018, configurable on the state.
DEFAULT_GROUND_DELAY_MINUTES = 12


class DeliveryState(StrEnum):
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


@dataclass(frozen=True, slots=True)
class OutboxItem:
    crew_id: str
    day_label: str  # the journey day it was sent
    sent_at: datetime
    arrives_at: datetime
    bundle: dict[str, Any]
    readings: int
    states: int
    indicators: tuple[Indicator, ...]
    voices: int = 0  # voice notes in the package (numbers only)


def delivery_state(item: OutboxItem, now: datetime) -> DeliveryState:
    return DeliveryState.DELIVERED if now >= item.arrives_at else DeliveryState.IN_TRANSIT
