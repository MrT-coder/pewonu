"""C4: status resolution: reference, indicator status, system status, escalation, reasons."""

from datetime import UTC, datetime, timedelta

import pytest

from crew_self_check.core.contract import (
    CrewProfile,
    Environment,
    Escalation,
    Indicator,
    IndicatorStatus,
    Measurement,
    Reference,
    Sex,
    Source,
    Status,
    System,
    SystemStatus,
)
from crew_self_check.core.reasons import Language, ReasonCode
from crew_self_check.core.status import (
    SYSTEM_INDICATORS,
    IndicatorResolution,
    escalation_for,
    resolve_indicator,
    resolve_system,
)

START = datetime(2026, 11, 1, 7, 30, tzinfo=UTC)
STABLE = [60, 61, 59, 60, 62, 58, 60]  # median 60, band 60 +- 3.7065
EARTH, SHIP, PLANET = Environment.EARTH, Environment.SPACECRAFT, Environment.PLANET
MALE_30 = CrewProfile("crew-01", 30, Sex.MALE, "simulated-clinical-history")


def series(
    values: list[float],
    environment: Environment = EARTH,
    *,
    first_day: int = 0,
    indicator: Indicator = Indicator.RESTING_HR,
    crew_id: str = "crew-01",
) -> list[Measurement]:
    return [
        Measurement(
            crew_id,
            indicator,
            value,
            "bpm",
            START + timedelta(days=first_day + i),
            Source.SIMULATED_SCENARIO,
            environment,
        )
        for i, value in enumerate(values)
    ]


def resolve(
    data: list[Measurement],
    environment: Environment = EARTH,
    indicator: Indicator = Indicator.RESTING_HR,
    **kwargs: object,
) -> IndicatorResolution:
    return resolve_indicator(data, "crew-01", indicator, environment, **kwargs)  # type: ignore[arg-type]


def assert_contract_valid(resolution: IndicatorResolution) -> None:
    status = resolution.status
    assert IndicatorStatus.from_dict(status.to_dict()) == status
    assert status.reason == resolution.reason.text(Language.EN)


# --- the four states, personal reference ---------------------------------------------------------


def test_gray_without_data() -> None:
    result = resolve([])
    assert result.status.status is Status.INSUFFICIENT_DATA
    assert result.reason.code is ReasonCode.NO_DATA
    assert result.status.latest is None
    assert_contract_valid(result)


def test_gray_while_the_baseline_builds_and_without_a_profile() -> None:
    result = resolve(series([60, 61, 59]))
    assert result.status.status is Status.INSUFFICIENT_DATA
    assert result.status.reference is Reference.PERSONAL
    assert result.reason.code is ReasonCode.BUILDING_BASELINE
    assert result.reason.params == {"days": 3, "needed": 5}
    assert result.status.escalation is Escalation.SELF_CARE
    assert_contract_valid(result)


def test_green_with_a_personal_baseline() -> None:
    result = resolve(series([*STABLE, 60, 61, 59]))
    status = result.status
    assert status.status is Status.OK
    assert status.reference is Reference.PERSONAL
    assert status.baseline is not None
    assert status.baseline.center == 60
    assert status.baseline_environment is None
    assert status.escalation is Escalation.SELF_CARE
    assert result.reason.code is ReasonCode.PERSONAL_OK
    assert [p.value for p in status.trend] == [60, 61, 59]
    assert_contract_valid(result)


def test_amber_with_three_readings_above_the_personal_range() -> None:
    result = resolve(series([*STABLE, 70, 71, 72]))
    assert result.status.status is Status.WATCH
    assert result.status.reference is Reference.PERSONAL
    assert result.status.escalation is Escalation.CREW_CMO
    assert result.status.reason == "3 consecutive readings above personal range"
    assert result.status.latest == 72
    assert_contract_valid(result)


def test_amber_below_the_personal_range() -> None:
    result = resolve(series([*STABLE, 50, 49, 48]))
    assert result.status.status is Status.WATCH
    assert result.reason.code is ReasonCode.PERSONAL_BELOW


# --- transition ---------------------------------------------------------------


def test_transition_waits_for_enough_readings() -> None:
    data = series([*STABLE, 60, 61, 59]) + series([62, 63], SHIP, first_day=10)
    result = resolve(data, SHIP)
    status = result.status
    assert status.status is Status.INSUFFICIENT_DATA
    assert status.reference is Reference.TRANSITION
    assert status.baseline_environment is EARTH
    assert result.reason.code is ReasonCode.WAITING_TRANSITION
    assert result.reason.params == {"have": 2, "needed": 3, "previous": EARTH}
    assert_contract_valid(result)


def test_transition_is_green_when_readings_stay_in_the_previous_band() -> None:
    data = series([*STABLE, 60, 61, 59]) + series([60, 61, 62], SHIP, first_day=10)
    result = resolve(data, SHIP)
    assert result.status.status is Status.OK
    assert result.status.reference is Reference.TRANSITION
    assert result.status.baseline is not None
    assert result.status.baseline.center == 60  # the band that was used: the Earth one
    assert result.reason.code is ReasonCode.TRANSITION_OK
    assert_contract_valid(result)


def test_transition_is_amber_when_readings_leave_the_previous_band() -> None:
    data = series([*STABLE, 60, 61, 59]) + series([72, 73, 74], SHIP, first_day=10)
    result = resolve(data, SHIP)
    assert result.status.status is Status.WATCH
    assert result.status.reference is Reference.TRANSITION
    assert result.status.escalation is Escalation.CREW_CMO
    assert result.reason.code is ReasonCode.TRANSITION_ABOVE
    assert_contract_valid(result)


def test_the_own_baseline_takes_over_when_it_matures() -> None:
    ship = series([72, 73, 71, 72, 74, 70, 72, 72, 72, 72], SHIP, first_day=10)
    result = resolve(series([*STABLE, 60, 61, 59]) + ship, SHIP)
    assert result.status.reference is Reference.PERSONAL
    assert result.status.baseline_environment is None
    assert result.status.baseline is not None
    assert result.status.baseline.center == 72
    assert result.status.status is Status.OK


def test_planet_compares_with_the_spacecraft_when_it_has_a_baseline() -> None:
    earth = series([*STABLE, 60, 61, 59])
    ship = series([72, 73, 71, 72, 74, 70, 72, 72, 72, 72], SHIP, first_day=10)
    planet = series([72, 71, 73], PLANET, first_day=20)
    result = resolve(earth + ship + planet, PLANET)
    assert result.status.reference is Reference.TRANSITION
    assert result.status.baseline_environment is SHIP
    assert result.status.baseline is not None
    assert result.status.baseline.center == 72


def test_planet_falls_back_to_earth_when_the_spacecraft_has_no_baseline() -> None:
    earth = series([*STABLE, 60, 61, 59])
    planet = series([60, 61, 59], PLANET, first_day=20)
    result = resolve(earth + planet, PLANET)
    assert result.status.baseline_environment is EARTH


def test_earth_never_uses_the_transition() -> None:
    ship = series([*STABLE, 60, 61, 59], SHIP)
    assert resolve(ship + series([60], EARTH, first_day=30), EARTH).status.reference is not (
        Reference.TRANSITION
    )


# --- population ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("bpm", "status", "escalation", "code"),
    [
        (70, Status.OK, Escalation.SELF_CARE, ReasonCode.POPULATION_OK),
        (95, Status.WATCH, Escalation.CREW_CMO, ReasonCode.POPULATION_WATCH_HIGH),
        (50, Status.WATCH, Escalation.CREW_CMO, ReasonCode.POPULATION_WATCH_LOW),
        (105, Status.ACT, Escalation.GROUND_SURGEON, ReasonCode.POPULATION_ACT_HIGH),
        (44, Status.ACT, Escalation.GROUND_SURGEON, ReasonCode.POPULATION_ACT_LOW),
    ],
)
def test_population_reference_while_there_is_no_personal_baseline(
    bpm: float, status: Status, escalation: Escalation, code: ReasonCode
) -> None:
    result = resolve(series([bpm]), profile=MALE_30)  # male 20-39: p1 47, p5 52, p95 89, p99 101
    assert result.status.status is status
    assert result.status.reference is Reference.POPULATION
    assert result.status.baseline is None
    assert result.status.escalation is escalation
    assert result.reason.code is code
    assert "population" in result.status.reason.lower()
    assert "poblaci" in result.reason.text(Language.ES).lower()
    assert_contract_valid(result)


def test_the_personal_baseline_wins_over_the_population() -> None:
    result = resolve(series([*STABLE, 60, 61, 59]), profile=MALE_30)
    assert result.status.reference is Reference.PERSONAL


def test_the_transition_wins_over_the_population() -> None:
    data = series([*STABLE, 60, 61, 59]) + series([60, 61, 62], SHIP, first_day=10)
    assert resolve(data, SHIP, profile=MALE_30).status.reference is Reference.TRANSITION


def test_population_only_applies_to_resting_pulse() -> None:
    result = resolve(
        series([97], indicator=Indicator.SPO2), indicator=Indicator.SPO2, profile=MALE_30
    )
    assert result.status.status is Status.INSUFFICIENT_DATA
    assert result.status.reference is Reference.PERSONAL


def test_population_needs_a_profile_inside_the_table() -> None:
    old = CrewProfile("crew-01", 85, Sex.MALE, "simulated-clinical-history")
    assert resolve(series([70]), profile=old).status.status is Status.INSUFFICIENT_DATA
    assert resolve(series([70])).status.status is Status.INSUFFICIENT_DATA


def test_population_uses_the_profile_of_the_person_asked() -> None:
    other = CrewProfile("crew-02", 30, Sex.MALE, "simulated-clinical-history")
    assert resolve(series([70]), profile=other).status.status is Status.INSUFFICIENT_DATA


# --- stale readings -----------------------------------------------------------


def test_old_latest_reading_turns_gray_when_a_clock_is_given() -> None:
    data = series([*STABLE, 60, 61, 59])
    last = data[-1].timestamp
    fresh = resolve(data, as_of=last + timedelta(days=3))
    assert fresh.status.status is Status.OK
    stale = resolve(data, as_of=last + timedelta(days=3, minutes=1))
    assert stale.status.status is Status.INSUFFICIENT_DATA
    assert stale.reason.code is ReasonCode.STALE_READING
    assert stale.status.reference is Reference.PERSONAL
    assert_contract_valid(stale)


def test_population_goes_gray_without_recent_readings() -> None:
    data = series([70])
    result = resolve(data, profile=MALE_30, as_of=data[0].timestamp + timedelta(days=10))
    assert result.status.status is Status.INSUFFICIENT_DATA
    assert result.reason.code is ReasonCode.STALE_READING


def test_without_a_clock_nothing_is_stale() -> None:
    assert resolve(series([*STABLE, 60, 61, 59])).status.status is Status.OK


# --- escalation ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("status", "escalation"),
    [
        (Status.OK, Escalation.SELF_CARE),
        (Status.INSUFFICIENT_DATA, Escalation.SELF_CARE),
        (Status.WATCH, Escalation.CREW_CMO),
        (Status.ACT, Escalation.GROUND_SURGEON),
    ],
)
def test_escalation_is_a_suggestion_by_status(status: Status, escalation: Escalation) -> None:
    assert escalation_for(status) is escalation


# --- system -------------------------------------------------------------------


def indicator_status(
    indicator: Indicator, status: Status, crew_id: str = "crew-01"
) -> IndicatorStatus:
    return IndicatorStatus(
        crew_id=crew_id,
        indicator=indicator,
        status=status,
        reason="x",
        escalation=escalation_for(status),
        environment=EARTH,
        reference=Reference.PERSONAL,
    )


CARDIO = SYSTEM_INDICATORS[System.CARDIOVASCULAR]


def system_of(*statuses: IndicatorStatus, system: System = System.CARDIOVASCULAR) -> SystemStatus:
    result = resolve_system("crew-01", system, statuses)
    assert result is not None
    return result


def test_the_contract_example_cardiovascular_indicators_are_included() -> None:
    assert {Indicator.RESTING_HR, Indicator.SYSTOLIC_BP, Indicator.DIASTOLIC_BP} <= set(CARDIO)


def test_the_system_is_as_bad_as_its_worst_indicator() -> None:
    hr, sbp, dbp = Indicator.RESTING_HR, Indicator.SYSTOLIC_BP, Indicator.DIASTOLIC_BP
    assert (
        system_of(indicator_status(hr, Status.OK), indicator_status(sbp, Status.WATCH)).status
        is Status.WATCH
    )
    assert (
        system_of(
            indicator_status(hr, Status.WATCH),
            indicator_status(sbp, Status.ACT),
            indicator_status(dbp, Status.OK),
        ).status
        is Status.ACT
    )
    assert system_of(indicator_status(hr, Status.OK)).status is Status.OK


def test_gray_indicators_do_not_hide_a_state() -> None:
    hr, sbp = Indicator.RESTING_HR, Indicator.SYSTOLIC_BP
    mixed = system_of(
        indicator_status(hr, Status.INSUFFICIENT_DATA), indicator_status(sbp, Status.OK)
    )
    assert mixed.status is Status.OK


def test_the_system_is_gray_when_every_indicator_is_gray_or_missing() -> None:
    assert system_of().status is Status.INSUFFICIENT_DATA
    gray = indicator_status(Indicator.RESTING_HR, Status.INSUFFICIENT_DATA)
    assert system_of(gray).status is Status.INSUFFICIENT_DATA


def test_the_system_lists_its_indicators_and_ignores_the_rest() -> None:
    result = system_of(
        indicator_status(Indicator.MOOD, Status.ACT),  # not cardiovascular
        indicator_status(Indicator.RESTING_HR, Status.OK, crew_id="crew-02"),  # someone else
    )
    assert result.status is Status.INSUFFICIENT_DATA
    assert result.indicators == CARDIO
    assert SystemStatus.from_dict(result.to_dict()) == result


def test_systems_without_a_measured_indicator_have_no_status() -> None:
    assert SYSTEM_INDICATORS[System.BONE_MUSCLE] == ()
    assert resolve_system("crew-01", System.BONE_MUSCLE, []) is None


def test_every_indicator_belongs_to_at_most_one_system() -> None:
    seen = [i for indicators in SYSTEM_INDICATORS.values() for i in indicators]
    assert len(seen) == len(set(seen))
    assert set(SYSTEM_INDICATORS) == set(System)
