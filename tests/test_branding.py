"""D-030: the product is called PeWoNu and shows its logo (transparent PNG) in both systems."""

from pathlib import Path

from fastapi.testclient import TestClient

from crew_self_check.astronaut.i18n import translate
from crew_self_check.core.inbox import InMemoryBundleInbox
from crew_self_check.core.reasons import Language
from crew_self_check.ground.api import create_app
from crew_self_check.ground.service import GroundService

PNG = bytes([0x89, 0x50, 0x4E, 0x47])
ASTRONAUT_LOGO = Path("src/crew_self_check/astronaut/assets/brand/pewonu.png")


def _png_has_alpha(path: Path) -> bool:
    data = path.read_bytes()
    return data[:4] == PNG and data[25] == 6  # IHDR color type 6 = RGBA


def test_the_astronaut_app_is_named_pewonu_in_both_languages() -> None:
    for language in Language:
        assert translate("app.name", language) == "PeWoNu"


def test_the_logo_is_a_png_with_a_transparent_background() -> None:
    assert _png_has_alpha(ASTRONAUT_LOGO)


def test_the_ground_base_is_named_pewonu_and_serves_the_logo() -> None:
    client = TestClient(create_app(GroundService(InMemoryBundleInbox())))
    page = client.get("/?lang=en").text
    assert "PeWoNu" in page and "Crew Self-Check" not in page
    assert '<img class="logo"' in page
    logo = client.get("/brand/pewonu.png")
    assert logo.status_code == 200
    assert logo.headers["content-type"] == "image/png"
    assert logo.content[:4] == PNG


GROUND_LOGO = Path("src/crew_self_check/ground/static/pewonu.png")


def test_both_systems_ship_the_same_logo_with_the_ai_mark_strip() -> None:
    assert GROUND_LOGO.read_bytes() == ASTRONAUT_LOGO.read_bytes()
    data = ASTRONAUT_LOGO.read_bytes()
    width, height = int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    assert height > width * 1.2  # the original logo plus the strip that holds the mark
