"""One command for the whole system: ``uv run pewonu``.

Starts the ground base in the background (http://127.0.0.1:8560) and the astronaut app in front
(http://127.0.0.1:8550, opened in the browser). Closing the astronaut app stops the ground base.
Everything runs on this computer only.
"""

import subprocess
import sys
import threading
import webbrowser

GROUND_URL = "http://127.0.0.1:8560"
OPEN_GROUND_AFTER_SECONDS = 4.0


def ground_command() -> list[str]:
    return [sys.executable, "-m", "crew_self_check.ground"]


def run_astronaut() -> None:
    from crew_self_check.astronaut.ui.app import run

    run()


def open_ground_page_later() -> None:
    timer = threading.Timer(OPEN_GROUND_AFTER_SECONDS, webbrowser.open, args=(GROUND_URL,))
    timer.daemon = True
    timer.start()


def main() -> None:
    ground = subprocess.Popen(ground_command())
    try:
        open_ground_page_later()
        run_astronaut()
    finally:
        ground.terminate()
        try:
            ground.wait(timeout=5)
        except subprocess.TimeoutExpired:
            ground.kill()
