"""Share with the ground team (A10): the astronaut chooses, confirms, and only then it is packed."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import format_reading
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.share_model import DeliveryState, OutboxItem, delivery_state
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.summary_model import Summary
from crew_self_check.astronaut.ui.common import Actions, card
from crew_self_check.core.contract import Indicator
from crew_self_check.core.fhir import ConsentRequired, bundle_json
from crew_self_check.core.reasons import Language


def package_dialog(
    item: OutboxItem, language: Language, close: Callable[[], None]
) -> ft.AlertDialog:
    """The exact FHIR data of a sent package, selectable so it can be read and copied."""
    return ft.AlertDialog(
        title=ft.Text(translate("share.data_title", language)),
        content=ft.Container(
            width=680,
            height=440,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text(
                        bundle_json(item.bundle),
                        selectable=True,
                        size=11,
                        font_family="monospace",
                        color=theme.TEXT,
                    )
                ],
            ),
        ),
        actions=[
            ft.TextButton(content=translate("glossary.close", language), on_click=lambda _: close())
        ],
    )


def build_share_panel(state: AppState, summary: Summary, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    count_text = ft.Text(size=13, color=theme.TEXT)
    confirm = ft.Checkbox(label=say("share.confirm"), value=False)
    send = ft.FilledButton(content=say("share.send"), icon=ft.Icons.SEND, height=44)
    boxes: dict[Indicator, ft.Checkbox] = {}

    def apply() -> None:
        """Bring every control in line with the state (no page update here)."""
        chosen = len(state.share_selection)
        count_text.value = (
            say("share.summary", readings=chosen, states=chosen) if chosen else say("share.nothing")
        )
        confirm.value = state.share_confirmed
        confirm.disabled = chosen == 0
        send.disabled = not (chosen and state.share_confirmed)
        for indicator, box in boxes.items():
            box.value = indicator in state.share_selection

    def sync() -> None:
        """Update in place, so the page keeps its scroll position while the astronaut chooses."""
        apply()
        actions.refresh()

    def toggled(indicator: Indicator) -> None:
        state.toggle_share(indicator)
        sync()

    def shortcut(choose: Callable[[], None]) -> None:
        choose()
        sync()

    def confirmed(event: ft.Event[ft.Checkbox]) -> None:
        state.set_share_confirmed(bool(event.control.value))
        sync()

    def send_now(_: object) -> None:
        try:
            state.send_to_ground()
        except (ConsentRequired, ValueError):
            sync()  # the button is disabled without a confirmation: this is only a safety net
            return
        actions.rerender()

    confirm.on_change = confirmed
    send.on_click = send_now

    for row in summary.rows:
        indicator = row.indicator
        label = (
            f"{translate(f'indicator.{indicator.value}', language)} · "
            f"{format_reading(indicator, row.value, row.unit, language)} · "
            f"{translate(f'summary.short.{row.status.status.value}', language)}"
        )
        boxes[indicator] = ft.Checkbox(
            label=label,
            value=indicator in state.share_selection,
            on_change=lambda _, i=indicator: toggled(i),
        )
    apply()

    lines: list[ft.Control] = [
        ft.Text(say("share.title"), size=16, weight=ft.FontWeight.W_600, color=theme.TEXT),
        ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.LOCK_OUTLINE, size=16, color=theme.GOOD),
                ft.Text(say("share.note"), size=13, color=theme.MUTED, expand=True),
            ],
        ),
        ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
            controls=[
                ft.OutlinedButton(
                    content=say("share.attention"),
                    on_click=lambda _: shortcut(state.select_attention),
                ),
                ft.OutlinedButton(
                    content=say("share.all"), on_click=lambda _: shortcut(state.select_all)
                ),
                ft.TextButton(
                    content=say("share.clear"), on_click=lambda _: shortcut(state.clear_share)
                ),
            ],
        ),
        ft.Column(spacing=0, controls=list(boxes.values())),
        count_text,
        confirm,
        send,
        ft.Divider(height=8, color=theme.CARD_BORDER),
        *_sent(state, actions),
    ]
    return card(ft.Column(spacing=10, controls=lines))


def _sent_line(say: Callable[..., str], item: OutboxItem) -> str:
    if item.voices and not item.readings:
        return say("share.sent_voice", label=item.day_label, voices=item.voices)
    return say("share.sent_line", label=item.day_label, readings=item.readings, states=item.states)


def _sent(state: AppState, actions: Actions) -> list[ft.Control]:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    out: list[ft.Control] = [
        ft.Text(say("share.sent_title"), size=15, weight=ft.FontWeight.W_600, color=theme.TEXT)
    ]
    items = state.own_outbox()
    if not items:
        out.append(ft.Text(say("share.sent_empty"), size=13, color=theme.MUTED))
    now = state.journey_time()
    for item in items:
        arrived = delivery_state(item, now) is DeliveryState.DELIVERED
        minutes = max(0, round((item.arrives_at - now).total_seconds() / 60))
        if item in state.unsent_to_ground():
            status = say("share.waiting_ground")
        elif arrived:
            status = say("share.delivered_linked" if state.ground_linked else "share.delivered")
        else:
            status = say("share.in_transit", minutes=minutes)
        out.append(
            ft.Container(
                padding=ft.Padding.symmetric(vertical=4),
                content=ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            _sent_line(say, item),
                            size=13,
                            color=theme.TEXT,
                        ),
                        ft.Text(status, size=12, color=theme.GOOD if arrived else theme.GOLD),
                        ft.TextButton(
                            content=say("share.show_data"),
                            icon=ft.Icons.CODE,
                            on_click=lambda _, i=item: actions.show_package(i),
                        ),
                    ],
                ),
            )
        )
    note = "share.linked_note" if state.ground_linked else "share.sim_note"
    out.append(ft.Text(say(note), size=11, color=theme.MUTED))
    return out
