"""Part 2a: the manual pulse as a guided mission. Pure logic, with explicit times."""

from datetime import UTC, datetime

import pytest

from crew_self_check.astronaut.pulse_mission import (
    INTERVALS,
    MAX_PLAUSIBLE_BPM,
    MIN_PLAUSIBLE_BPM,
    PulseMission,
    Station,
)
from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source

NOW = datetime(2026, 11, 14, 21, 40, tzinfo=UTC)


def ready_to_count(interval: int = 30) -> PulseMission:
    mission = PulseMission(interval)
    for _ in range(3):
        mission.complete_station()
    return mission


def counted(taps: int, interval: int = 30) -> PulseMission:
    mission = ready_to_count(interval)
    mission.start_count(100.0)
    for i in range(taps):
        assert mission.tap(100.0 + i * interval / max(taps, 1) * 0.99)
    mission.finish(100.0 + interval)
    return mission


def test_the_mission_starts_at_rest_with_thirty_seconds() -> None:
    mission = PulseMission()
    assert mission.station is Station.REST
    assert mission.interval == 30
    assert mission.points == 0
    assert mission.result is None


def test_the_intervals_are_the_ones_of_the_guide() -> None:
    assert INTERVALS == (30, 60)
    with pytest.raises(ValueError, match="interval"):
        PulseMission(15)
    with pytest.raises(ValueError, match="interval"):
        PulseMission(45)


def test_the_three_steps_are_confirmed_in_order_and_then_it_is_time_to_count() -> None:
    mission = PulseMission()
    seen = [mission.station]
    for _ in range(3):
        mission.complete_station()
        seen.append(mission.station)
    assert seen == [Station.REST, Station.LOCATE, Station.PRESSURE, Station.COUNT]


def test_you_cannot_confirm_past_the_counting_station() -> None:
    mission = ready_to_count()
    with pytest.raises(RuntimeError, match="count"):
        mission.complete_station()


def test_you_cannot_count_before_the_steps_are_done() -> None:
    mission = PulseMission()
    with pytest.raises(RuntimeError, match="steps"):
        mission.start_count(0.0)
    mission.complete_station()
    with pytest.raises(RuntimeError, match="steps"):
        mission.start_count(0.0)


def test_taps_only_count_inside_the_counting_window() -> None:
    mission = ready_to_count(30)
    assert not mission.tap(99.0)  # not started
    mission.start_count(100.0)
    assert mission.tap(100.0)
    assert mission.tap(115.0)
    assert mission.tap(130.0)  # the last instant is still inside
    assert not mission.tap(130.01)  # too late
    assert mission.taps == 3


def test_the_remaining_time_counts_down_and_stops_at_zero() -> None:
    mission = ready_to_count(30)
    assert mission.remaining(0.0) == 30
    mission.start_count(100.0)
    assert mission.remaining(100.0) == 30
    assert mission.remaining(112.5) == pytest.approx(17.5)
    assert mission.remaining(500.0) == 0


def test_you_cannot_finish_before_the_time_is_up() -> None:
    mission = ready_to_count(30)
    mission.start_count(100.0)
    mission.tap(101.0)
    with pytest.raises(RuntimeError, match="time"):
        mission.finish(129.0)


@pytest.mark.parametrize(
    ("interval", "taps", "bpm"),
    [(30, 35, 70), (30, 31, 62), (60, 62, 62), (60, 75, 75), (30, 40, 80)],
)
def test_the_beats_become_beats_per_minute(interval: int, taps: int, bpm: int) -> None:
    mission = counted(taps, interval)
    assert mission.station is Station.RESULT
    assert mission.result is not None
    assert mission.result.taps == taps
    assert mission.result.interval == interval
    assert mission.result.bpm == bpm
    assert mission.result.valid


@pytest.mark.parametrize(
    ("taps", "valid"),
    [
        (0, False),
        (9, False),  # 18 bpm
        (10, True),  # 20 bpm: the lowest accepted
        (125, True),  # 250 bpm: the highest accepted
        (126, False),  # 252 bpm
    ],
)
def test_an_implausible_count_asks_for_a_recount(taps: int, valid: bool) -> None:
    assert (MIN_PLAUSIBLE_BPM, MAX_PLAUSIBLE_BPM) == (20, 250)
    mission = counted(taps, 30)
    assert mission.result is not None
    assert mission.result.valid is valid


def test_a_recount_goes_back_to_counting_without_repeating_the_steps() -> None:
    mission = counted(0)
    mission.retry()
    assert mission.station is Station.COUNT
    assert mission.taps == 0
    assert mission.result is None
    mission.start_count(500.0)
    mission.tap(501.0)
    mission.finish(530.0)
    assert mission.result is not None
    assert mission.result.taps == 1


def test_a_valid_result_cannot_be_retried_by_mistake() -> None:
    mission = counted(35)
    with pytest.raises(RuntimeError, match="retry"):
        mission.retry()


def test_the_interval_can_change_only_before_counting() -> None:
    mission = ready_to_count(30)
    mission.set_interval(60)
    assert mission.interval == 60
    mission.start_count(0.0)
    with pytest.raises(RuntimeError, match="interval"):
        mission.set_interval(30)


# --- the game rewards the technique, never the value ------------------------------------------


def test_points_come_from_the_steps_and_a_complete_measurement() -> None:
    mission = PulseMission()
    points = [mission.points]
    for _ in range(3):
        mission.complete_station()
        points.append(mission.points)
    assert points == [0, 10, 20, 30]
    mission.start_count(0.0)
    assert mission.points == 30
    for i in range(35):
        mission.tap(i * 0.8)
    mission.finish(30.0)
    assert mission.points == 30 + 10 + 20


@pytest.mark.parametrize("taps", [10, 22, 35, 60, 125])
def test_the_points_do_not_depend_on_how_high_or_low_the_pulse_is(taps: int) -> None:
    assert counted(taps).points == counted(35).points == 60


def test_a_recount_does_not_pay_the_bonus() -> None:
    assert counted(0).points == 30 + 10  # the steps and the attempt, but no measurement bonus


def test_the_badge_is_for_finishing_a_valid_measurement_only() -> None:
    assert not PulseMission().earned_badge
    assert not counted(0).earned_badge
    assert counted(35).earned_badge
    assert counted(125).earned_badge  # even a very high count: the badge is for the technique


# --- the result is a contract measurement -----------------------------------------------------


def test_the_result_becomes_a_manual_palpation_measurement() -> None:
    measurement = counted(35).to_measurement("crew-01", Environment.SPACECRAFT, NOW)
    assert measurement == Measurement(
        crew_id="crew-01",
        indicator=Indicator.RESTING_HR,
        value=70.0,
        unit="bpm",
        timestamp=NOW,
        source=Source.MANUAL,
        environment=Environment.SPACECRAFT,
        method=Method.PALPATION,
    )
    assert Measurement.from_dict(measurement.to_dict()) == measurement


def test_no_measurement_without_a_valid_result() -> None:
    with pytest.raises(RuntimeError, match="result"):
        PulseMission().to_measurement("crew-01", Environment.EARTH, NOW)
    with pytest.raises(RuntimeError, match="valid"):
        counted(0).to_measurement("crew-01", Environment.EARTH, NOW)


def test_it_is_counting_only_between_the_start_and_the_finish() -> None:
    mission = ready_to_count(30)
    assert not mission.counting
    mission.start_count(0.0)
    assert mission.counting
    mission.finish(30.0)
    assert not mission.counting
    mission.retry()
    assert not mission.counting
