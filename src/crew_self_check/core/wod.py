"""The workout of the day (WOD) on the three machines of the station (T9, D-030). Pure Python.

The ISS crew trains on three devices: the **T2** treadmill, the **CEVIS** cycle ergometer and the
**ARED** resistive device (NASA, "Astronaut exercise"). NASA schedules about two and a half hours of
exercise a day. This module turns the person's own data into one educational plan: age (a rough
heart-rate reference), weight (the energy of the session) and the preflight bone density (why the
loading matters), adjusted by how the person is today (sleep, balance, mood).

What it does **not** do: it gives no load, no dose and no diagnosis, and no clinical threshold.
Effort is perceived exertion (RPE); the ground exercise specialists set the real prescription.
The weekly rotation, the effort scales and the energy factors are conventions ([SUPOSICION],
``docs/decisiones.md`` D-030), inspired by the public description of ISS sessions, not NASA's own
schedule. Deterministic: there is no model and no random number here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from crew_self_check.core.contract import CrewProfile

BONE_LOSS_LOW_PCT_PER_MONTH = 1.0  # NASA HRP: unmitigated loss of 1-2 % a month
BONE_LOSS_HIGH_PCT_PER_MONTH = 2.0
_DAYS_PER_MONTH = 30.0
_EXTRA_LOADING_AFTER_DAYS = 14
_MODERATE_BAND = (0.50, 0.70)  # share of the estimated maximum heart rate (a common rule of thumb)


class Machine(StrEnum):
    TREADMILL = "treadmill"  # T2
    CYCLE = "cycle"  # CEVIS
    RESISTIVE = "resistive"  # ARED


class Effort(StrEnum):
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"


_RPE = {Effort.EASY: (3, 4), Effort.MODERATE: (5, 6), Effort.HARD: (7, 8)}

# Approximate metabolic equivalents (MET) by machine and effort, in the spirit of the Compendium
# of Physical Activities. [SUPOSICION] rounded conventions, not measurements.
_MET = {
    Machine.TREADMILL: {Effort.EASY: 4.5, Effort.MODERATE: 7.0, Effort.HARD: 9.0},
    Machine.CYCLE: {Effort.EASY: 4.0, Effort.MODERATE: 6.0, Effort.HARD: 8.0},
    Machine.RESISTIVE: {Effort.EASY: 3.5, Effort.MODERATE: 5.0, Effort.HARD: 6.0},
}


class Adjustment(StrEnum):
    LIGHTER_SLEEP = "lighter_sleep"  # a poor night: shorter and never hard
    NO_TREADMILL = "no_treadmill"  # balance trouble: the bike instead of the treadmill
    TELL_CMO = "tell_cmo"  # a strong balance flag: tell the crew medical officer first
    MOOD_NOTE = "mood_note"  # low mood: the plan is the same, with a note
    EXTRA_LOADING = "extra_loading"  # a long stay in space: one more loading set


@dataclass(frozen=True, slots=True)
class Block:
    machine: Machine
    effort: Effort
    minutes: int
    focus: str  # a text key suffix: intervals, steady, legs, upper, full, easy


@dataclass(frozen=True, slots=True)
class WodContext:
    """How the person is today. The flags come from the engine's own states."""

    day_in_week: int  # 0 to 6, from the mission day
    days_in_space: int = 0
    sleep_flagged: bool = False
    balance_flagged: bool = False  # orthostatic or balance indicators outside the range
    balance_severe: bool = False
    mood_flagged: bool = False


@dataclass(frozen=True, slots=True)
class HrReference:
    max_bpm: int  # 220 minus the age: a rough rule, not a measurement
    moderate_low: int
    moderate_high: int


@dataclass(frozen=True, slots=True)
class BoneNote:
    baseline: float  # preflight bone mineral density, g/cm2
    months: float  # time in space
    expected_low_pct: float  # NASA's unmitigated range, as an illustration
    expected_high_pct: float


@dataclass(frozen=True, slots=True)
class Wod:
    kind: str  # a text key suffix naming the day
    blocks: tuple[Block, ...]
    adjustments: tuple[Adjustment, ...]
    minutes: int
    energy_kcal: int | None
    hr_reference: HrReference | None
    bone: BoneNote | None


T, C, R = Machine.TREADMILL, Machine.CYCLE, Machine.RESISTIVE
E, M, H = Effort.EASY, Effort.MODERATE, Effort.HARD

# One educational week, six working days and one light day ([SUPOSICION], see the module note).
_WEEK: tuple[tuple[str, tuple[Block, ...]], ...] = (
    ("legs_and_easy_bike", (Block(R, M, 50, "legs"), Block(C, E, 30, "easy"))),
    ("run_intervals_and_upper", (Block(T, H, 30, "intervals"), Block(R, M, 45, "upper"))),
    ("steady_bike_and_full", (Block(C, M, 40, "steady"), Block(R, M, 50, "full"))),
    ("steady_run_and_legs", (Block(T, M, 40, "steady"), Block(R, M, 50, "legs"))),
    ("bike_intervals_and_upper", (Block(C, H, 30, "intervals"), Block(R, M, 45, "upper"))),
    (
        "circuit",
        (Block(T, M, 20, "steady"), Block(C, M, 20, "steady"), Block(R, E, 30, "full")),
    ),
    ("active_recovery", (Block(T, E, 20, "easy"),)),
)


def rpe_range(effort: Effort) -> tuple[int, int]:
    return _RPE[effort]


def _round5(minutes: float) -> int:
    return max(5, round(minutes / 5) * 5)


def _adjusted(
    blocks: tuple[Block, ...], context: WodContext
) -> tuple[tuple[Block, ...], tuple[Adjustment, ...]]:
    notes: list[Adjustment] = []
    out = list(blocks)
    if context.sleep_flagged:
        notes.append(Adjustment.LIGHTER_SLEEP)
        out = [
            Block(b.machine, M if b.effort is H else b.effort, _round5(b.minutes * 0.7), b.focus)
            for b in out
        ]
    if context.balance_flagged:
        notes.append(Adjustment.NO_TREADMILL)
        out = [Block(C, b.effort, b.minutes, b.focus) if b.machine is T else b for b in out]
        if context.balance_severe:
            notes.append(Adjustment.TELL_CMO)
            out = [
                Block(b.machine, M if b.effort is H else b.effort, b.minutes, b.focus) for b in out
            ]
    if context.mood_flagged:
        notes.append(Adjustment.MOOD_NOTE)
    if context.days_in_space >= _EXTRA_LOADING_AFTER_DAYS:
        notes.append(Adjustment.EXTRA_LOADING)
    return tuple(out), tuple(notes)


def _energy(blocks: tuple[Block, ...], weight_kg: float | None) -> int | None:
    if weight_kg is None:
        return None
    hours = {b: b.minutes / 60 for b in blocks}
    return round(sum(_MET[b.machine][b.effort] * weight_kg * hours[b] for b in blocks))


def _hr_reference(age: int) -> HrReference:
    maximum = 220 - age
    low, high = _MODERATE_BAND
    return HrReference(maximum, round(maximum * low), round(maximum * high))


def _bone(profile: CrewProfile, days_in_space: int) -> BoneNote | None:
    if profile.bone_mineral_density is None:
        return None
    months = days_in_space / _DAYS_PER_MONTH
    return BoneNote(
        baseline=profile.bone_mineral_density,
        months=months,
        expected_low_pct=BONE_LOSS_LOW_PCT_PER_MONTH * months,
        expected_high_pct=BONE_LOSS_HIGH_PCT_PER_MONTH * months,
    )


def plan_wod(profile: CrewProfile, context: WodContext) -> Wod:
    kind, blocks = _WEEK[context.day_in_week % len(_WEEK)]
    blocks, adjustments = _adjusted(blocks, context)
    return Wod(
        kind=kind,
        blocks=blocks,
        adjustments=adjustments,
        minutes=sum(b.minutes for b in blocks),
        energy_kcal=_energy(blocks, profile.weight_kg),
        hr_reference=_hr_reference(profile.age),
        bone=_bone(profile, context.days_in_space),
    )
