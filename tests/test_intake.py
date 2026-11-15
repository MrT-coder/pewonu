"""The data intake view: what came in, from where, and what it shows (A17)."""

from __future__ import annotations

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.intake import FEED_DAYS, SourceKind, build_intake
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Indicator, Source


def _state(code_index: int = 0, day: str | None = None) -> AppState:
    state = AppState(simulated_directory())
    state.login(state.demo_codes()[code_index])
    if day is not None:
        state.set_day(next(d.index for d in state.scenario.days if d.label == day))
    return state


def test_nothing_is_shown_without_a_session() -> None:
    state = AppState(simulated_directory())
    intake = build_intake(state)
    assert intake.total_readings == 0
    assert intake.sources == ()
    assert intake.feed == ()


def test_the_totals_are_what_the_person_has_received_so_far() -> None:
    state = _state()
    intake = build_intake(state)
    assert intake.total_readings == len(state.visible_measurements())
    assert intake.indicators_covered == len({m.indicator for m in state.visible_measurements()})
    assert intake.indicators_total == len(Indicator)


def test_each_source_says_what_it_delivers() -> None:
    intake = build_intake(_state())
    by_kind = {row.kind: row for row in intake.sources}
    assert Indicator.SYSTOLIC_BP in by_kind[SourceKind.WEARABLE].indicators
    assert by_kind[SourceKind.HAND_PULSE].indicators == (Indicator.RESTING_HR,)
    assert Indicator.MOOD in by_kind[SourceKind.SURVEY].indicators
    assert sum(row.readings for row in intake.sources) == intake.total_readings


def test_the_feed_is_newest_first_and_counts_the_days_readings() -> None:
    state = _state(day="T+3")
    intake = build_intake(state)
    assert 1 <= len(intake.feed) <= FEED_DAYS
    assert intake.feed[0].label == "T+3"
    days = [entry.label for entry in intake.feed]
    assert days == sorted(days, key=lambda label: _order(state, label), reverse=True)
    today = state.current_day.timestamp.date()
    expected = sum(1 for m in state.visible_measurements() if m.timestamp.date() == today)
    assert intake.feed[0].total == expected


def _order(state: AppState, label: str) -> int:
    return next(d.index for d in state.scenario.days if d.label == label)


def test_a_person_with_little_data_shows_it_plainly() -> None:
    intake = build_intake(_state(1, "R+2"))
    kinds = {row.kind for row in intake.sources}
    assert kinds == {SourceKind.HAND_PULSE}
    assert intake.indicators_covered == 1


def test_what_the_astronaut_enters_is_a_source_of_its_own_and_shows_in_the_feed() -> None:
    state = _state()
    state.choose_mood(3)
    state.save_mood()
    intake = build_intake(state)
    entered = next(row for row in intake.sources if row.kind is SourceKind.ENTERED)
    assert entered.readings == 1
    assert entered.indicators == (Indicator.MOOD,)
    assert intake.feed[0].counts[SourceKind.ENTERED] == 1


def test_the_origin_is_always_labelled_and_simulated_data_is_flagged() -> None:
    intake = build_intake(_state())
    assert Source.SIMULATED_SCENARIO in intake.origins
    assert intake.simulated


def test_it_counts_only_the_signed_in_persons_readings() -> None:
    for index, crew_id in enumerate(("crew-01", "crew-02", "crew-03")):
        state = _state(index, "R+2")
        cutoff = state.current_day.timestamp.date()
        own = [
            m
            for m in state.scenario.measurements
            if m.crew_id == crew_id and m.timestamp.date() <= cutoff
        ]
        assert build_intake(state).total_readings == len(own)


def test_more_days_bring_more_readings_in() -> None:
    state = _state()
    before = build_intake(state).total_readings
    state.advance()
    assert build_intake(state).total_readings > before
