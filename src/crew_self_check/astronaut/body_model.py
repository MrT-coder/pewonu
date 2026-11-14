"""What the body view says: labels, references, readings and trend data. Pure logic, no UI."""

from __future__ import annotations

from collections.abc import Sequence

from crew_self_check.astronaut.i18n import translate
from crew_self_check.core.contract import (
    Indicator,
    IndicatorStatus,
    Measurement,
    Reference,
    Status,
)
from crew_self_check.core.reasons import Language

TREND_READINGS = 14  # how many of the latest readings the trend shows

_STATUS_KEYS = {
    Status.OK: "status.ok",
    Status.WATCH: "status.watch",
    Status.ACT: "status.act",
    Status.INSUFFICIENT_DATA: "status.insufficient_data",
}


def status_label_key(status: Status | None) -> str:
    """The text key of a state; ``None`` is a system with nothing measured."""
    return "status.nothing" if status is None else _STATUS_KEYS[status]


def reference_text(status: IndicatorStatus, language: Language) -> str:
    """What the state was compared with, in plain words (the app always says it)."""
    if status.reference is Reference.TRANSITION and status.baseline_environment is not None:
        previous = translate(f"env.{status.baseline_environment.value}.short", language)
        return translate("reference.transition", language, previous=previous)
    if status.reference is Reference.POPULATION:
        return translate("reference.population", language)
    return translate("reference.personal", language)


def _number(value: float) -> str:
    return f"{value:g}"


def format_reading(indicator: Indicator, value: float, unit: str, language: Language) -> str:
    """A reading with a unit the astronaut understands (lpm in Spanish, a face for the mood)."""
    if indicator is Indicator.MOOD:
        return translate(f"mood.level.{round(value)}", language)
    if indicator is Indicator.TANDEM_WALK_OK:
        return translate("value.yes" if value >= 0.5 else "value.no", language)
    if indicator is Indicator.VESTIBULAR_SYMPTOMS:
        return f"{_number(value)} {translate('unit.points', language)}"
    shown = {"bpm": "lpm" if language is Language.ES else "bpm", "degC": "°C"}.get(unit, unit)
    return f"{_number(value)} {shown}"


def chart_series(
    visible: Sequence[Measurement], indicator: Indicator, limit: int = TREND_READINGS
) -> list[Measurement]:
    """The latest ``limit`` readings of one indicator, oldest first."""
    mine = sorted((m for m in visible if m.indicator is indicator), key=lambda m: m.timestamp)
    return mine[-limit:]
