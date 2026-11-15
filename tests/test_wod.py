"""T9: the workout of the day on the three machines of the ISS (T2 treadmill, CEVIS bike, ARED)."""

from __future__ import annotations

import pytest

from crew_self_check.core.contract import CrewProfile, Sex
from crew_self_check.core.wod import (
    Adjustment,
    Effort,
    Machine,
    WodContext,
    plan_wod,
    rpe_range,
)

PROFILE = CrewProfile("crew-09", 40, Sex.FEMALE, "simulated", 62.0, 168.0, 1.04)


def ctx(day: int = 0, **flags: object) -> WodContext:
    return WodContext(day_in_week=day % 7, days_in_space=30, **flags)  # type: ignore[arg-type]


def test_only_the_three_machines_of_the_station_are_used() -> None:
    used = {block.machine for d in range(7) for block in plan_wod(PROFILE, ctx(d)).blocks}
    assert used == {Machine.TREADMILL, Machine.CYCLE, Machine.RESISTIVE}


def test_the_week_rotates_and_has_one_light_day() -> None:
    kinds = [plan_wod(PROFILE, ctx(d)).kind for d in range(7)]
    assert len(set(kinds)) == 7
    light = [d for d in range(7) if plan_wod(PROFILE, ctx(d)).minutes <= 30]
    assert light == [6]


def test_every_working_day_has_resistive_work_to_load_the_bones() -> None:
    for day in range(6):
        machines = {b.machine for b in plan_wod(PROFILE, ctx(day)).blocks}
        assert Machine.RESISTIVE in machines, day


def test_the_plan_stays_inside_the_time_nasa_schedules() -> None:
    for day in range(7):
        assert plan_wod(PROFILE, ctx(day)).minutes <= 150  # about 2.5 hours a day


def test_the_same_inputs_give_the_same_plan() -> None:
    assert plan_wod(PROFILE, ctx(2)) == plan_wod(PROFILE, ctx(2))


def test_effort_is_perceived_exertion_not_a_heart_rate_or_a_load() -> None:
    assert rpe_range(Effort.EASY) == (3, 4)
    assert rpe_range(Effort.MODERATE) == (5, 6)
    assert rpe_range(Effort.HARD) == (7, 8)


def test_a_poor_night_makes_the_day_lighter_and_never_hard() -> None:
    normal = plan_wod(PROFILE, ctx(1))
    lighter = plan_wod(PROFILE, ctx(1, sleep_flagged=True))
    assert Adjustment.LIGHTER_SLEEP in lighter.adjustments
    assert lighter.minutes < normal.minutes
    assert all(block.effort is not Effort.HARD for block in lighter.blocks)


def test_balance_trouble_swaps_the_treadmill_for_the_bike() -> None:
    normal = plan_wod(PROFILE, ctx(1))
    assert any(b.machine is Machine.TREADMILL for b in normal.blocks)
    safe = plan_wod(PROFILE, ctx(1, balance_flagged=True))
    assert Adjustment.NO_TREADMILL in safe.adjustments
    assert all(b.machine is not Machine.TREADMILL for b in safe.blocks)
    assert safe.minutes == normal.minutes


def test_a_strong_balance_flag_also_says_to_tell_the_medical_officer_and_stays_moderate() -> None:
    plan = plan_wod(PROFILE, ctx(1, balance_flagged=True, balance_severe=True))
    assert Adjustment.TELL_CMO in plan.adjustments
    assert all(block.effort is not Effort.HARD for block in plan.blocks)


def test_a_low_mood_adds_a_note_and_changes_nothing_else() -> None:
    normal = plan_wod(PROFILE, ctx(2))
    mood = plan_wod(PROFILE, ctx(2, mood_flagged=True))
    assert Adjustment.MOOD_NOTE in mood.adjustments
    assert mood.blocks == normal.blocks


def test_a_long_stay_in_space_adds_an_extra_loading_set() -> None:
    short = plan_wod(PROFILE, WodContext(day_in_week=0, days_in_space=3))
    long_stay = plan_wod(PROFILE, WodContext(day_in_week=0, days_in_space=30))
    assert Adjustment.EXTRA_LOADING not in short.adjustments
    assert Adjustment.EXTRA_LOADING in long_stay.adjustments


def test_the_energy_of_the_session_grows_with_the_body_weight() -> None:
    light = plan_wod(CrewProfile("a", 40, Sex.MALE, "s", 60.0, 170.0, 1.1), ctx(1))
    heavy = plan_wod(CrewProfile("b", 40, Sex.MALE, "s", 90.0, 170.0, 1.1), ctx(1))
    assert light.energy_kcal is not None and heavy.energy_kcal is not None
    assert heavy.energy_kcal > light.energy_kcal > 0


def test_without_a_weight_there_is_no_energy_estimate() -> None:
    plan = plan_wod(CrewProfile("a", 40, Sex.MALE, "s"), ctx(1))
    assert plan.energy_kcal is None


def test_the_heart_rate_reference_comes_from_the_age_and_is_only_a_reference() -> None:
    plan = plan_wod(PROFILE, ctx(1))
    assert plan.hr_reference is not None
    assert plan.hr_reference.max_bpm == 180  # 220 minus 40: a rough rule
    assert plan.hr_reference.moderate_low < plan.hr_reference.moderate_high < 180
    older = plan_wod(CrewProfile("o", 60, Sex.MALE, "s", 80.0, 175.0, 1.0), ctx(1))
    assert older.hr_reference is not None and older.hr_reference.max_bpm == 160


def test_the_bone_note_shows_the_unmitigated_range_of_nasa_for_the_days_in_space() -> None:
    plan = plan_wod(PROFILE, WodContext(day_in_week=0, days_in_space=60))
    assert plan.bone is not None
    assert plan.bone.baseline == 1.04
    assert plan.bone.months == pytest.approx(2.0)
    assert plan.bone.expected_low_pct == pytest.approx(2.0)  # 1 % a month
    assert plan.bone.expected_high_pct == pytest.approx(4.0)  # 2 % a month


def test_on_earth_there_is_nothing_to_illustrate_yet() -> None:
    plan = plan_wod(PROFILE, WodContext(day_in_week=0, days_in_space=0))
    assert plan.bone is not None
    assert plan.bone.expected_high_pct == 0


def test_without_bone_data_there_is_no_bone_note() -> None:
    plan = plan_wod(CrewProfile("a", 40, Sex.MALE, "s", 70.0, 170.0), ctx(0))
    assert plan.bone is None


def test_the_plan_gives_no_loads_doses_or_diagnosis_in_its_keys() -> None:
    plan = plan_wod(PROFILE, ctx(0, sleep_flagged=True, balance_flagged=True, mood_flagged=True))
    keys = [plan.kind, *(b.focus for b in plan.blocks), *(a.value for a in plan.adjustments)]
    for key in keys:
        assert "kg" not in key and "mg" not in key and "diagnos" not in key
