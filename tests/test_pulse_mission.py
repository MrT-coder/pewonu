"""Part 2a: the manual pulse as a guided mission. The astronaut counts and enters the beats."""

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


def counted(beats: int, interval: int = 30) -> PulseMission:
    mission = ready_to_count(interval)
    mission.submit_count(beats)
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


def test_you_cannot_enter_a_count_before_the_steps_are_done() -> None:
    mission = PulseMission()
    with pytest.raises(RuntimeError, match="steps"):
        mission.submit_count(35)
    mission.complete_station()
    with pytest.raises(RuntimeError, match="steps"):
        mission.submit_count(35)


@pytest.mark.parametrize(
    ("interval", "beats", "bpm"),
    [(30, 35, 70), (30, 31, 62), (60, 62, 62), (60, 75, 75), (30, 40, 80)],
)
def test_the_beats_become_beats_per_minute(interval: int, beats: int, bpm: int) -> None:
    mission = counted(beats, interval)
    assert mission.station is Station.RESULT
    assert mission.result is not None
    assert mission.result.beats == beats
    assert mission.result.interval == interval
    assert mission.result.bpm == bpm
    assert mission.result.valid


def test_the_submitted_result_is_returned() -> None:
    mission = ready_to_count()
    assert mission.submit_count(35) is mission.result


@pytest.mark.parametrize(
    ("beats", "valid"),
    [
        (0, False),
        (9, False),  # 18 bpm
        (10, True),  # 20 bpm: the lowest accepted
        (125, True),  # 250 bpm: the highest accepted
        (126, False),  # 252 bpm
        (400, False),
    ],
)
def test_an_implausible_count_asks_for_a_recount(beats: int, valid: bool) -> None:
    assert (MIN_PLAUSIBLE_BPM, MAX_PLAUSIBLE_BPM) == (20, 250)
    mission = counted(beats, 30)
    assert mission.result is not None
    assert mission.result.valid is valid


@pytest.mark.parametrize("beats", [-1, 3.5, "35", None, True])
def test_what_is_not_a_whole_number_of_beats_is_refused(beats: object) -> None:
    mission = ready_to_count()
    with pytest.raises(ValueError, match="beats"):
        mission.submit_count(beats)  # type: ignore[arg-type]
    assert mission.station is Station.COUNT
    assert mission.result is None


def test_the_count_can_only_be_entered_once_until_a_recount() -> None:
    mission = counted(35)
    with pytest.raises(RuntimeError, match="count"):
        mission.submit_count(36)


def test_a_recount_goes_back_to_counting_without_repeating_the_steps() -> None:
    mission = counted(0)
    mission.retry()
    assert mission.station is Station.COUNT
    assert mission.result is None
    mission.submit_count(35)
    assert mission.result is not None
    assert mission.result.bpm == 70


def test_a_valid_result_cannot_be_retried_by_mistake() -> None:
    mission = counted(35)
    with pytest.raises(RuntimeError, match="retry"):
        mission.retry()


def test_the_interval_can_change_until_the_count_is_entered() -> None:
    mission = ready_to_count(30)
    mission.set_interval(60)
    assert mission.interval == 60
    mission.submit_count(70)
    assert mission.result is not None
    assert mission.result.bpm == 70
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
    mission.submit_count(35)
    assert mission.points == 30 + 10 + 20


@pytest.mark.parametrize("beats", [10, 22, 35, 60, 125])
def test_the_points_do_not_depend_on_how_high_or_low_the_pulse_is(beats: int) -> None:
    assert counted(beats).points == counted(35).points == 60


def test_a_recount_does_not_pay_the_bonus_and_does_not_pay_twice() -> None:
    mission = counted(0)
    assert mission.points == 30 + 10  # the steps and the attempt, but no measurement bonus
    mission.retry()
    mission.submit_count(35)
    assert mission.points == 60  # not 70: the attempt is paid once


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
