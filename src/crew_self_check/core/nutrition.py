"""Nutrition estimate and meal log (T10, D-030). Pure Python, educational and neutral.

The energy estimate is Mifflin-St Jeor times a light activity factor, plus the energy of the day's
exercise. It is shown next to the 1,900-3,200 kcal range the Canadian Space Agency describes for
station dieticians. Protein uses the Dietary Reference Intake of 0.8 g/kg (NASA's nutrition
standard follows the NIH DRIs). The activity factor and the food catalog are conventions
([SUPOSICION], ``docs/decisiones.md`` D-030): the catalog is a small, simulated, illustrative list
by ISS food category, not the real menu. There is no state, no alert and no target to "fail": the
ground dietitians set the real plan. No supplements, no doses, no medical advice.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from crew_self_check.core.contract import CrewProfile, Sex

ACTIVITY_FACTOR = 1.3  # light activity outside the scheduled exercise [SUPOSICION]
PROTEIN_G_PER_KG = 0.8  # DRI RDA for adults
CONTEXT_KCAL = (1900, 3200)  # CSA: dietitians' range by weight, sex and needs


@dataclass(frozen=True, slots=True)
class NutritionPlan:
    energy_kcal: int
    protein_g: int
    context_low_kcal: int
    context_high_kcal: int


@dataclass(frozen=True, slots=True)
class Food:
    id: str
    category: str  # rehydratable, thermostabilized, intermediate, irradiated, natural, fresh
    kcal: int
    protein_g: float
    carbs_g: float
    fat_g: float  # per serving, approximate and simulated


@dataclass(frozen=True, slots=True)
class MealEntry:
    food_id: str
    servings: float


@dataclass(frozen=True, slots=True)
class Intake:
    energy_kcal: int
    protein_g: int
    carbs_g: int
    fat_g: int
    shares: tuple[float, float, float] | None  # % of energy: protein, carbs, fat


FOODS: tuple[Food, ...] = (
    Food("scrambled_eggs", "rehydratable", 190, 12.0, 3.0, 14.0),
    Food("oatmeal", "rehydratable", 160, 5.0, 28.0, 3.0),
    Food("macaroni_cheese", "rehydratable", 280, 11.0, 35.0, 11.0),
    Food("beef_stew", "thermostabilized", 230, 18.0, 12.0, 12.0),
    Food("chicken_rice", "thermostabilized", 260, 17.0, 32.0, 6.0),
    Food("tuna_pouch", "thermostabilized", 120, 26.0, 0.0, 1.5),
    Food("lentil_soup", "thermostabilized", 210, 12.0, 34.0, 3.0),
    Food("fruit_cup", "thermostabilized", 90, 1.0, 22.0, 0.0),
    Food("granola_bar", "intermediate", 190, 4.0, 29.0, 7.0),
    Food("dried_apricots", "intermediate", 100, 1.0, 25.0, 0.0),
    Food("smoked_turkey", "irradiated", 140, 24.0, 2.0, 4.0),
    Food("beef_jerky", "intermediate", 116, 9.4, 3.1, 7.3),
    Food("almonds", "natural", 170, 6.0, 6.0, 15.0),
    Food("peanut_butter", "natural", 190, 7.0, 7.0, 16.0),
    Food("tortilla", "natural", 140, 4.0, 24.0, 3.0),
    Food("cookies", "natural", 150, 2.0, 21.0, 7.0),
    Food("fresh_apple", "fresh", 95, 0.5, 25.0, 0.3),
    Food("fresh_greens", "fresh", 25, 2.0, 4.0, 0.3),
)
_BY_ID = {f.id: f for f in FOODS}


def food_by_id(food_id: str) -> Food:
    return _BY_ID[food_id]


def plan_nutrition(profile: CrewProfile, exercise_kcal: int) -> NutritionPlan | None:
    if profile.weight_kg is None or profile.height_cm is None:
        return None
    bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age
    bmr += 5 if profile.sex is Sex.MALE else -161
    return NutritionPlan(
        energy_kcal=round(bmr * ACTIVITY_FACTOR) + exercise_kcal,
        protein_g=round(PROTEIN_G_PER_KG * profile.weight_kg),
        context_low_kcal=CONTEXT_KCAL[0],
        context_high_kcal=CONTEXT_KCAL[1],
    )


def summarize_intake(entries: Iterable[MealEntry]) -> Intake:
    kcal = protein = carbs = fat = 0.0
    for entry in entries:
        if entry.servings <= 0:
            raise ValueError("servings must be greater than 0")
        food = food_by_id(entry.food_id)
        kcal += food.kcal * entry.servings
        protein += food.protein_g * entry.servings
        carbs += food.carbs_g * entry.servings
        fat += food.fat_g * entry.servings
    macro_kcal = 4 * protein + 4 * carbs + 9 * fat
    shares = (
        None
        if macro_kcal <= 0
        else (
            100 * 4 * protein / macro_kcal,
            100 * 4 * carbs / macro_kcal,
            100 * 9 * fat / macro_kcal,
        )
    )
    return Intake(round(kcal), round(protein), round(carbs), round(fat), shares)
