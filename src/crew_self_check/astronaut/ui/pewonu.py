"""PeWoNu: Peace, WOD and Nutrition (D-030). The pillars panel and the WOD and nutrition modals.

The plans come from ``core.wod`` and ``core.nutrition``; this view only lays them out. Everything
is educational and neutral: there is no state color for the food, and no load or dose anywhere.
"""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, card
from crew_self_check.core.nutrition import FOODS, summarize_intake
from crew_self_check.core.nutrition import food_by_id as food_of
from crew_self_check.core.wod import Wod, rpe_range

_MACHINE_ICONS = {
    "treadmill": ft.Icons.DIRECTIONS_RUN,
    "cycle": ft.Icons.PEDAL_BIKE,
    "resistive": ft.Icons.FITNESS_CENTER,
}


def _pillar(
    state: AppState, icon: ft.IconData, title_key: str, sub_key: str, on_click: object
) -> ft.Control:
    language = state.language
    return ft.Container(
        on_click=on_click,  # type: ignore[arg-type]
        ink=True,
        padding=10,
        border_radius=12,
        content=ft.Row(
            spacing=10,
            controls=[
                ft.Icon(icon, color=theme.ACCENT, size=26),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Text(
                            translate(title_key, language),
                            size=15,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT,
                        ),
                        ft.Text(translate(sub_key, language), size=11, color=theme.MUTED),
                    ],
                ),
            ],
        ),
    )


def build_pillars(state: AppState, actions: Actions) -> ft.Control:
    """The three pillars of the system, one tap each."""
    language = state.language

    def go(opener: object) -> object:
        def handler(_: object) -> None:
            opener()  # type: ignore[operator]
            actions.rerender()

        return handler

    return card(
        ft.Column(
            spacing=2,
            controls=[
                ft.Text(
                    translate("pewonu.title", language),
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT,
                ),
                ft.Text(translate("pewonu.tagline", language), size=11, color=theme.MUTED),
                _pillar(
                    state,
                    ft.Icons.SELF_IMPROVEMENT,
                    "pewonu.peace",
                    "pewonu.peace.sub",
                    go(state.open_mood),
                ),
                _pillar(
                    state,
                    ft.Icons.FITNESS_CENTER,
                    "pewonu.wod",
                    "pewonu.wod.sub",
                    go(state.open_wod),
                ),
                _pillar(
                    state,
                    ft.Icons.RESTAURANT,
                    "pewonu.nutrition",
                    "pewonu.nutrition.sub",
                    go(state.open_nutrition),
                ),
            ],
        ),
        padding=12,
    )


def _note(text: str) -> ft.Control:
    return ft.Text(text, size=12, color=theme.MUTED)


def _block_row(state: AppState, wod: Wod, index: int) -> ft.Control:
    language = state.language
    block = wod.blocks[index]
    low, high = rpe_range(block.effort)
    return card(
        ft.Row(
            spacing=12,
            controls=[
                ft.Icon(_MACHINE_ICONS[block.machine.value], color=theme.ACCENT, size=28),
                ft.Column(
                    expand=True,
                    spacing=2,
                    controls=[
                        ft.Text(
                            translate(f"wod.machine.{block.machine.value}", language),
                            size=15,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT,
                        ),
                        ft.Text(
                            f"{translate(f'wod.focus.{block.focus}', language)} · "
                            f"{translate(f'wod.effort.{block.effort.value}', language)}",
                            size=13,
                            color=theme.TEXT,
                        ),
                        _note(translate("wod.rpe", language, low=low, high=high)),
                    ],
                ),
                ft.Text(
                    translate("wod.minutes", language, minutes=block.minutes),
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT,
                ),
            ],
        ),
        padding=12,
    )


def build_wod(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    wod = state.wod_plan()
    if wod is None:
        return _note(translate("wod.no_profile", language))

    def toggle(_: object) -> None:
        state.toggle_wod_done()
        actions.rerender()

    done = state.wod_done()
    controls: list[ft.Control] = [
        ft.Text(
            translate(f"wod.kind.{wod.kind}", language),
            size=18,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
        ),
        _note(translate("wod.total", language, minutes=wod.minutes)),
        *[_block_row(state, wod, i) for i in range(len(wod.blocks))],
    ]
    controls += [_note(f"•  {translate(f'wod.adj.{a.value}', language)}") for a in wod.adjustments]
    if wod.hr_reference is not None:
        hr = wod.hr_reference
        controls.append(
            _note(
                translate(
                    "wod.hr",
                    language,
                    low=hr.moderate_low,
                    high=hr.moderate_high,
                    maximum=hr.max_bpm,
                )
            )
        )
    if wod.energy_kcal is not None:
        controls.append(_note(translate("wod.energy", language, kcal=wod.energy_kcal)))
    if wod.bone is not None:
        bone = wod.bone
        controls.append(
            _note(
                translate(
                    "wod.bone",
                    language,
                    baseline=f"{bone.baseline:.2f}",
                    months=f"{bone.months:.1f}",
                    low=f"{bone.expected_low_pct:.1f}",
                    high=f"{bone.expected_high_pct:.1f}",
                )
            )
        )
    controls += [
        _note(translate("wod.disclaimer", language)),
        ft.FilledButton(
            content=translate("wod.done" if done else "wod.mark_done", language),
            icon=ft.Icons.CHECK_CIRCLE if done else ft.Icons.CHECK_CIRCLE_OUTLINE,
            height=46,
            on_click=toggle,
        ),
    ]
    return ft.Column(
        spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=controls
    )


def build_nutrition(state: AppState, actions: Actions) -> ft.Control:
    language = state.language
    plan = state.nutrition_plan()
    entries = state.meals()
    intake = summarize_intake(entries)
    controls: list[ft.Control] = []
    if plan is None:
        controls.append(_note(translate("nutrition.no_profile", language)))
    else:
        controls += [
            _note(translate("nutrition.energy", language, kcal=plan.energy_kcal)),
            _note(translate("nutrition.protein", language, grams=plan.protein_g)),
            ft.ProgressBar(
                value=min(1.0, intake.energy_kcal / plan.energy_kcal),
                color=theme.ACCENT,
                bgcolor=theme.CARD_BORDER,
            ),
            _note(
                translate(
                    "nutrition.progress",
                    language,
                    kcal=intake.energy_kcal,
                    target=plan.energy_kcal,
                )
            ),
        ]
    controls.append(
        ft.Text(
            translate("nutrition.logged", language),
            size=15,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
        )
    )
    if not entries:
        controls.append(_note(translate("nutrition.empty", language)))
    for index, entry in enumerate(entries):
        name = translate(f"food.{entry.food_id}", language)

        def remove(_: object, i: int = index) -> None:
            state.remove_meal(i)
            actions.rerender()

        controls.append(
            ft.Row(
                controls=[
                    ft.Text(name, expand=True, size=13, color=theme.TEXT),
                    ft.Text(f"{food_of(entry.food_id).kcal} kcal", size=12, color=theme.MUTED),
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                        tooltip=translate("nutrition.remove", language, food=name),
                        on_click=remove,
                    ),
                ]
            )
        )
    if entries:
        controls.append(
            _note(
                translate(
                    "nutrition.totals",
                    language,
                    kcal=intake.energy_kcal,
                    protein=intake.protein_g,
                    carbs=intake.carbs_g,
                    fat=intake.fat_g,
                )
            )
        )
    if intake.shares is not None:
        protein, carbs, fat = (round(x) for x in intake.shares)
        controls.append(
            _note(translate("nutrition.shares", language, protein=protein, carbs=carbs, fat=fat))
        )
    controls.append(
        ft.Text(
            translate("nutrition.add", language),
            size=15,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
        )
    )

    def adder(food_id: str) -> object:
        def handler(_: object) -> None:
            state.add_meal(food_id)
            actions.rerender()

        return handler

    controls.append(
        ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
            controls=[
                ft.OutlinedButton(
                    content=translate(f"food.{food.id}", language),
                    tooltip=translate(f"food.cat.{food.category}", language),
                    on_click=adder(food.id),  # type: ignore[arg-type]
                )
                for food in FOODS
            ],
        )
    )
    controls.append(_note(translate("nutrition.disclaimer", language)))
    return ft.Column(
        spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=controls
    )
