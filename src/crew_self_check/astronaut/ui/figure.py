"""The body figure of the single screen: an original silhouette with tappable zones (UX v2).

The silhouette is ``assets/body.svg`` (drawn for this project). Each zone takes the color of
the state the engine calculated for its system; tapping it opens that system in a modal, and
the wrist opens the pulse. Nothing here computes a state.
"""

from __future__ import annotations

from dataclasses import dataclass

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, status_color
from crew_self_check.core.contract import Indicator, Status, System

STAGE_WIDTH = 720
STAGE_HEIGHT = 580
_BODY_LEFT = 210  # the silhouette is 300 wide and sits in the middle of the stage
_LABEL_WIDTH = 204


@dataclass(frozen=True, slots=True)
class _Zone:
    key: str  # "wrist" or a system value
    system: System | None  # ``None`` for the wrist (it opens the pulse)
    x: int  # position and size in the silhouette's own units
    y: int
    w: int
    h: int
    round: bool
    side: str  # which side the label sits on: "l" or "r"
    anchor_y: int


_ZONES = (
    _Zone("sleep_brain", System.SLEEP_BRAIN, 126, 22, 48, 48, True, "r", 46),
    _Zone("vestibular", System.VESTIBULAR, 115, 42, 12, 20, True, "l", 52),
    _Zone("cardiovascular", System.CARDIOVASCULAR, 112, 130, 52, 60, True, "r", 160),
    _Zone("immune", System.IMMUNE, 112, 205, 76, 40, False, "r", 225),
    _Zone("wrist", None, 41, 270, 28, 28, True, "l", 284),
    _Zone("bone_muscle", System.BONE_MUSCLE, 98, 340, 104, 150, False, "r", 420),
)


# the short wording of each state, so a label fits on one line
_SHORT: dict[Status | None, str] = {
    Status.OK: "summary.short.ok",
    Status.WATCH: "summary.short.watch",
    Status.ACT: "summary.short.act",
    Status.INSUFFICIENT_DATA: "summary.short.insufficient_data",
    None: "summary.short.nothing",
}


def _zone_status(state: AppState, zone: _Zone) -> Status | None:
    if zone.system is None:
        return state.resolutions()[Indicator.RESTING_HR].status.status
    status = state.system_statuses().get(zone.system)
    return status.status if status else None


def _zone_name(state: AppState, zone: _Zone) -> str:
    key = "zone.wrist" if zone.system is None else f"system.{zone.system.value}"
    return translate(key, state.language)


def _open(state: AppState, actions: Actions, zone: _Zone) -> None:
    if zone.system is None:
        state.open_pulse()
    else:
        state.open_zone(zone.system)
    actions.rerender()


def _label(
    state: AppState, actions: Actions, zone: _Zone, status: Status | None, color: str
) -> ft.Control:
    left_edge = _BODY_LEFT - 6 - _LABEL_WIDTH + 0 if zone.side == "l" else _BODY_LEFT + 300 - 14
    return ft.GestureDetector(
        left=left_edge,
        top=zone.anchor_y - 14,
        on_tap=lambda _: _open(state, actions, zone),
        content=ft.Container(
            width=_LABEL_WIDTH,
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(0.78, "#06101f"),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.5, color)),
            content=ft.Row(
                spacing=6,
                tight=True,
                alignment=ft.MainAxisAlignment.END
                if zone.side == "l"
                else ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(width=9, height=9, border_radius=5, bgcolor=color),
                    ft.Column(
                        tight=True,
                        spacing=0,
                        controls=[
                            ft.Text(
                                _zone_name(state, zone),
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                width=_LABEL_WIDTH - 44,
                                size=11,
                                weight=ft.FontWeight.W_600,
                                color=theme.TEXT,
                            ),
                            ft.Text(
                                translate(_SHORT[status], state.language),
                                size=10,
                                color=theme.MUTED,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )


def _leader(zone: _Zone, color: str) -> ft.Control:
    """A thin line from the zone to its label."""
    cx = _BODY_LEFT + zone.x + zone.w // 2
    edge = _BODY_LEFT - 6 if zone.side == "l" else _BODY_LEFT + 300 - 14
    left, right = (edge, cx) if zone.side == "l" else (cx, edge)
    return ft.Container(
        left=left,
        top=zone.anchor_y,
        width=max(right - left, 0),
        height=1,
        bgcolor=ft.Colors.with_opacity(0.5, color),
    )


def _hotspot(
    state: AppState,
    actions: Actions,
    zone: _Zone,
    color: str,
    flagged: bool,
    known: bool,
) -> ft.Control:
    return ft.GestureDetector(
        left=_BODY_LEFT + zone.x,
        top=zone.y,
        on_tap=lambda _: _open(state, actions, zone),
        content=ft.Container(
            width=zone.w,
            height=zone.h,
            border_radius=zone.w // 2 if zone.round else 18,
            bgcolor=ft.Colors.with_opacity(0.28 if known else 0.1, color),
            border=ft.Border.all(3 if known else 1, color),
            shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.6, color))
            if flagged
            else None,
        ),
    )


def build_figure(state: AppState, actions: Actions) -> ft.Control:
    layers: list[ft.Control] = [
        ft.Image(
            src="body.svg",
            left=_BODY_LEFT,
            top=0,
            width=300,
            height=STAGE_HEIGHT,
            fit=ft.BoxFit.CONTAIN,
        )
    ]
    leaders: list[ft.Control] = []
    spots: list[ft.Control] = []
    labels: list[ft.Control] = []
    for zone in _ZONES:
        status = _zone_status(state, zone)
        color = status_color(status)
        leaders.append(_leader(zone, color))
        flagged = status in (Status.WATCH, Status.ACT)
        spots.append(_hotspot(state, actions, zone, color, flagged, status is not None))
        labels.append(_label(state, actions, zone, status, color))
    return ft.Stack(
        width=STAGE_WIDTH, height=STAGE_HEIGHT, controls=[*layers, *leaders, *spots, *labels]
    )
