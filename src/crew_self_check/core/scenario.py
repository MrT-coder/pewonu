"""Simulated scenario: a fictitious crew travelling Earth -> spacecraft -> planet (D-013).

Everything here is **simulated, analog data** (``source: simulated-scenario``), never astronaut
data, and the crew is fictitious. The values are illustrative: they are shaped to show the four
states and the reference labels in the demo, not to model physiology.

- ``crew-01`` (38, female) has a simulated clinical history on Earth, so her baselines are personal.
  On the spacecraft her sleep drops (flagged against the Earth baseline until her own matures); on
  the planet (R+0 to R+3) pulse, the orthostatic delta and vestibular symptoms rise.
- ``crew-02`` (45, male) has no history and only enters the resting pulse by hand (D-014), so the
  state comes from the population table, up to red on R+2.
- Blood glucose is measured weekly: its normal state is gray (contract §1).

Reproducible: the same seed always gives the same scenario. Only ``random.Random(seed)`` is used.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from crew_self_check.core.contract import (
    CrewProfile,
    Environment,
    Indicator,
    Measurement,
    Method,
    Sex,
    Source,
)

EARTH_DAYS = 14
SHIP_DAYS = 10
PLANET_DAYS = 4  # R+0 to R+3
DEFAULT_START = datetime(2026, 11, 1, 7, 30, tzinfo=UTC)

CREW: tuple[CrewProfile, ...] = (
    CrewProfile("crew-01", 38, Sex.FEMALE, "simulated-clinical-history"),
    CrewProfile("crew-02", 45, Sex.MALE, "simulated-no-history"),
)


@dataclass(frozen=True, slots=True)
class ScenarioDay:
    index: int
    timestamp: datetime
    environment: Environment
    label: str  # E-14..E-1 (Earth), T+1..T+10 (transit), R+0..R+3 (arrival)


@dataclass(frozen=True, slots=True)
class Scenario:
    seed: int
    crew: tuple[CrewProfile, ...]
    days: tuple[ScenarioDay, ...]
    measurements: tuple[Measurement, ...]  # sorted by time

    def measurements_through(self, day_index: int) -> tuple[Measurement, ...]:
        """Everything measured up to and including that day (for the journey player)."""
        if not 0 <= day_index < len(self.days):
            raise IndexError(f"day {day_index} is outside 0..{len(self.days) - 1}")
        cutoff = self.days[day_index].timestamp
        return tuple(m for m in self.measurements if m.timestamp <= cutoff)


@dataclass(frozen=True, slots=True)
class _Spec:
    unit: str
    method: Method
    earth: float
    spacecraft: float
    planet: tuple[float, float, float, float]  # R+0 .. R+3
    noise: float = 0.0  # half width of the uniform noise (earth and spacecraft only)
    decimals: int = 0
    every: int = 1  # measured every N days


_SPECS: dict[Indicator, _Spec] = {
    Indicator.RESTING_HR: _Spec("bpm", Method.PALPATION, 60, 62, (72, 74, 76, 77), 2),
    Indicator.SYSTOLIC_BP: _Spec("mmHg", Method.DEVICE, 118, 118, (119, 118, 120, 118), 3),
    Indicator.DIASTOLIC_BP: _Spec("mmHg", Method.DEVICE, 76, 76, (77, 76, 76, 77), 2),
    Indicator.ORTHOSTATIC_HR_DELTA: _Spec("bpm", Method.DEVICE, 12, 14, (30, 32, 33, 31), 2),
    Indicator.VESTIBULAR_SYMPTOMS: _Spec("score", Method.SURVEY, 0, 0, (6, 7, 7, 6)),
    Indicator.TANDEM_WALK_OK: _Spec("0/1", Method.SURVEY, 1, 1, (1, 0, 0, 0)),
    Indicator.SLEEP_HOURS: _Spec("h", Method.DEVICE, 7.5, 6.0, (6.0, 6.1, 5.9, 6.0), 0.3, 1),
    Indicator.MOOD: _Spec("score", Method.SURVEY, 4, 4, (4, 4, 3, 4)),
    Indicator.SPO2: _Spec("%", Method.DEVICE, 98, 98, (98, 98, 97, 98)),
    Indicator.BODY_TEMP: _Spec("degC", Method.DEVICE, 36.6, 36.6, (36.7, 36.6, 36.7, 36.6), 0.1, 1),
    Indicator.BLOOD_GLUCOSE: _Spec("mg/dL", Method.DEVICE, 90, 90, (90, 90, 90, 90), 3, every=7),
}

# crew-02: resting pulse by hand, only on the last two transit days and on the arrival days.
_CREW_02_SHIP = {EARTH_DAYS + SHIP_DAYS - 2: 70.0, EARTH_DAYS + SHIP_DAYS - 1: 72.0}
_CREW_02_PLANET = (72.0, 94.0, 108.0, 80.0)  # male 40-59: ok, watch (>p95), act (>p99), ok


def _build_days(start: datetime) -> tuple[ScenarioDay, ...]:
    labels = (
        [(Environment.EARTH, f"E-{EARTH_DAYS - i}") for i in range(EARTH_DAYS)]
        + [(Environment.SPACECRAFT, f"T+{i + 1}") for i in range(SHIP_DAYS)]
        + [(Environment.PLANET, f"R+{i}") for i in range(PLANET_DAYS)]
    )
    return tuple(
        ScenarioDay(i, start + timedelta(days=i), environment, label)
        for i, (environment, label) in enumerate(labels)
    )


def _value(spec: _Spec, day: ScenarioDay, rng: random.Random) -> float:
    if day.environment is Environment.PLANET:
        return spec.planet[day.index - EARTH_DAYS - SHIP_DAYS]
    mean = spec.earth if day.environment is Environment.EARTH else spec.spacecraft
    if spec.noise:
        mean += rng.uniform(-spec.noise, spec.noise)
    return round(mean, spec.decimals)


def _reading(
    crew_id: str,
    indicator: Indicator,
    value: float,
    unit: str,
    method: Method,
    day: ScenarioDay,
) -> Measurement:
    return Measurement(
        crew_id=crew_id,
        indicator=indicator,
        value=value,
        unit=unit,
        timestamp=day.timestamp,
        source=Source.SIMULATED_SCENARIO,
        environment=day.environment,
        method=method,
    )


def generate_scenario(seed: int = 0, start: datetime = DEFAULT_START) -> Scenario:
    """Build the scenario. Same ``seed`` and ``start`` always give the same result."""
    rng = random.Random(seed)
    days = _build_days(start)
    readings: list[Measurement] = []
    for day in days:
        for indicator, spec in _SPECS.items():
            if day.index % spec.every:
                continue
            value = _value(spec, day, rng)
            readings.append(_reading("crew-01", indicator, value, spec.unit, spec.method, day))
        pulse = _CREW_02_SHIP.get(day.index)
        if day.environment is Environment.PLANET:
            pulse = _CREW_02_PLANET[day.index - EARTH_DAYS - SHIP_DAYS]
        if pulse is not None:
            readings.append(
                _reading("crew-02", Indicator.RESTING_HR, pulse, "bpm", Method.PALPATION, day)
            )
    readings.sort(key=lambda m: m.timestamp)
    return Scenario(seed, CREW, days, tuple(readings))
