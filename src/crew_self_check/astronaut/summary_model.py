"""The summary per astronaut: a few human numbers built from what the engine already calculated.

Nothing here is a clinical number and nothing is new: it counts states, lists what is outside its
range, and measures **regularity** (how often the astronaut measures, never how they are) and how
well the app already knows them in this space (D-013). Pure logic, no UI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Environment, Indicator, IndicatorStatus, Reference, Status
from crew_self_check.core.status import IndicatorResolution

REGULARITY_DAYS = 7  # the window of the regularity count


@dataclass(frozen=True, slots=True)
class StateCounts:
    ok: int = 0
    watch: int = 0
    act: int = 0
    gray: int = 0
    nothing: int = 0  # systems with nothing measured for them

    @property
    def total(self) -> int:
        return self.ok + self.watch + self.act + self.gray + self.nothing


@dataclass(frozen=True, slots=True)
class BaselineReadiness:
    ready: int  # indicators with a mature personal baseline in this space
    total: int  # indicators that have any reading in this space


@dataclass(frozen=True, slots=True)
class CheckIn:
    pulse: bool
    mood: bool


@dataclass(frozen=True, slots=True)
class ReadingRow:
    indicator: Indicator
    value: float
    unit: str
    status: IndicatorStatus


@dataclass(frozen=True, slots=True)
class Summary:
    crew_code: str | None
    day_label: str
    environment: Environment
    counts: StateCounts
    attention: tuple[IndicatorResolution, ...]  # outside the range, the worst first
    days_measured: int  # days with any reading among the last seven
    baseline: BaselineReadiness
    checked_in: CheckIn
    rows: tuple[ReadingRow, ...]


def _counts(state: AppState) -> StateCounts:
    ok = watch = act = gray = nothing = 0
    for system_status in state.system_statuses().values():
        if system_status is None:
            nothing += 1
        elif system_status.status is Status.OK:
            ok += 1
        elif system_status.status is Status.WATCH:
            watch += 1
        elif system_status.status is Status.ACT:
            act += 1
        else:
            gray += 1
    return StateCounts(ok, watch, act, gray, nothing)


def build_summary(state: AppState) -> Summary:
    day = state.current_day
    if state.profile is None:
        return Summary(
            None, day.label, state.environment, StateCounts(), (), 0,
            BaselineReadiness(0, 0), CheckIn(False, False), (),
        )  # fmt: skip

    resolutions = state.resolutions()
    visible = state.visible_measurements()

    attention = tuple(
        sorted(
            (r for r in resolutions.values() if r.status.status in (Status.WATCH, Status.ACT)),
            key=lambda r: (0 if r.status.status is Status.ACT else 1, r.status.indicator.value),
        )
    )

    today = day.timestamp.date()
    window = {today - timedelta(days=n) for n in range(REGULARITY_DAYS)}
    days_measured = len({m.timestamp.date() for m in visible if m.timestamp.date() in window})

    known = {m.indicator for m in visible if m.environment is state.environment}
    mature = (Status.OK, Status.WATCH, Status.ACT)
    ready = sum(
        1
        for indicator in known
        if resolutions[indicator].status.reference is Reference.PERSONAL
        and resolutions[indicator].status.status in mature
    )

    own_today = [m for m in state.own_measurements() if m.timestamp.date() == today]
    checked_in = CheckIn(
        pulse=any(m.indicator is Indicator.RESTING_HR for m in own_today),
        mood=any(m.indicator is Indicator.MOOD for m in own_today),
    )

    rows = []
    for indicator in Indicator:
        status = resolutions[indicator].status
        if status.latest is None:
            continue
        unit = next((m.unit for m in reversed(visible) if m.indicator is indicator), "")
        rows.append(ReadingRow(indicator, status.latest, unit, status))

    return Summary(
        crew_code=state.code,
        day_label=day.label,
        environment=state.environment,
        counts=_counts(state),
        attention=attention,
        days_measured=days_measured,
        baseline=BaselineReadiness(ready, len(known)),
        checked_in=checked_in,
        rows=tuple(rows),
    )
