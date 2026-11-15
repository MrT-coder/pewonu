"""T10: the nutrition estimate and the meal log (educational, neutral, simulated food catalog)."""

from __future__ import annotations

import pytest

from crew_self_check.core.contract import CrewProfile, Sex
from crew_self_check.core.nutrition import (
    FOODS,
    MealEntry,
    food_by_id,
    plan_nutrition,
    summarize_intake,
)

FEMALE = CrewProfile("crew-09", 38, Sex.FEMALE, "simulated", 62.0, 168.0, 1.04)
MALE = CrewProfile("crew-08", 45, Sex.MALE, "simulated", 84.0, 179.0, 1.16)


def test_the_energy_estimate_follows_mifflin_st_jeor_with_a_light_activity_factor() -> None:
    plan = plan_nutrition(FEMALE, exercise_kcal=0)
    assert plan is not None
    bmr = 10 * 62.0 + 6.25 * 168.0 - 5 * 38 - 161
    assert plan.energy_kcal == round(bmr * 1.3)


def test_the_exercise_of_the_day_adds_its_energy() -> None:
    rest = plan_nutrition(MALE, exercise_kcal=0)
    trained = plan_nutrition(MALE, exercise_kcal=600)
    assert rest is not None and trained is not None
    assert trained.energy_kcal == rest.energy_kcal + 600


def test_a_man_and_a_woman_of_the_same_build_differ_by_the_formula_constant() -> None:
    f = plan_nutrition(CrewProfile("f", 40, Sex.FEMALE, "s", 70.0, 170.0), 0)
    m = plan_nutrition(CrewProfile("m", 40, Sex.MALE, "s", 70.0, 170.0), 0)
    assert f is not None and m is not None
    assert m.energy_kcal > f.energy_kcal


def test_without_weight_or_height_there_is_no_estimate() -> None:
    assert plan_nutrition(CrewProfile("a", 40, Sex.MALE, "s"), 0) is None
    assert plan_nutrition(CrewProfile("a", 40, Sex.MALE, "s", 70.0), 0) is None


def test_protein_reference_is_the_dietary_reference_intake_per_kilogram() -> None:
    plan = plan_nutrition(MALE, 0)
    assert plan is not None
    assert plan.protein_g == round(0.8 * 84.0)


def test_the_context_range_of_the_space_agencies_is_shown_with_the_estimate() -> None:
    plan = plan_nutrition(MALE, 0)
    assert plan is not None
    assert (plan.context_low_kcal, plan.context_high_kcal) == (1900, 3200)


def test_the_catalog_is_small_labelled_and_consistent() -> None:
    assert 12 <= len(FOODS) <= 30
    assert len({f.id for f in FOODS}) == len(FOODS)
    assert {f.category for f in FOODS} >= {"rehydratable", "thermostabilized", "natural", "fresh"}
    for food in FOODS:
        assert food.kcal > 0
        # The calories must roughly match the macronutrients (4/4/9 kcal per gram).
        assert food.kcal == pytest.approx(
            4 * food.protein_g + 4 * food.carbs_g + 9 * food.fat_g, rel=0.2
        )


def test_the_intake_adds_up_the_meals_by_servings() -> None:
    first, second = FOODS[0], FOODS[1]
    summary = summarize_intake([MealEntry(first.id, 2.0), MealEntry(second.id, 1.0)])
    assert summary.energy_kcal == round(2 * first.kcal + second.kcal)
    assert summary.protein_g == round(2 * first.protein_g + second.protein_g)


def test_an_empty_day_has_no_shares() -> None:
    summary = summarize_intake([])
    assert summary.energy_kcal == 0
    assert summary.shares is None


def test_the_shares_of_energy_add_up_to_one_hundred() -> None:
    summary = summarize_intake([MealEntry(f.id, 1.0) for f in FOODS[:4]])
    assert summary.shares is not None
    assert sum(summary.shares) == pytest.approx(100, abs=1.0)


def test_an_unknown_food_is_refused() -> None:
    with pytest.raises(KeyError):
        food_by_id("nope")
    with pytest.raises(KeyError):
        summarize_intake([MealEntry("nope", 1.0)])


def test_the_servings_must_be_positive() -> None:
    with pytest.raises(ValueError):
        summarize_intake([MealEntry(FOODS[0].id, 0)])


def test_no_supplement_or_medication_in_the_catalog() -> None:
    for food in FOODS:
        assert "supplement" not in food.id and "vitamin" not in food.id and "pill" not in food.id
