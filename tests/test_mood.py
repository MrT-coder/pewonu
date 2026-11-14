"""Part 2b: the mood survey (five faces, D-015). Pure logic."""

from datetime import UTC, datetime

import pytest

from crew_self_check.astronaut.mood import MOOD_LEVELS, mood_measurement
from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source

NOW = datetime(2026, 11, 14, 21, 45, tzinfo=UTC)


def test_the_scale_has_five_levels() -> None:
    assert MOOD_LEVELS == (1, 2, 3, 4, 5)


@pytest.mark.parametrize("level", MOOD_LEVELS)
def test_a_face_becomes_a_manual_survey_measurement_of_mood(level: int) -> None:
    measurement = mood_measurement("crew-01", level, Environment.SPACECRAFT, NOW)
    assert measurement == Measurement(
        crew_id="crew-01",
        indicator=Indicator.MOOD,
        value=float(level),
        unit="score",
        timestamp=NOW,
        source=Source.MANUAL,
        environment=Environment.SPACECRAFT,
        method=Method.SURVEY,
    )
    assert Measurement.from_dict(measurement.to_dict()) == measurement


@pytest.mark.parametrize("level", [0, 6, -1, 3.5, True])
def test_a_level_outside_the_scale_is_refused(level: int) -> None:
    with pytest.raises(ValueError, match="level"):
        mood_measurement("crew-01", level, Environment.EARTH, NOW)
