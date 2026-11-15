"""C5: simulated Earth -> spacecraft -> planet scenario with a fictitious crew."""

import itertools
from datetime import timedelta

import pytest

from crew_self_check.core.contract import (
    CrewProfile,
    Environment,
    Indicator,
    Measurement,
    Method,
    Reference,
    Source,
    Status,
)
from crew_self_check.core.scenario import Scenario, generate_scenario
from crew_self_check.core.status import IndicatorResolution, resolve_indicator

SEEDS = [0, 1, 7, 42, 2026]
EARTH, SHIP, PLANET = Environment.EARTH, Environment.SPACECRAFT, Environment.PLANET


def resolve_at(
    scenario: Scenario, day: int, crew_id: str, indicator: Indicator
) -> IndicatorResolution:
    when = scenario.days[day]
    profile = next(p for p in scenario.crew if p.crew_id == crew_id)
    return resolve_indicator(
        scenario.measurements_through(day),
        crew_id,
        indicator,
        when.environment,
        profile=profile,
        as_of=when.timestamp,
    )


def day_of(scenario: Scenario, label: str) -> int:
    return next(d.index for d in scenario.days if d.label == label)


def test_same_seed_gives_the_same_scenario() -> None:
    assert generate_scenario(5) == generate_scenario(5)


def test_different_seeds_give_different_readings() -> None:
    assert generate_scenario(1).measurements != generate_scenario(2).measurements


def test_the_default_seed_is_stable() -> None:
    assert generate_scenario() == generate_scenario(0)


@pytest.mark.parametrize("seed", SEEDS)
def test_every_reading_is_labelled_simulated_and_valid(seed: int) -> None:
    scenario = generate_scenario(seed)
    assert scenario.measurements
    for m in scenario.measurements:
        assert m.source is Source.SIMULATED_SCENARIO
        assert Measurement.from_dict(m.to_dict()) == m
    for profile in scenario.crew:
        assert CrewProfile.from_dict(profile.to_dict()) == profile


def test_the_journey_goes_earth_spacecraft_planet() -> None:
    days = generate_scenario().days
    environments = [d.environment for d in days]
    assert environments == [EARTH] * 14 + [SHIP] * 10 + [PLANET] * 4
    assert [d.index for d in days] == list(range(28))
    assert [d.label for d in days][:2] == ["E-14", "E-13"]
    assert days[13].label == "E-1"
    assert days[14].label == "T+1"
    assert days[23].label == "T+10"
    assert [d.label for d in days[-4:]] == ["R+0", "R+1", "R+2", "R+3"]
    for before, after in itertools.pairwise(days):
        assert after.timestamp - before.timestamp == timedelta(days=1)


def test_each_reading_sits_in_the_environment_of_its_day() -> None:
    scenario = generate_scenario()
    by_date = {d.timestamp.date(): d.environment for d in scenario.days}
    assert all(by_date[m.timestamp.date()] is m.environment for m in scenario.measurements)


def test_readings_are_sorted_in_time() -> None:
    stamps = [m.timestamp for m in generate_scenario().measurements]
    assert stamps == sorted(stamps)


def test_measurements_through_stops_at_the_given_day() -> None:
    scenario = generate_scenario()
    first = scenario.measurements_through(0)
    assert first
    assert all(m.timestamp <= scenario.days[0].timestamp for m in first)
    everything = scenario.measurements_through(len(scenario.days) - 1)
    assert everything == scenario.measurements
    with pytest.raises(IndexError):
        scenario.measurements_through(28)


def test_the_resting_pulse_is_always_entered_by_hand() -> None:
    pulses = [m for m in generate_scenario().measurements if m.indicator is Indicator.RESTING_HR]
    assert pulses
    assert all(m.method is Method.PALPATION for m in pulses)


def test_the_crew_is_fictitious_and_has_the_three_cases() -> None:
    crew = {p.crew_id: p for p in generate_scenario().crew}
    assert set(crew) == {"crew-01", "crew-02", "crew-03"}
    for profile in crew.values():
        assert "simulated" in profile.baseline_source


def test_crew_03_sleep_is_flagged_against_the_earth_baseline_then_against_her_own_range() -> None:
    """The isolation case: sleep drops in transit and stays flagged until arrival."""
    scenario = generate_scenario()
    early = resolve_at(scenario, day_of(scenario, "T+4"), "crew-03", Indicator.SLEEP_HOURS)
    assert early.status.status is Status.WATCH
    assert early.status.reference is Reference.TRANSITION
    assert early.status.baseline_environment is EARTH
    late = resolve_at(scenario, day_of(scenario, "T+10"), "crew-03", Indicator.SLEEP_HOURS)
    assert late.status.status is Status.WATCH
    assert late.status.reference is Reference.PERSONAL


def test_crew_03_mood_slips_in_transit() -> None:
    scenario = generate_scenario()
    mood = resolve_at(scenario, day_of(scenario, "T+5"), "crew-03", Indicator.MOOD)
    assert mood.status.status is Status.WATCH


def test_crew_03_cardiovascular_and_balance_stay_in_range_along_the_whole_journey() -> None:
    scenario = generate_scenario()
    steady = (
        Indicator.RESTING_HR,
        Indicator.SYSTOLIC_BP,
        Indicator.DIASTOLIC_BP,
        Indicator.VESTIBULAR_SYMPTOMS,
        Indicator.TANDEM_WALK_OK,
        Indicator.SPO2,
    )
    for day in scenario.days:
        for indicator in steady:
            status = resolve_at(scenario, day.index, "crew-03", indicator).status.status
            assert status in (Status.OK, Status.INSUFFICIENT_DATA), (day.label, indicator)


def test_crew_03_is_labelled_as_simulated_data() -> None:
    mine = [m for m in generate_scenario().measurements if m.crew_id == "crew-03"]
    assert mine
    assert {m.source for m in mine} == {Source.SIMULATED_SCENARIO}


@pytest.mark.parametrize("seed", SEEDS)
def test_the_four_states_appear_along_the_journey(seed: int) -> None:
    scenario = generate_scenario(seed)
    seen: set[Status] = set()
    for day in scenario.days:
        for profile in scenario.crew:
            for indicator in Indicator:
                seen.add(resolve_at(scenario, day.index, profile.crew_id, indicator).status.status)
    assert seen == set(Status)


@pytest.mark.parametrize("seed", SEEDS)
def test_the_earth_history_gives_a_personal_baseline(seed: int) -> None:
    scenario = generate_scenario(seed)
    result = resolve_at(scenario, day_of(scenario, "E-1"), "crew-01", Indicator.RESTING_HR)
    assert result.status.reference is Reference.PERSONAL
    assert result.status.status is Status.OK


@pytest.mark.parametrize("seed", SEEDS)
def test_arrival_is_gray_until_three_readings_then_amber_against_the_spacecraft(seed: int) -> None:
    scenario = generate_scenario(seed)
    r0 = resolve_at(scenario, day_of(scenario, "R+0"), "crew-01", Indicator.RESTING_HR)
    assert r0.status.status is Status.INSUFFICIENT_DATA
    assert r0.status.reference is Reference.TRANSITION
    assert r0.status.baseline_environment is SHIP
    for label in ("R+2", "R+3"):
        later = resolve_at(scenario, day_of(scenario, label), "crew-01", Indicator.RESTING_HR)
        assert later.status.status is Status.WATCH
        assert later.status.reference is Reference.TRANSITION
        assert later.status.baseline_environment is SHIP
    for indicator in (Indicator.ORTHOSTATIC_HR_DELTA, Indicator.VESTIBULAR_SYMPTOMS):
        last = resolve_at(scenario, day_of(scenario, "R+3"), "crew-01", indicator)
        assert last.status.status is Status.WATCH


@pytest.mark.parametrize("seed", SEEDS)
def test_the_sleep_drop_in_the_spacecraft_is_flagged_then_absorbed(seed: int) -> None:
    scenario = generate_scenario(seed)
    early = resolve_at(scenario, day_of(scenario, "T+3"), "crew-01", Indicator.SLEEP_HOURS)
    assert early.status.status is Status.WATCH
    assert early.status.reference is Reference.TRANSITION
    assert early.status.baseline_environment is EARTH
    late = resolve_at(scenario, day_of(scenario, "T+10"), "crew-01", Indicator.SLEEP_HOURS)
    assert late.status.status is Status.OK
    assert late.status.reference is Reference.PERSONAL


@pytest.mark.parametrize("seed", SEEDS)
def test_the_manual_pulse_without_history_uses_the_population_and_reaches_red(seed: int) -> None:
    scenario = generate_scenario(seed)
    states = {
        label: resolve_at(scenario, day_of(scenario, label), "crew-02", Indicator.RESTING_HR)
        for label in ("R+0", "R+1", "R+2", "R+3")
    }
    assert [s.status.status for s in states.values()] == [
        Status.OK,
        Status.WATCH,
        Status.ACT,
        Status.OK,
    ]
    assert all(s.status.reference is Reference.POPULATION for s in states.values())
    only_pulse = {m.indicator for m in scenario.measurements if m.crew_id == "crew-02"}
    assert only_pulse == {Indicator.RESTING_HR}


@pytest.mark.parametrize("seed", SEEDS)
def test_glucose_stays_gray_the_whole_trip(seed: int) -> None:
    scenario = generate_scenario(seed)
    for day in scenario.days:
        result = resolve_at(scenario, day.index, "crew-01", Indicator.BLOOD_GLUCOSE)
        assert result.status.status is Status.INSUFFICIENT_DATA


def test_stable_indicators_stay_green_on_the_planet() -> None:
    scenario = generate_scenario()
    last = day_of(scenario, "R+3")
    for indicator in (Indicator.SYSTOLIC_BP, Indicator.DIASTOLIC_BP, Indicator.MOOD):
        assert resolve_at(scenario, last, "crew-01", indicator).status.status is Status.OK
