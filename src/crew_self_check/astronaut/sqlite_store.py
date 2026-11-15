"""SQLite adapter of the measurement storage port. Standard library only; local file, no network."""

from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

from crew_self_check.core.contract import Measurement

_SCHEMA = """
CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crew_id TEXT NOT NULL,
    payload TEXT NOT NULL
)
"""


class SqliteMeasurementStore:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Flet runs handlers on worker threads: one shared connection, guarded by a lock.
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(_SCHEMA)
        self._db.commit()

    def add(self, measurement: Measurement) -> None:
        with self._lock:
            self._db.execute(
                "INSERT INTO measurements (crew_id, payload) VALUES (?, ?)",
                (measurement.crew_id, json.dumps(measurement.to_dict())),
            )
            self._db.commit()

    def all(self) -> tuple[Measurement, ...]:
        with self._lock:
            rows = self._db.execute("SELECT payload FROM measurements ORDER BY id").fetchall()
        return tuple(Measurement.from_dict(json.loads(row[0])) for row in rows)

    def for_crew(self, crew_id: str) -> tuple[Measurement, ...]:
        with self._lock:
            rows = self._db.execute(
                "SELECT payload FROM measurements WHERE crew_id = ? ORDER BY id", (crew_id,)
            ).fetchall()
        return tuple(Measurement.from_dict(json.loads(row[0])) for row in rows)

    def close(self) -> None:
        with self._lock:
            self._db.close()
