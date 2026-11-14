"""C6: the simulated watch and band, and the engine consuming it without changes."""

from datetime import UTC, datetime, timedelta

import pytest

from crew_self_check.astronaut.simulated_device import SimulatedWearable
from crew_self_check.core.contract import (
    Environment,
    Indicator,
    Measurement,
    Method,
    Source,
)
from crew_self_check.core.devices import DeviceSource, drain
from crew_self_check.core.scenario import generate_scenario
from crew_self_check.core.status import resolve_indicator

T0 = datetime(2026, 11, 1, 7, 30, tzinfo=UTC)


def make(day: int, indicator: Indicator, value: float, method: Method = Method.DEVICE,
         crew_id: str = "crew-01") -> Measurement:  # fmt: skip
    return Measurement(
        crew_id, indicator, value, "u", T0 + timedelta(days=day),
        Source.SIMULATED_SCENARIO, Environment.EARTH, method,
    )  # fmt: skip


def test_it_fits_the_port() -> None:
    port: DeviceSource = SimulatedWearable([], "crew-01")
    assert port.capabilities() == frozenset()


def test_capabilities_are_what_the_devices_of_that_person_measure() -> None:
    data = [
        make(0, Indicator.SPO2, 98),
        make(0, Indicator.SLEEP_HOURS, 7),
        make(0, Indicator.RESTING_HR, 60, Method.PALPATION),  # counted by hand, not a device
        make(0, Indicator.BODY_TEMP, 36.6, crew_id="crew-02"),  # someone else
    ]
    assert SimulatedWearable(data, "crew-01").capabilities() == {
        Indicator.SPO2,
        Indicator.SLEEP_HOURS,
    }


def test_nothing_comes_out_before_start_or_before_the_clock_moves() -> None:
    device = SimulatedWearable([make(0, Indicator.SPO2, 98)], "crew-01")
    device.advance_to(T0)
    assert device.poll() == ()  # not started
    device.start()
    fresh = SimulatedWearable([make(0, Indicator.SPO2, 98)], "crew-01")
    fresh.start()
    assert fresh.poll() == ()  # the clock has not moved


def test_poll_delivers_each_reading_once_up_to_the_clock() -> None:
    device = SimulatedWearable(
        [make(0, Indicator.SPO2, 98), make(1, Indicator.SPO2, 97), make(2, Indicator.SPO2, 96)],
        "crew-01",
    )
    device.start()
    device.advance_to(T0 + timedelta(days=1))
    assert [r.value for r in device.poll()] == [98, 97]
    assert device.poll() == ()
    device.advance_to(T0 + timedelta(days=5))
    assert [r.value for r in device.poll()] == [96]


def test_readings_carry_what_the_device_measured() -> None:
    device = SimulatedWearable([make(0, Indicator.SPO2, 98)], "crew-01")
    device.start()
    device.advance_to(T0)
    (r,) = device.poll()
    assert (r.indicator, r.value, r.unit, r.timestamp, r.source) == (
        Indicator.SPO2, 98, "u", T0, Source.SIMULATED_SCENARIO,
    )  # fmt: skip


def test_stop_pauses_delivery_and_start_resumes_without_loss() -> None:
    device = SimulatedWearable(
        [make(0, Indicator.SPO2, 98), make(1, Indicator.SPO2, 97)], "crew-01"
    )
    device.start()
    device.advance_to(T0)
    assert len(device.poll()) == 1
    device.stop()
    device.advance_to(T0 + timedelta(days=1))
    assert device.poll() == ()
    device.start()
    assert [r.value for r in device.poll()] == [97]


def test_start_and_stop_are_idempotent() -> None:
    device = SimulatedWearable([make(0, Indicator.SPO2, 98)], "crew-01")
    device.stop()
    device.start()
    device.start()
    device.advance_to(T0)
    assert len(device.poll()) == 1
    device.stop()
    device.stop()


def test_the_clock_only_moves_forward_and_needs_a_timezone() -> None:
    device = SimulatedWearable([], "crew-01")
    device.advance_to(T0 + timedelta(days=1))
    with pytest.raises(ValueError, match="backwards"):
        device.advance_to(T0)
    with pytest.raises(ValueError, match="timezone"):
        device.advance_to(datetime(2026, 11, 3))


def test_the_input_order_does_not_matter() -> None:
    device = SimulatedWearable(
        [make(1, Indicator.SPO2, 97), make(0, Indicator.SPO2, 98)], "crew-01"
    )
    device.start()
    device.advance_to(T0 + timedelta(days=1))
    assert [r.value for r in device.poll()] == [98, 97]


# --- the engine consumes the simulator unchanged ------------------------------------------------


@pytest.mark.parametrize("seed", [0, 7])
def test_the_engine_resolves_the_same_from_the_device_stream_as_from_the_scenario(
    seed: int,
) -> None:
    scenario = generate_scenario(seed)
    device = SimulatedWearable(scenario.measurements, "crew-01")
    device.start()
    collected: list[Measurement] = []
    for day in scenario.days:
        device.advance_to(day.timestamp)
        collected.extend(drain(device, "crew-01", day.environment))
        for indicator in device.capabilities():
            direct = resolve_indicator(
                scenario.measurements_through(day.index), "crew-01", indicator, day.environment,
                as_of=day.timestamp,
            )  # fmt: skip
            streamed = resolve_indicator(
                collected, "crew-01", indicator, day.environment, as_of=day.timestamp
            )
            assert streamed == direct, (day.label, indicator)
    assert {m.indicator for m in collected} == device.capabilities()
    assert all(m.method is Method.DEVICE for m in collected)


def test_the_device_does_not_deliver_the_hand_counted_pulse() -> None:
    scenario = generate_scenario()
    device = SimulatedWearable(scenario.measurements, "crew-01")
    assert Indicator.RESTING_HR not in device.capabilities()
    assert Indicator.SLEEP_HOURS in device.capabilities()
