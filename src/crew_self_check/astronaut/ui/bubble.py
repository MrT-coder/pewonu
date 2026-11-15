"""The mood bubble: a small floating circle that opens the faces and the voice log (UX v2).

It can be dragged anywhere (it hangs from the right and bottom edges, so it needs no page size).
The ring takes the color of the astronaut's calculated mood, so it also says how things stand.
A tap opens the mood modal; dragging does not.
"""

from __future__ import annotations

import flet as ft

from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, status_color
from crew_self_check.core.contract import System

SIZE = 66


def build_bubble(state: AppState, actions: Actions) -> ft.Control:
    status = state.system_statuses().get(System.MOOD)
    ring = status_color(status.status if status else None)
    right, bottom = state.bubble_offset

    def open_mood(_: object) -> None:
        state.open_mood()
        actions.rerender()

    detector = ft.GestureDetector(
        right=right,
        bottom=bottom,
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=open_mood,
        content=ft.Container(
            width=SIZE,
            height=SIZE,
            border_radius=SIZE // 2,
            alignment=ft.Alignment.CENTER,
            gradient=ft.RadialGradient(
                center=ft.Alignment(-0.4, -0.5), colors=["#7dd3fc", "#6366f1"]
            ),
            border=ft.Border.all(3, ring),
            shadow=ft.BoxShadow(
                blur_radius=26, spread_radius=2, color=ft.Colors.with_opacity(0.55, ring)
            ),
            tooltip=translate("bubble.tip", state.language),
            content=ft.Icon(ft.Icons.FAVORITE, size=30, color="#ffffff"),
        ),
    )

    def drag(event: ft.DragUpdateEvent[ft.GestureDetector]) -> None:
        delta = event.local_delta
        if delta is None:
            return
        state.move_bubble(delta.x, delta.y)
        detector.right, detector.bottom = state.bubble_offset
        actions.refresh()

    detector.on_pan_update = drag
    return detector
