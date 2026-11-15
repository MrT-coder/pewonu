"""SQLite adapter of the bundle inbox. Standard library only; one local file."""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path

from crew_self_check.core.inbox import ReceivedBundle

_SCHEMA = """
CREATE TABLE IF NOT EXISTS bundles (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    bundle_id TEXT NOT NULL UNIQUE,
    crew_id TEXT NOT NULL,
    sent_at TEXT NOT NULL,
    received_at TEXT NOT NULL,
    available_at TEXT NOT NULL,
    readings INTEGER NOT NULL,
    states INTEGER NOT NULL,
    payload TEXT NOT NULL
)
"""
_COLUMNS = "bundle_id, crew_id, sent_at, received_at, available_at, readings, states, payload"

_Row = tuple[str, str, str, str, str, int, int, str]


class SqliteBundleInbox:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()  # the web server answers on worker threads
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(_SCHEMA)
        self._db.commit()

    def add(self, item: ReceivedBundle) -> None:
        with self._lock:
            self._db.execute(
                f"INSERT OR IGNORE INTO bundles ({_COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    item.bundle_id,
                    item.crew_id,
                    item.sent_at.isoformat(),
                    item.received_at.isoformat(),
                    item.available_at.isoformat(),
                    item.readings,
                    item.states,
                    json.dumps(item.bundle),
                ),
            )
            self._db.commit()

    def get(self, bundle_id: str) -> ReceivedBundle | None:
        with self._lock:
            row = self._db.execute(
                f"SELECT {_COLUMNS} FROM bundles WHERE bundle_id = ?", (bundle_id,)
            ).fetchone()
        return _item(row) if row else None

    def all(self) -> tuple[ReceivedBundle, ...]:
        with self._lock:
            rows = self._db.execute(f"SELECT {_COLUMNS} FROM bundles ORDER BY seq").fetchall()
        return tuple(_item(row) for row in rows)

    def close(self) -> None:
        with self._lock:
            self._db.close()


def _item(row: _Row) -> ReceivedBundle:
    return ReceivedBundle(
        bundle_id=row[0],
        crew_id=row[1],
        sent_at=datetime.fromisoformat(row[2]),
        received_at=datetime.fromisoformat(row[3]),
        available_at=datetime.fromisoformat(row[4]),
        readings=row[5],
        states=row[6],
        bundle=json.loads(row[7]),
    )
