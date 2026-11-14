"""The mood survey: five faces, one tap (D-015). Pure logic.

The survey is the only thing that feeds the ``mood`` state: it is a self-report (``method:
survey``), never an inference from the voice or from anything else.
"""

from __future__ import annotations

from datetime import datetime

from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source

MOOD_LEVELS = (1, 2, 3, 4, 5)  # 1 is the lowest face, 5 the highest


def check_level(level: object) -> int:
    """The level as an ``int``, or ``ValueError`` if it is not one of the five faces."""
    if isinstance(level, bool) or not isinstance(level, int) or level not in MOOD_LEVELS:
        raise ValueError(f"level must be one of {MOOD_LEVELS}, got {level!r}")
    return level


def mood_measurement(
    crew_id: str, level: int, environment: Environment, timestamp: datetime
) -> Measurement:
    return Measurement(
        crew_id=crew_id,
        indicator=Indicator.MOOD,
        value=float(check_level(level)),
        unit="score",
        timestamp=timestamp,
        source=Source.MANUAL,
        environment=environment,
        method=Method.SURVEY,
    )
