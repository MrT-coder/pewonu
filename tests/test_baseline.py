"""C3: per-person baseline engine (D-013): robust band, sustained deviation, insufficient data."""

from datetime import UTC, datetime, timedelta

import pytest

from crew_self_check.core.baseline import (
    DEFAULT_CONFIG,
    BaselineAssessment,
    BaselineConfig,
    Direction,
    assess,
)
from crew_self_check.core.contract import (
    Environment,
    Indicator,
    Measurement,
    Source,
    Status,
)

START = datetime(2026, 11, 1, 7, 30, tzinfo=UTC)


def reading(
    day: int,
    value: float,
    *,
    environment: Environment = Environment.EARTH,
    crew_id: str = "crew-01",
    indicator: Indicator = Indicator.RESTING_HR,
    hour: int = 0,
) -> Measurement:
    return Measurement(
        crew_id=crew_id,
        indicator=indicator,
        value=value,
        unit="bpm",
        timestamp=START + timedelta(days=day, hours=hour),
        source=Source.SIMULATED_SCENARIO,
        environment=environment,
    )


def daily(values: list[float], **kwargs: object) -> list[Measurement]:
    return [reading(day, value, **kwargs) for day, value in enumerate(values)]  # type: ignore[arg-type]


def run(
    measurements: list[Measurement],
    environment: Environment = Environment.EARTH,
    config: BaselineConfig = DEFAULT_CONFIG,
) -> BaselineAssessment:
    return assess(measurements, "crew-01", Indicator.RESTING_HR, environment, config)


# Seven stable baseline days: median 60, MAD 1 -> scaled 1.4826, band 60 +- 2.5 * 1.4826.
STABLE = [60, 61, 59, 60, 62, 58, 60]
LOW, HIGH = 60 - 2.5 * 1.4826, 60 + 2.5 * 1.4826


def test_no_data_is_gray() -> None:
    result = run([])
    assert result.status is Status.INSUFFICIENT_DATA
    assert result.baseline is None
    assert result.latest is None
    assert result.recent == ()
    assert result.direction is None


def test_many_readings_on_one_day_are_still_gray() -> None:
    many = [reading(0, 60 + i % 3, hour=i % 20) for i in range(30)]
    assert run(many).status is Status.INSUFFICIENT_DATA


def test_baseline_needs_the_minimum_number_of_days() -> None:
    # 5 baseline days + the 3 recent readings: mature. One day less: gray.
    mature = daily([60, 61, 59, 60, 62, 60, 61, 59])
    assert run(mature).status is Status.OK
    short = daily([60, 61, 59, 60, 60, 61, 59])
    result = run(short)
    assert result.status is Status.INSUFFICIENT_DATA
    assert result.baseline is None


def test_gray_still_reports_the_latest_reading() -> None:
    result = run(daily([60, 61, 59]))
    assert result.status is Status.INSUFFICIENT_DATA
    assert result.latest == 59
    assert [p.value for p in result.recent] == [60, 61, 59]


def test_stable_readings_are_ok_with_the_robust_band() -> None:
    result = run(daily([*STABLE, 60, 61, 59]))
    assert result.status is Status.OK
    assert result.direction is None
    assert result.baseline is not None
    assert result.baseline.center == 60
    assert result.baseline.low == pytest.approx(LOW)
    assert result.baseline.high == pytest.approx(HIGH)
    assert result.baseline.n_days == 7
    assert result.latest == 59


def test_three_sustained_readings_above_the_band_are_amber() -> None:
    result = run(daily([*STABLE, 70, 71, 72]))
    assert result.status is Status.WATCH
    assert result.direction is Direction.ABOVE
    assert [p.value for p in result.recent] == [70, 71, 72]
    assert result.latest == 72


def test_three_sustained_readings_below_the_band_are_amber() -> None:
    result = run(daily([*STABLE, 50, 49, 48]))
    assert result.status is Status.WATCH
    assert result.direction is Direction.BELOW


@pytest.mark.parametrize(
    "recent",
    [
        [70, 71, 60],  # only two out, the last one back in band
        [70, 60, 71],  # not consecutive
        [60, 70, 71],
        [70, 50, 71],  # out of band on both sides: erratic, not a sustained shift
    ],
)
def test_it_is_not_amber_without_three_sustained_readings_on_one_side(recent: list[float]) -> None:
    assert run(daily(STABLE + recent)).status is Status.OK


def test_band_edges_are_inside() -> None:
    edge = 60 + 2.5 * 1.4826
    assert run(daily([*STABLE, edge, edge, edge])).status is Status.OK
    assert run(daily(STABLE + [edge + 0.01] * 3)).status is Status.WATCH


def test_recent_readings_do_not_contaminate_the_baseline() -> None:
    with_shift = run(daily([*STABLE, 70, 71, 72]))
    without = run(daily([*STABLE, 60, 60, 60]))
    assert with_shift.baseline == without.baseline


def test_each_environment_has_its_own_baseline() -> None:
    earth = daily([*STABLE, 60, 61, 59])
    spacecraft = daily([75, 76], environment=Environment.SPACECRAFT)
    alone = run(earth)
    both_earth = run(earth + spacecraft)
    both_ship = run(earth + spacecraft, Environment.SPACECRAFT)
    assert both_earth == alone  # spacecraft readings do not leak into earth
    assert both_ship.status is Status.INSUFFICIENT_DATA  # and earth does not give a baseline to it
    assert both_ship.baseline is None
    assert both_ship.latest == 76


def test_baselines_differ_per_environment_when_both_are_mature() -> None:
    earth = daily([*STABLE, 60, 60, 60])
    ship = daily([70, 71, 69, 70, 72, 68, 70, 70, 70, 70], environment=Environment.SPACECRAFT)
    a = run(earth + ship, Environment.EARTH)
    b = run(earth + ship, Environment.SPACECRAFT)
    assert a.baseline is not None
    assert b.baseline is not None
    assert (a.baseline.center, b.baseline.center) == (60, 70)
    assert a.status is b.status is Status.OK


def test_other_people_and_other_indicators_are_ignored() -> None:
    noise = daily([99] * 12, crew_id="crew-02") + daily([99] * 12, indicator=Indicator.SPO2)
    assert run(daily([*STABLE, 60, 61, 59]) + noise).status is Status.OK
    assert run(noise).status is Status.INSUFFICIENT_DATA


def test_input_order_does_not_matter() -> None:
    data = daily([*STABLE, 70, 71, 72])
    assert run(list(reversed(data))) == run(data)


def test_constant_history_gives_a_degenerate_band() -> None:
    assert run(daily([60] * 7 + [60, 60, 60])).status is Status.OK
    shifted = run(daily([60] * 7 + [61, 61, 61]))
    assert shifted.status is Status.WATCH
    assert shifted.baseline is not None
    assert shifted.baseline.low == shifted.baseline.high == 60


def test_binary_indicator_works_with_the_same_engine() -> None:
    ok = [reading(d, 1, indicator=Indicator.TANDEM_WALK_OK) for d in range(7)]
    failed = [reading(7 + d, 0, indicator=Indicator.TANDEM_WALK_OK) for d in range(3)]
    result = assess(ok + failed, "crew-01", Indicator.TANDEM_WALK_OK, Environment.EARTH)
    assert result.status is Status.WATCH
    assert result.direction is Direction.BELOW


def test_config_is_configurable() -> None:
    strict = BaselineConfig(min_days=3, sustained=2, band_k=1.0)
    data = daily([60, 61, 59, 65, 66])
    assert run(data, config=strict).status is Status.WATCH
    assert run(data).status is Status.INSUFFICIENT_DATA


@pytest.mark.parametrize(
    "kwargs",
    [{"min_days": 0}, {"sustained": 0}, {"band_k": 0}, {"band_k": -1.0}, {"band_k": float("nan")}],
)
def test_invalid_config_is_rejected(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        BaselineConfig(**kwargs)  # type: ignore[arg-type]


def test_default_config_values_are_the_documented_ones() -> None:
    assert (DEFAULT_CONFIG.min_days, DEFAULT_CONFIG.sustained, DEFAULT_CONFIG.band_k) == (5, 3, 2.5)


def test_repeated_values_do_not_collapse_the_band() -> None:
    # More than half of the history is 59, so the MAD is 0, but the history does spread.
    # Before the fallback the band was the single point 59 and [60, 62, 61] raised amber.
    history = [59, 59, 59, 59, 59, 57, 61]
    result = run(daily([*history, 60, 62, 61]))
    assert result.status is Status.OK
    assert result.baseline is not None
    assert result.baseline.low < 59 < result.baseline.high
    # A real sustained shift is still caught.
    assert run(daily([*history, 64, 65, 64])).status is Status.WATCH
