"""``pewonu`` starts the ground base in the background and the astronaut app in front."""

import sys
from typing import Any

import pytest

from crew_self_check import launcher


class FakeProcess:
    def __init__(self) -> None:
        self.terminated = False

    def terminate(self) -> None:
        self.terminated = True

    def wait(self, timeout: float | None = None) -> int:
        return 0


def test_the_ground_base_runs_as_a_module_of_the_same_python() -> None:
    assert launcher.ground_command() == [sys.executable, "-m", "crew_self_check.ground"]


def test_the_ground_base_is_stopped_when_the_astronaut_app_ends(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ground = FakeProcess()
    started: list[Any] = []
    monkeypatch.setattr(launcher.subprocess, "Popen", lambda cmd: started.append(cmd) or ground)
    monkeypatch.setattr(launcher, "run_astronaut", lambda: None)
    monkeypatch.setattr(launcher, "open_ground_page_later", lambda: None)
    launcher.main()
    assert started == [launcher.ground_command()]
    assert ground.terminated


def test_the_ground_base_is_stopped_even_if_the_astronaut_app_crashes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ground = FakeProcess()
    monkeypatch.setattr(launcher.subprocess, "Popen", lambda cmd: ground)
    monkeypatch.setattr(launcher, "open_ground_page_later", lambda: None)

    def crash() -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(launcher, "run_astronaut", crash)
    with pytest.raises(RuntimeError):
        launcher.main()
    assert ground.terminated
