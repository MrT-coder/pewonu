"""Run the ground base: ``uv run --extra ground python -m crew_self_check.ground``.

Serves on this computer only (127.0.0.1:8560). The database is ``data/ground.db`` unless
``CREW_SELF_CHECK_GROUND_DB`` says otherwise; ``data/`` is git-ignored (AGENTS.md section 8).
"""

import os
from pathlib import Path

import uvicorn

from crew_self_check.core.inbox import BundleInbox
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import GroundService
from crew_self_check.ground.sqlite_inbox import SqliteBundleInbox

HOST = "127.0.0.1"
PORT = 8560
DB_ENV = "CREW_SELF_CHECK_GROUND_DB"
DEFAULT_DB = Path("data") / "ground.db"


def build_inbox() -> BundleInbox:
    return SqliteBundleInbox(Path(os.environ.get(DB_ENV, DEFAULT_DB)))


def main() -> None:
    uvicorn.run(create_app(GroundService(build_inbox())), host=HOST, port=PORT)


if __name__ == "__main__":
    main()
