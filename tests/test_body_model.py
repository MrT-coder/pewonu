"""The body view model: what to say about a state, how to format a reading, how to draw a trend."""

from datetime import UTC, datetime, timedelta

import pytest

from crew_self_check.astronaut.body_model import (
    chart_series,
    format_reading,
    reference_text,
    status_label_key,
)
from crew_self_check.astronaut.chart_layout import layout_series
from crew_self_check.astronaut.i18n import STRINGS, translate
from crew_self_check.core.contract import (
    Environment,
    Escalation,
    Indicator,
    IndicatorStatus,
    Measurement,
    Reference,
    Source,
    Status,
)
from crew_self_check.core.reasons import Language

START = datetime(2026, 11, 1, 7, 30, tzinfo=UTC)


def make_status(
    reference: Reference, baseline_environment: Environment | None = None
) -> IndicatorStatus:
    return IndicatorStatus(
        crew_id="crew-01",
        indicator=Indicator.RESTING_HR,
        status=Status.WATCH,
        reason="x",
        escalation=Escalation.CREW_CMO,
        environment=Environment.PLANET,
        reference=reference,
        baseline_environment=baseline_environment,
    )


# --- what a state is compared with ------------------------------------------------------------


@pytest.mark.parametrize("language", list(Language))
def test_the_reference_is_always_named(language: Language) -> None:
    personal = reference_text(make_status(Reference.PERSONAL), language)
    transition = reference_text(make_status(Reference.TRANSITION, Environment.SPACECRAFT), language)
    population = reference_text(make_status(Reference.POPULATION), language)
    assert len({personal, transition, population}) == 3
    assert translate("env.spacecraft.short", language) in transition
    assert "poblaci" in population.lower() or "population" in population.lower()


def test_the_transition_text_names_the_previous_space() -> None:
    text = reference_text(make_status(Reference.TRANSITION, Environment.EARTH), Language.ES)
    assert "Tierra" in text
    assert "earth" not in text.lower()


@pytest.mark.parametrize(
    ("status", "key"),
    [
        (Status.OK, "status.ok"),
        (Status.WATCH, "status.watch"),
        (Status.ACT, "status.act"),
        (Status.INSUFFICIENT_DATA, "status.insufficient_data"),
        (None, "status.nothing"),
    ],
)
def test_every_state_has_a_label(status: Status | None, key: str) -> None:
    assert status_label_key(status) == key
    assert key in STRINGS


# --- how a reading is shown --------------------------------------------------------------------


@pytest.mark.parametrize(
    ("indicator", "value", "unit", "language", "expected"),
    [
        (Indicator.RESTING_HR, 68, "bpm", Language.EN, "68 bpm"),
        (Indicator.RESTING_HR, 68, "bpm", Language.ES, "68 lpm"),
        (Indicator.BODY_TEMP, 36.6, "degC", Language.EN, "36.6 °C"),
        (Indicator.SLEEP_HOURS, 6.5, "h", Language.ES, "6.5 h"),
        (Indicator.SYSTOLIC_BP, 118, "mmHg", Language.EN, "118 mmHg"),
        (Indicator.SPO2, 97, "%", Language.EN, "97 %"),
        (Indicator.MOOD, 4, "score", Language.EN, translate("mood.level.4", Language.EN)),
        (Indicator.MOOD, 4, "score", Language.ES, translate("mood.level.4", Language.ES)),
        (Indicator.VESTIBULAR_SYMPTOMS, 6, "score", Language.EN, "6 points"),
        (Indicator.VESTIBULAR_SYMPTOMS, 6, "score", Language.ES, "6 puntos"),
        (Indicator.TANDEM_WALK_OK, 1, "0/1", Language.EN, "yes"),
        (Indicator.TANDEM_WALK_OK, 0, "0/1", Language.ES, "no"),
        (Indicator.TANDEM_WALK_OK, 1, "0/1", Language.ES, "sí"),
    ],
)
def test_a_reading_is_shown_with_a_unit_the_astronaut_understands(
    indicator: Indicator, value: float, unit: str, language: Language, expected: str
) -> None:
    assert format_reading(indicator, value, unit, language) == expected


def test_an_unknown_unit_is_shown_as_it_came() -> None:
    assert format_reading(Indicator.BLOOD_GLUCOSE, 90, "mg/dL", Language.EN) == "90 mg/dL"


# --- which readings go into a trend ------------------------------------------------------------


def reading(
    day: int, value: float, indicator: Indicator = Indicator.RESTING_HR, crew: str = "crew-01"
) -> Measurement:
    return Measurement(
        crew, indicator, value, "bpm", START + timedelta(days=day), Source.MANUAL, Environment.EARTH
    )


def test_a_trend_keeps_only_the_indicator_in_time_order_and_the_latest_ones() -> None:
    data = [reading(d, 60 + d) for d in range(20)]
    data += [reading(3, 99, Indicator.SPO2), reading(4, 98, Indicator.SPO2)]
    series = chart_series(list(reversed(data)), Indicator.RESTING_HR, limit=14)
    assert [m.value for m in series] == [66.0 + i for i in range(14)]
    assert all(m.indicator is Indicator.RESTING_HR for m in series)


def test_a_trend_with_no_readings_is_empty() -> None:
    assert chart_series([], Indicator.RESTING_HR) == []


# --- the geometry of the chart ----------------------------------------------------------------


def test_two_readings_are_the_least_that_can_be_drawn() -> None:
    assert layout_series([], None, None, 400, 100) is None
    assert layout_series([60.0], 55, 65, 400, 100) is None
    assert layout_series([60.0, 61.0], None, None, 400, 100) is not None


def test_the_points_are_spread_left_to_right_and_higher_values_are_higher() -> None:
    layout = layout_series([60.0, 70.0, 65.0], None, None, 400, 100, padding=10)
    assert layout is not None
    xs = [x for x, _ in layout.points]
    assert xs == [10.0, 200.0, 390.0]
    ys = [y for _, y in layout.points]
    assert ys[1] < ys[2] < ys[0]  # 70 is higher (smaller y) than 65, than 60
    assert min(ys) == 10.0
    assert max(ys) == 90.0


def test_the_band_is_a_rectangle_between_its_limits() -> None:
    layout = layout_series([60.0, 64.0, 62.0], 58.0, 66.0, 400, 100, padding=10)
    assert layout is not None
    assert layout.band is not None
    x, y, width, height = layout.band
    assert x == 10.0
    assert width == 380.0
    assert height > 0
    # every reading sits inside the band, so the points are inside its vertical extent
    assert all(y <= py <= y + height for _, py in layout.points)


def test_a_reading_outside_the_band_stretches_the_scale_to_show_both() -> None:
    layout = layout_series([60.0, 80.0], 55.0, 65.0, 400, 100, padding=10)
    assert layout is not None
    assert layout.band is not None
    _, band_y, _, band_height = layout.band
    top_point = min(y for _, y in layout.points)
    assert top_point < band_y  # the 80 is drawn above the band
    assert band_y >= 10.0 and band_y + band_height <= 90.0


def test_a_flat_series_does_not_divide_by_zero() -> None:
    layout = layout_series([60.0, 60.0, 60.0], None, None, 400, 100)
    assert layout is not None
    ys = {y for _, y in layout.points}
    assert len(ys) == 1


def test_a_degenerate_band_still_has_a_visible_height() -> None:
    layout = layout_series([60.0, 60.0], 60.0, 60.0, 400, 100)
    assert layout is not None
    assert layout.band is not None
    assert layout.band[3] > 0
