"""C2: population resting-pulse reference (NHSR nº 41, Tables 2 and 3, adult rows).

The expected values were copied from the PDF page images, not from this module.
"""

import pytest

from crew_self_check.core.contract import Sex, Status
from crew_self_check.core.pulse_reference import (
    PERCENTILES,
    PULSE_TABLE,
    SOURCE_CITATION,
    SOURCE_URL,
    population_status,
    reference_row,
)

# (sex, age_min, age_max, n, mean, [percentiles 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99])
PDF_ROWS = [
    (Sex.MALE, 20, 39, 3445, 71, [47, 50, 52, 55, 61, 69, 76, 84, 89, 95, 101]),
    (Sex.MALE, 40, 59, 2559, 71, [46, 49, 52, 55, 61, 68, 77, 85, 90, 95, 104]),
    (Sex.MALE, 60, 79, 1147, 70, [45, 48, 50, 54, 60, 67, 75, 84, 91, 98, 102]),
    (Sex.FEMALE, 20, 39, 3061, 76, [52, 55, 57, 60, 66, 74, 82, 89, 95, 99, 104]),
    (Sex.FEMALE, 40, 59, 2409, 73, [51, 53, 56, 59, 64, 71, 79, 86, 92, 97, 101]),
    (Sex.FEMALE, 60, 79, 1163, 73, [52, 54, 56, 59, 64, 70, 78, 86, 92, 96, 102]),
]
ROW_IDS = [f"{sex}-{lo}-{hi}" for sex, lo, hi, *_ in PDF_ROWS]


def test_table_has_exactly_the_six_adult_rows() -> None:
    assert len(PULSE_TABLE) == 6


def test_percentile_columns_are_the_ones_in_the_pdf() -> None:
    assert PERCENTILES == (1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99)


@pytest.mark.parametrize(("sex", "lo", "hi", "n", "mean", "values"), PDF_ROWS, ids=ROW_IDS)
def test_row_matches_the_pdf(
    sex: Sex, lo: int, hi: int, n: int, mean: int, values: list[int]
) -> None:
    row = reference_row(lo, sex)
    assert row is not None
    assert (row.sex, row.age_min, row.age_max, row.n, row.mean) == (sex, lo, hi, n, mean)
    assert list(row.percentile_values) == values
    assert reference_row(hi, sex) is row


@pytest.mark.parametrize(("sex", "lo", "hi", "n", "mean", "values"), PDF_ROWS, ids=ROW_IDS)
def test_percentiles_increase(
    sex: Sex, lo: int, hi: int, n: int, mean: int, values: list[int]
) -> None:
    assert values == sorted(values)
    assert len(set(values)) == len(values)


@pytest.mark.parametrize("sex", list(Sex))
@pytest.mark.parametrize("age", [-1, 0, 19, 80, 95])
def test_ages_outside_the_adult_rows_have_no_reference(sex: Sex, age: int) -> None:
    assert reference_row(age, sex) is None
    assert population_status(70, age, sex) is None


@pytest.mark.parametrize("sex", list(Sex))
def test_age_group_edges(sex: Sex) -> None:
    for age, expected_lo in [(20, 20), (39, 20), (40, 40), (59, 40), (60, 60), (79, 60)]:
        row = reference_row(age, sex)
        assert row is not None
        assert row.age_min == expected_lo


@pytest.mark.parametrize(("sex", "lo", "hi", "n", "mean", "values"), PDF_ROWS, ids=ROW_IDS)
def test_color_criterion_at_every_cut(
    sex: Sex, lo: int, hi: int, n: int, mean: int, values: list[int]
) -> None:
    p1, p5, p95, p99 = values[0], values[2], values[8], values[10]
    expected = [
        (p1 - 1, Status.ACT),
        (p1, Status.WATCH),
        (p5 - 1, Status.WATCH),
        (p5, Status.OK),
        (values[5], Status.OK),  # the median
        (p95, Status.OK),
        (p95 + 1, Status.WATCH),
        (p99, Status.WATCH),
        (p99 + 1, Status.ACT),
    ]
    for bpm, status in expected:
        assert population_status(bpm, lo, sex) == status, (bpm, status)


def test_fractional_bpm_between_cuts() -> None:
    # Male 20-39: p5 = 52, p95 = 89.
    assert population_status(51.9, 30, Sex.MALE) == Status.WATCH
    assert population_status(89.4, 30, Sex.MALE) == Status.WATCH


@pytest.mark.parametrize("bad", [0, -5, float("nan"), float("inf")])
def test_non_physiological_input_is_rejected(bad: float) -> None:
    with pytest.raises(ValueError, match="bpm"):
        population_status(bad, 30, Sex.MALE)


def test_the_citation_is_carried_with_the_data() -> None:
    assert "Ostchega" in SOURCE_CITATION
    assert "National Health Statistics Reports" in SOURCE_CITATION
    assert SOURCE_URL == "https://www.cdc.gov/nchs/data/nhsr/nhsr041.pdf"
