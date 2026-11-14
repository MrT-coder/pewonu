"""Simulated watch and band: an adapter of the ``DeviceSource`` port (D-011).

It replays the device readings of one crew member from a list of measurements (the simulated
scenario, C5), as the journey clock advances. Everything it delivers is labelled by the source it
was given (``simulated-scenario``): it is simulated data, never astronaut data.

Only readings taken with ``method: device`` are delivered. The resting pulse is counted by hand
(D-014), so it does not come from here.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from datetime import datetime

from crew_self_check.core.contract import Indicator, Measurement, Method
from crew_self_check.core.devices import DeviceReading


class SimulatedWearable:
    def __init__(self, measurements: Iterable[Measurement], crew_id: str) -> None:
        own = sorted(
            (m for m in measurements if m.crew_id == crew_id and m.method is Method.DEVICE),
            key=lambda m: m.timestamp,
        )
        self._pending: deque[Measurement] = deque(own)
        self._capabilities = frozenset(m.indicator for m in own)
        self._now: datetime | None = None
        self._running = False

    def capabilities(self) -> frozenset[Indicator]:
        return self._capabilities

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        """Pause delivery. Readings that fall due meanwhile are kept for the next ``start``."""
        self._running = False

    def advance_to(self, when: datetime) -> None:
        """Move the simulated clock (not part of the port: only a simulation needs it)."""
        if when.tzinfo is None:
            raise ValueError("when needs a timezone")
        if self._now is not None and when < self._now:
            raise ValueError("the simulated clock cannot go backwards")
        self._now = when

    def poll(self) -> tuple[DeviceReading, ...]:
        if not self._running or self._now is None:
            return ()
        due: list[DeviceReading] = []
        while self._pending and self._pending[0].timestamp <= self._now:
            m = self._pending.popleft()
            due.append(DeviceReading(m.indicator, m.value, m.unit, m.timestamp, m.source))
        return tuple(due)
