"""Smoke test: the three packages exist and the core does not depend on the two systems."""

import importlib
import sys

import pytest

PACKAGES = ["core", "astronaut", "ground"]


@pytest.mark.parametrize("name", PACKAGES)
def test_package_is_importable(name: str) -> None:
    assert importlib.import_module(f"crew_self_check.{name}")


def test_core_does_not_import_the_systems() -> None:
    for name in ("crew_self_check.astronaut", "crew_self_check.ground"):
        sys.modules.pop(name, None)
    importlib.reload(importlib.import_module("crew_self_check.core"))
    assert "crew_self_check.astronaut" not in sys.modules
    assert "crew_self_check.ground" not in sys.modules
