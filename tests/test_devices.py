"""C6: the DeviceSource port and its helpers (core). Any object with the four methods fits."""

from datetime import UTC, datetime

import pytest

from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source
from crew_self_check.core.devices import DeviceReading, drain, to_measurement

T0 = datetime(2026, 11, 1, 7, 30, tzinfo=UTC)


def reading(value: float = 97.0, indicator: Indicator = Indicator.SPO2) -> DeviceReading:
    return DeviceReading(indicator, value, "%", T0, Source.SIMULATED_SCENARIO)


class FakeSource:
    """A hand-made adapter: nothing in common with the simulated one, only the port."""

    def __init__(self, batches: list[tuple[DeviceReading, ...]]) -> None:
        self._batches = batches
        self.calls: list[str] = []

    def capabilities(self) -> frozenset[Indicator]:
        return frozenset({Indicator.SPO2})

    def start(self) -> None:
        self.calls.append("start")

    def stop(self) -> None:
        self.calls.append("stop")

    def poll(self) -> tuple[DeviceReading, ...]:
        self.calls.append("poll")
        return self._batches.pop(0) if self._batches else ()


def test_a_reading_has_the_shape_of_d011() -> None:
    r = reading()
    assert (r.indicator, r.value, r.unit, r.timestamp, r.source) == (
        Indicator.SPO2,
        97.0,
        "%",
        T0,
        Source.SIMULATED_SCENARIO,
    )


def test_a_reading_becomes_a_device_measurement() -> None:
    m = to_measurement(reading(), "crew-01", Environment.SPACECRAFT)
    assert m == Measurement(
        crew_id="crew-01",
        indicator=Indicator.SPO2,
        value=97.0,
        unit="%",
        timestamp=T0,
        source=Source.SIMULATED_SCENARIO,
        environment=Environment.SPACECRAFT,
        method=Method.DEVICE,
    )
    assert Measurement.from_dict(m.to_dict()) == m  # it is a valid contract object


def test_the_method_can_be_overridden() -> None:
    m = to_measurement(reading(), "crew-01", Environment.EARTH, Method.SURVEY)
    assert m.method is Method.SURVEY


def test_a_reading_with_an_invalid_value_is_rejected() -> None:
    with pytest.raises(ValueError, match="value"):
        to_measurement(reading(float("nan")), "crew-01", Environment.EARTH)


def test_drain_turns_what_the_source_has_into_measurements_in_order() -> None:
    source = FakeSource([(reading(97), reading(96)), (reading(98),)])
    first = drain(source, "crew-01", Environment.EARTH)
    assert [m.value for m in first] == [97, 96]
    assert [m.value for m in drain(source, "crew-01", Environment.EARTH)] == [98]
    assert drain(source, "crew-01", Environment.EARTH) == ()


def test_drain_only_polls_the_lifecycle_belongs_to_the_caller() -> None:
    source = FakeSource([(reading(),)])
    drain(source, "crew-01", Environment.EARTH)
    assert source.calls == ["poll"]
