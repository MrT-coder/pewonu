"""The ``DeviceSource`` port (D-011): where readings come from, behind one interface.

Adapters (simulated watch and band, file import, later Bluetooth or serial) live in the systems
(``astronaut``), not here. The engine never knows which one it is talking to: it receives
``Measurement`` objects, and ``drain`` is the only step between a source and the engine.

``DeviceReading`` has the shape of D-011 (type, value, unit, time, source). It is a port type, not
part of the data contract: the device does not know the crew member or the environment, so those
are added when the reading becomes a ``Measurement``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source


@dataclass(frozen=True, slots=True)
class DeviceReading:
    indicator: Indicator
    value: float
    unit: str
    timestamp: datetime
    source: Source


class DeviceSource(Protocol):
    """A source of device readings. Structural: any object with these methods fits.

    ``start`` and ``stop`` are idempotent. ``poll`` returns the readings produced since the last
    call, oldest first, each one exactly once; it returns nothing while the source is stopped.
    """

    def capabilities(self) -> frozenset[Indicator]:
        """The indicators this source can deliver."""
        ...

    def start(self) -> None: ...

    def stop(self) -> None: ...

    def poll(self) -> tuple[DeviceReading, ...]: ...


def to_measurement(
    reading: DeviceReading,
    crew_id: str,
    environment: Environment,
    method: Method = Method.DEVICE,
) -> Measurement:
    """Turn a device reading into a contract ``Measurement`` (validated by the contract)."""
    measurement = Measurement(
        crew_id=crew_id,
        indicator=reading.indicator,
        value=float(reading.value),
        unit=reading.unit,
        timestamp=reading.timestamp,
        source=reading.source,
        environment=environment,
        method=method,
    )
    return Measurement.from_dict(measurement.to_dict())


def drain(source: DeviceSource, crew_id: str, environment: Environment) -> tuple[Measurement, ...]:
    """Poll ``source`` once and return its new readings as measurements, oldest first.

    It never starts or stops the source: its lifecycle belongs to the caller.
    """
    return tuple(to_measurement(reading, crew_id, environment) for reading in source.poll())
