"""Part 4: the summary per astronaut (the "human KPIs"). Pure model, no UI."""

from datetime import timedelta

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.summary_model import build_summary
from crew_self_check.core.contract import Indicator, Status


def start(code: str, label: str) -> AppState:
    state = AppState(simulated_directory())
    state.login(code)
    state.set_day(next(d.index for d in state.scenario.days if d.label == label))
    return state


def test_without_a_session_there_is_no_summary() -> None:
    summary = build_summary(AppState(simulated_directory()))
    assert summary.counts.total == 0
    assert summary.attention == ()
    assert summary.rows == ()


def test_on_the_last_day_on_earth_every_measured_system_is_in_range() -> None:
    summary = build_summary(start("AST-0001", "E-1"))
    counts = summary.counts
    assert counts.total == 6  # the six systems of the figure
    assert counts.act == 0
    assert counts.watch == 0
    assert counts.nothing == 1  # bones and muscles: nothing is measured for them
    assert counts.ok == 5
    assert summary.attention == ()


def test_on_arrival_two_systems_are_outside_the_range() -> None:
    summary = build_summary(start("AST-0001", "R+3"))
    counts = summary.counts
    assert (counts.ok, counts.watch, counts.act, counts.gray, counts.nothing) == (3, 2, 0, 0, 1)


def test_what_needs_attention_lists_only_states_outside_the_range_worst_first() -> None:
    summary = build_summary(start("AST-0002", "R+2"))
    first = summary.attention[0]
    assert first.status.indicator is Indicator.RESTING_HR
    assert first.status.status is Status.ACT
    states = [item.status.status for item in summary.attention]
    assert all(s in (Status.WATCH, Status.ACT) for s in states)
    assert states == sorted(states, key=lambda s: 0 if s is Status.ACT else 1)


def test_the_attention_list_of_the_first_astronaut_on_arrival_has_the_pulse() -> None:
    summary = build_summary(start("AST-0001", "R+3"))
    indicators = {item.status.indicator for item in summary.attention}
    assert Indicator.RESTING_HR in indicators
    assert Indicator.ORTHOSTATIC_HR_DELTA in indicators
    assert Indicator.SYSTOLIC_BP not in indicators


def test_the_regularity_counts_days_with_readings_in_the_last_seven() -> None:
    assert build_summary(start("AST-0001", "E-1")).days_measured == 7
    assert build_summary(start("AST-0002", "R+2")).days_measured == 5
    assert build_summary(start("AST-0002", "E-1")).days_measured == 0


def test_the_regularity_ignores_days_after_the_current_one() -> None:
    state = start("AST-0001", "E-1")
    early = start("AST-0001", "E-14")
    assert build_summary(early).days_measured == 1
    assert build_summary(state).days_measured == 7


def test_the_baseline_readiness_is_per_space() -> None:
    earth = build_summary(start("AST-0001", "E-1")).baseline
    assert (earth.ready, earth.total) == (10, 11)  # glucose is measured too rarely
    arrival = build_summary(start("AST-0001", "R+0")).baseline
    assert arrival.ready == 0  # a new space starts without its own baseline
    assert arrival.total == 10  # no glucose reading on the planet


def test_the_baseline_is_empty_where_there_are_no_readings() -> None:
    summary = build_summary(start("AST-0002", "E-1"))
    assert (summary.baseline.ready, summary.baseline.total) == (0, 0)


def test_the_check_in_flags_follow_what_was_recorded_today() -> None:
    state = start("AST-0001", "T+3")
    assert not build_summary(state).checked_in.pulse
    assert not build_summary(state).checked_in.mood
    state.start_pulse()
    assert state.pulse is not None
    for _ in range(3):
        state.pulse.complete_station()
    state.pulse.submit_count(35)
    state.save_pulse()
    state.choose_mood(4)
    state.save_mood()
    summary = build_summary(state)
    assert summary.checked_in.pulse
    assert summary.checked_in.mood
    state.advance()  # tomorrow: nothing recorded yet
    tomorrow = build_summary(state)
    assert not tomorrow.checked_in.pulse
    assert not tomorrow.checked_in.mood


def test_the_latest_readings_list_every_indicator_that_has_one() -> None:
    summary = build_summary(start("AST-0001", "R+3"))
    indicators = {row.indicator for row in summary.rows}
    assert Indicator.RESTING_HR in indicators
    assert Indicator.BLOOD_GLUCOSE not in indicators  # no glucose on the planet yet
    pulse = next(row for row in summary.rows if row.indicator is Indicator.RESTING_HR)
    assert pulse.value == 77
    assert pulse.unit == "bpm"
    assert pulse.status.status is Status.WATCH


def test_the_summary_is_about_the_day_shown() -> None:
    state = start("AST-0001", "R+3")
    summary = build_summary(state)
    assert summary.day_label == "R+3"
    assert summary.environment is state.environment
    assert summary.crew_code == "AST-0001"
    assert timedelta(0) <= state.journey_time() - state.current_day.timestamp < timedelta(days=1)
