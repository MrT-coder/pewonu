"""Status resolution (D-013, D-014): reference, indicator status, system status, escalation.

Reference order for one person, indicator and environment:

1. ``personal``: the baseline of this environment, once mature (C3).
2. ``transition``: the baseline of the previous environment, while the own one is still building.
3. ``population``: the NHSR nº 41 table, only for the resting pulse and only with a crew profile.
4. Otherwise ``insufficient_data`` (gray).

The reason is always a template (``reasons.py``). Nothing here touches an LLM, a file or the
network, and nothing diagnoses: the output is "compared with what", never "what you have".
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta

from crew_self_check.core.baseline import (
    DEFAULT_CONFIG,
    BaselineConfig,
    Direction,
    assess,
    sustained_direction,
)
from crew_self_check.core.contract import (
    Baseline,
    CrewProfile,
    Environment,
    Escalation,
    Indicator,
    IndicatorStatus,
    Measurement,
    Reference,
    Status,
    System,
    SystemStatus,
    TrendPoint,
)
from crew_self_check.core.pulse_reference import population_status, reference_row
from crew_self_check.core.reasons import Language, Reason, ReasonCode

# [SUPOSICION] a reading older than this is not "recent" (only when the caller gives a clock).
DEFAULT_MAX_READING_AGE_DAYS = 3

# Where the journey comes from, nearest first (D-013: Earth -> spacecraft -> planet).
_PREVIOUS: dict[Environment, tuple[Environment, ...]] = {
    Environment.EARTH: (),
    Environment.SPACECRAFT: (Environment.EARTH,),
    Environment.PLANET: (Environment.SPACECRAFT, Environment.EARTH),
}

# [SUPOSICION] The contract only fixes cardiovascular. Each measured indicator sits in one system;
# ``blood_glucose`` has no zone on the figure yet and ``bone_muscle`` has nothing to measure
# (simulated only, D-016).
SYSTEM_INDICATORS: dict[System, tuple[Indicator, ...]] = {
    System.CARDIOVASCULAR: (
        Indicator.RESTING_HR,
        Indicator.SYSTOLIC_BP,
        Indicator.DIASTOLIC_BP,
        Indicator.ORTHOSTATIC_HR_DELTA,
        Indicator.SPO2,
    ),
    System.VESTIBULAR: (Indicator.VESTIBULAR_SYMPTOMS, Indicator.TANDEM_WALK_OK),
    System.SLEEP_BRAIN: (Indicator.SLEEP_HOURS,),
    System.MOOD: (Indicator.MOOD,),
    System.BONE_MUSCLE: (),
    System.IMMUNE: (Indicator.BODY_TEMP,),
}

_SEVERITY = {Status.OK: 0, Status.WATCH: 1, Status.ACT: 2}


@dataclass(frozen=True, slots=True)
class IndicatorResolution:
    status: IndicatorStatus  # ``status.reason`` is the English text
    reason: Reason  # render it in the app language with ``reason.text(Language.ES)``


def escalation_for(status: Status) -> Escalation:
    """A suggestion only: the app never sends anything without the astronaut's confirmation."""
    if status is Status.ACT:
        return Escalation.GROUND_SURGEON
    if status is Status.WATCH:
        return Escalation.CREW_CMO
    return Escalation.SELF_CARE


def _days_with_readings(
    data: list[Measurement], crew_id: str, indicator: Indicator, environment: Environment
) -> int:
    return len(
        {
            m.timestamp.date()
            for m in data
            if m.crew_id == crew_id and m.indicator is indicator and m.environment is environment
        }
    )


def _personal_reason(status: Status, direction: Direction | None, n: int) -> Reason:
    if status is Status.OK:
        return Reason(ReasonCode.PERSONAL_OK)
    code = ReasonCode.PERSONAL_ABOVE if direction is Direction.ABOVE else ReasonCode.PERSONAL_BELOW
    return Reason(code, {"n": n})


def _transition_reason(direction: Direction | None, n: int, previous: Environment) -> Reason:
    if direction is None:
        return Reason(ReasonCode.TRANSITION_OK, {"previous": previous})
    code = (
        ReasonCode.TRANSITION_ABOVE if direction is Direction.ABOVE else ReasonCode.TRANSITION_BELOW
    )
    return Reason(code, {"n": n, "previous": previous})


_POPULATION_CODES = {
    (Status.OK, True): ReasonCode.POPULATION_OK,
    (Status.OK, False): ReasonCode.POPULATION_OK,
    (Status.WATCH, True): ReasonCode.POPULATION_WATCH_HIGH,
    (Status.WATCH, False): ReasonCode.POPULATION_WATCH_LOW,
    (Status.ACT, True): ReasonCode.POPULATION_ACT_HIGH,
    (Status.ACT, False): ReasonCode.POPULATION_ACT_LOW,
}


def resolve_indicator(
    measurements: Iterable[Measurement],
    crew_id: str,
    indicator: Indicator,
    environment: Environment,
    *,
    profile: CrewProfile | None = None,
    config: BaselineConfig = DEFAULT_CONFIG,
    as_of: datetime | None = None,
    max_reading_age_days: int = DEFAULT_MAX_READING_AGE_DAYS,
) -> IndicatorResolution:
    """Resolve one indicator of one person in one environment.

    ``as_of`` is the current time. Without it nothing is considered stale; with it, a latest
    reading older than ``max_reading_age_days`` turns the state gray (D-013).
    """
    data = list(measurements)
    own = assess(data, crew_id, indicator, environment, config)

    status = Status.INSUFFICIENT_DATA
    reference = Reference.PERSONAL
    baseline: Baseline | None = None
    previous: Environment | None = None
    reason = Reason(ReasonCode.NO_DATA)

    if own.latest is not None:
        days = _days_with_readings(data, crew_id, indicator, environment)
        reason = Reason(ReasonCode.BUILDING_BASELINE, {"days": days, "needed": config.min_days})
        previous, previous_baseline = _previous(data, crew_id, indicator, environment, config)

        if own.baseline is not None:
            status, baseline = own.status, own.baseline
            reason = _personal_reason(status, own.direction, config.sustained)
            previous = None
        elif previous is not None and previous_baseline is not None:
            reference, baseline = Reference.TRANSITION, previous_baseline
            if len(own.recent) < config.sustained:
                reason = Reason(
                    ReasonCode.WAITING_TRANSITION,
                    {"have": len(own.recent), "needed": config.sustained, "previous": previous},
                )
            else:
                direction = sustained_direction(
                    [p.value for p in own.recent], previous_baseline, config.sustained
                )
                status = Status.OK if direction is None else Status.WATCH
                reason = _transition_reason(direction, config.sustained, previous)
        else:
            previous = None
            population = _population(indicator, crew_id, profile, own.latest)
            if population is not None:
                status, reason = population
                reference = Reference.POPULATION

        stale = _stale_days(own.recent, as_of, max_reading_age_days)
        if stale is not None:
            status, reason = (
                Status.INSUFFICIENT_DATA,
                Reason(ReasonCode.STALE_READING, {"days": stale}),
            )

    return IndicatorResolution(
        IndicatorStatus(
            crew_id=crew_id,
            indicator=indicator,
            status=status,
            reason=reason.text(Language.EN),
            escalation=escalation_for(status),
            environment=environment,
            reference=reference,
            trend=own.recent,
            baseline=baseline,
            latest=own.latest,
            baseline_environment=previous if reference is Reference.TRANSITION else None,
        ),
        reason,
    )


def _previous(
    data: list[Measurement],
    crew_id: str,
    indicator: Indicator,
    environment: Environment,
    config: BaselineConfig,
) -> tuple[Environment | None, Baseline | None]:
    """The nearest earlier environment with a mature baseline, or ``(None, None)``."""
    for candidate in _PREVIOUS[environment]:
        baseline = assess(data, crew_id, indicator, candidate, config).baseline
        if baseline is not None:
            return candidate, baseline
    return None, None


def _population(
    indicator: Indicator, crew_id: str, profile: CrewProfile | None, latest: float
) -> tuple[Status, Reason] | None:
    if indicator is not Indicator.RESTING_HR or profile is None or profile.crew_id != crew_id:
        return None
    status = population_status(latest, profile.age, profile.sex)
    row = reference_row(profile.age, profile.sex)
    if status is None or row is None:
        return None
    high = latest > row.percentile_values[5]  # above the median of the reference row
    return status, Reason(_POPULATION_CODES[(status, high)])


def _stale_days(
    recent: tuple[TrendPoint, ...], as_of: datetime | None, max_age_days: int
) -> int | None:
    if as_of is None or not recent:
        return None
    age = as_of - recent[-1].timestamp
    return age.days if age > timedelta(days=max_age_days) else None


def resolve_system(
    crew_id: str, system: System, statuses: Iterable[IndicatorStatus]
) -> SystemStatus | None:
    """The system is as bad as its worst indicator; gray only if none has a state (contract §3).

    Returns ``None`` for a system with no measured indicator (``bone_muscle``).
    """
    indicators = SYSTEM_INDICATORS[system]
    if not indicators:
        return None
    states = [
        s.status
        for s in statuses
        if s.crew_id == crew_id and s.indicator in indicators and s.status in _SEVERITY
    ]
    worst = max(states, key=_SEVERITY.__getitem__) if states else Status.INSUFFICIENT_DATA
    return SystemStatus(crew_id=crew_id, system=system, status=worst, indicators=indicators)
