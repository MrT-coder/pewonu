"""A2: measurements live behind a storage port; SQLite is one adapter, memory another."""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from crew_self_check.astronaut.access import simulated_directory
from crew_self_check.astronaut.sqlite_store import SqliteMeasurementStore
from crew_self_check.astronaut.state import AppState
from crew_self_check.core.contract import Environment, Indicator, Measurement, Method, Source
from crew_self_check.core.storage import InMemoryMeasurementStore, MeasurementStore

NOW = datetime(2026, 11, 14, 12, 0, tzinfo=UTC)


def _measurement(crew_id: str = "AST-0000", value: float = 62.0, method: Method | None = None):
    return Measurement(
        crew_id=crew_id,
        indicator=Indicator.RESTING_HR,
        value=value,
        unit="/min",
        timestamp=NOW,
        source=Source.MANUAL,
        environment=Environment.EARTH,
        method=method,
    )


@pytest.fixture(params=["memory", "sqlite"])
def store(request: pytest.FixtureRequest, tmp_path: Path) -> MeasurementStore:
    if request.param == "memory":
        return InMemoryMeasurementStore()
    return SqliteMeasurementStore(tmp_path / "crew.db")


def test_a_new_store_is_empty(store: MeasurementStore) -> None:
    assert store.all() == ()


def test_it_keeps_what_was_added_in_order(store: MeasurementStore) -> None:
    first, second = _measurement(value=60), _measurement(value=64, method=Method.PALPATION)
    store.add(first)
    store.add(second)
    assert store.all() == (first, second)


def test_it_keeps_the_crews_apart(store: MeasurementStore) -> None:
    mine, other = _measurement("AST-0000"), _measurement("AST-0001")
    store.add(mine)
    store.add(other)
    assert store.for_crew("AST-0000") == (mine,)


def test_sqlite_data_survives_a_restart(tmp_path: Path) -> None:
    path = tmp_path / "crew.db"
    saved = _measurement(method=Method.PALPATION)
    first = SqliteMeasurementStore(path)
    first.add(saved)
    first.close()
    assert SqliteMeasurementStore(path).all() == (saved,)


def test_sqlite_creates_missing_folders(tmp_path: Path) -> None:
    store = SqliteMeasurementStore(tmp_path / "nested" / "dir" / "crew.db")
    store.add(_measurement())
    assert len(store.all()) == 1


def test_the_state_uses_the_injected_store() -> None:
    store = InMemoryMeasurementStore()
    state = AppState(simulated_directory(), store=store)
    state.login(state.demo_codes()[0])
    state.choose_mood(3)
    saved = state.save_mood()
    assert store.all() == (saved,)
    assert state.own_measurements() == (saved,)


def test_the_state_defaults_to_memory() -> None:
    state = AppState(simulated_directory())
    state.login(state.demo_codes()[0])
    state.choose_mood(3)
    saved = state.save_mood()
    assert state.own_measurements() == (saved,)


def test_a_new_state_over_the_same_database_sees_the_old_data(tmp_path: Path) -> None:
    path = tmp_path / "crew.db"
    first = AppState(simulated_directory(), store=SqliteMeasurementStore(path))
    first.login(first.demo_codes()[0])
    first.choose_mood(4)
    saved = first.save_mood()
    second = AppState(simulated_directory(), store=SqliteMeasurementStore(path))
    second.login(second.demo_codes()[0])
    assert second.own_measurements() == (saved,)
