"""Population reference for resting pulse by age and sex (D-014).

Source: Ostchega Y, Porter KS, Hughes J, Dillon CF, Nwankwo T. Resting pulse rate reference data
for children, adolescents, and adults: United States, 1999-2008. National Health Statistics
Reports no. 41, 2011, Tables 2 (males) and 3 (females). Values were copied from the page images of
the PDF, adult rows only. The data excludes people with a medical condition or medication that
affects the resting pulse rate.

This is a statistical reference of the general US population, **not** a clinical threshold and not
astronaut data. It is only used while the personal baseline is not mature, and it must always be
shown with ``reference: population`` (docs/pulso-referencia.md).

Not covered, on purpose: under 20 (not the crew) and 80 and over (the PDF leaves cells blank).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from crew_self_check.core.contract import Sex, Status

SOURCE_CITATION = (
    "Ostchega Y, et al. Resting pulse rate reference data for children, adolescents, and adults: "
    "United States, 1999-2008. National Health Statistics Reports no. 41. Hyattsville, MD: "
    "National Center for Health Statistics; 2011."
)
SOURCE_URL = "https://www.cdc.gov/nchs/data/nhsr/nhsr041.pdf"

# Columns of the PDF tables, in order.
PERCENTILES: tuple[float, ...] = (1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99)
_P1, _P5, _P95, _P99 = 0, 2, 8, 10  # indexes into PERCENTILES used by the color criterion


@dataclass(frozen=True, slots=True)
class PulseRow:
    sex: Sex
    age_min: int
    age_max: int
    n: int
    mean: int
    percentile_values: tuple[int, ...]  # bpm, aligned with PERCENTILES


PULSE_TABLE: tuple[PulseRow, ...] = (
    # Table 2, males
    PulseRow(Sex.MALE, 20, 39, 3445, 71, (47, 50, 52, 55, 61, 69, 76, 84, 89, 95, 101)),
    PulseRow(Sex.MALE, 40, 59, 2559, 71, (46, 49, 52, 55, 61, 68, 77, 85, 90, 95, 104)),
    PulseRow(Sex.MALE, 60, 79, 1147, 70, (45, 48, 50, 54, 60, 67, 75, 84, 91, 98, 102)),
    # Table 3, females
    PulseRow(Sex.FEMALE, 20, 39, 3061, 76, (52, 55, 57, 60, 66, 74, 82, 89, 95, 99, 104)),
    PulseRow(Sex.FEMALE, 40, 59, 2409, 73, (51, 53, 56, 59, 64, 71, 79, 86, 92, 97, 101)),
    PulseRow(Sex.FEMALE, 60, 79, 1163, 73, (52, 54, 56, 59, 64, 70, 78, 86, 92, 96, 102)),
)


def reference_row(age: int, sex: Sex) -> PulseRow | None:
    """The row for this age and sex, or ``None`` when the table does not cover them."""
    for row in PULSE_TABLE:
        if row.sex is sex and row.age_min <= age <= row.age_max:
            return row
    return None


def population_status(bpm: float, age: int, sex: Sex) -> Status | None:
    """Color of a resting pulse against the population table, or ``None`` without a row.

    Criterion (proposal, D-014 asks to define and document it):

    - ``ok``: from the 5th to the 95th percentile, both included (the central 90 %).
    - ``watch``: from the 1st up to below the 5th, or above the 95th up to the 99th.
    - ``act``: below the 1st or above the 99th percentile.

    It says "unusual compared with healthy adults of the same age and sex", never "disease".
    """
    if not math.isfinite(bpm) or bpm <= 0:
        raise ValueError(f"bpm must be a positive finite number, got {bpm!r}")
    row = reference_row(age, sex)
    if row is None:
        return None
    values = row.percentile_values
    if bpm < values[_P1] or bpm > values[_P99]:
        return Status.ACT
    if bpm < values[_P5] or bpm > values[_P95]:
        return Status.WATCH
    return Status.OK
