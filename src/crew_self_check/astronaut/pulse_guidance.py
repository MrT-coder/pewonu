"""What to do after counting the pulse (A5). Pure logic: it returns text keys, never prose.

The guidance is educational and cites a public source (MedlinePlus, "How to take your pulse",
https://medlineplus.gov/ency/article/003399.htm): a resting count needs at least 10 minutes of rest,
a fast pulse may signal infection or dehydration, a continually high pulse or an uneven one is worth
telling a health professional. There is no dose and no clinical step of our own (AGENTS.md,
section 6): who to tell comes from the same suggestion the system card shows (``escalation_for``).
"""

from __future__ import annotations

from dataclasses import dataclass

from crew_self_check.core.contract import Escalation, Status
from crew_self_check.core.status import IndicatorResolution, escalation_for


@dataclass(frozen=True, slots=True)
class PulseGuidance:
    status: Status | None  # ``None``: nothing to compare with
    steps: tuple[str, ...]  # text keys, in the order they are shown
    escalation: Escalation  # who could be told (a suggestion, nothing is sent)


_OUTSIDE = (
    "pulse.todo.rest",
    "pulse.todo.recount",
    "pulse.todo.fluids",
    "pulse.todo.uneven",
)


def outside_band(resolution: IndicatorResolution) -> bool:
    """The count sits outside the person's own band, even if it is not sustained (not amber yet)."""
    baseline, latest = resolution.status.baseline, resolution.status.latest
    if baseline is None or latest is None:
        return False
    return latest < baseline.low or latest > baseline.high


def pulse_guidance(status: Status | None, outside: bool = False) -> PulseGuidance:
    """``outside``: the count is outside the band but the state is still ``ok`` (one count only)."""
    if status in (Status.WATCH, Status.ACT):
        return PulseGuidance(status, _OUTSIDE, escalation_for(status))
    if status is Status.OK and outside:
        return PulseGuidance(
            status,
            ("pulse.todo.single", "pulse.todo.rest", "pulse.todo.recount"),
            Escalation.SELF_CARE,
        )
    if status is Status.OK:
        return PulseGuidance(
            status, ("pulse.todo.same_time", "pulse.todo.rest_first"), escalation_for(status)
        )
    return PulseGuidance(
        status, ("pulse.todo.keep_measuring", "pulse.todo.rest_first"), Escalation.SELF_CARE
    )
