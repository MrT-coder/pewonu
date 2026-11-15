"""The daily check-in: today the pulse mission (manual pulse, D-014, D-021)."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.body_model import reference_text, status_label_key
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.mood import MOOD_LEVELS
from crew_self_check.astronaut.pulse_guidance import outside_band, pulse_guidance
from crew_self_check.astronaut.pulse_mission import INTERVALS, PulseMission, Station
from crew_self_check.astronaut.state import AppState
from crew_self_check.astronaut.ui.common import Actions, card, status_color
from crew_self_check.core.contract import Escalation, Status

Say = Callable[..., str]

_STATIONS = (Station.REST, Station.LOCATE, Station.PRESSURE, Station.COUNT)
_TICK_SECONDS = 0.25
_MAX_DOTS = 150  # an implausible count must not draw thousands of hearts


def _station_number(station: Station) -> int:
    return 4 if station is Station.RESULT else _STATIONS.index(station) + 1


def build_checkin(state: AppState, actions: Actions) -> ft.Control:
    if state.pulse is None:
        return _hub(state, actions)
    return _mission(state, state.pulse, actions)


# --- the hub: what can be done today --------------------------------------------------------------


def _hub(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    last = state.last_pulse()
    pulse_lines: list[ft.Control] = [
        ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=30, color=theme.ACCENT),
        ft.Text(say("pulse.title"), size=17, weight=ft.FontWeight.W_600, color=theme.TEXT),
        ft.Text(say("pulse.hub_body"), size=13, color=theme.MUTED),
    ]
    if last is not None:
        pulse_lines.append(
            ft.Text(say("pulse.last", bpm=round(last.value)), size=13, color=theme.GOOD)
        )
    pulse_lines.append(
        ft.FilledButton(
            content=say("pulse.start"),
            icon=ft.Icons.PLAY_ARROW,
            height=44,
            on_click=lambda _: _start(state, actions),
        )
    )

    mood_card = _mood_card(state, actions, say)
    return ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(say("checkin.subtitle"), size=14, color=theme.MUTED),
            ft.ResponsiveRow(
                spacing=14,
                run_spacing=14,
                controls=[
                    ft.Container(
                        content=card(ft.Column(spacing=10, controls=pulse_lines)),
                        col={"xs": 12, "md": 6},
                    ),
                    ft.Container(content=mood_card, col={"xs": 12, "md": 6}),
                ],
            ),
        ],
    )


_FACES = {
    1: ft.Icons.SENTIMENT_VERY_DISSATISFIED,
    2: ft.Icons.SENTIMENT_DISSATISFIED,
    3: ft.Icons.SENTIMENT_NEUTRAL,
    4: ft.Icons.SENTIMENT_SATISFIED,
    5: ft.Icons.SENTIMENT_VERY_SATISFIED,
}


def _mood_card(state: AppState, actions: Actions, say: Say) -> ft.Control:
    chosen = state.mood_choice

    def face(level: int) -> ft.Control:
        selected = chosen == level

        def pick(_: object) -> None:
            state.choose_mood(level)
            actions.rerender()

        return ft.Container(
            width=86,
            padding=ft.Padding.symmetric(vertical=10),
            border_radius=14,
            ink=True,
            on_click=pick,
            bgcolor=theme.ACCENT_SOFT if selected else None,
            border=ft.Border.all(
                2 if selected else 1, theme.ACCENT if selected else theme.CARD_BORDER
            ),
            content=ft.Column(
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        _FACES[level], size=38, color=theme.ACCENT if selected else theme.MUTED
                    ),
                    ft.Text(
                        say(f"mood.level.{level}"),
                        size=12,
                        color=theme.TEXT if selected else theme.MUTED,
                    ),
                ],
            ),
        )

    def save(_: object) -> None:
        state.save_mood()
        actions.rerender()

    last = state.last_mood()
    lines: list[ft.Control] = [
        ft.Icon(ft.Icons.SENTIMENT_SATISFIED_OUTLINED, size=30, color=theme.ACCENT),
        ft.Text(say("checkin.mood.title"), size=17, weight=ft.FontWeight.W_600, color=theme.TEXT),
        ft.Text(say("mood.prompt"), size=13, color=theme.MUTED),
        ft.Row(wrap=True, spacing=8, run_spacing=8, controls=[face(n) for n in MOOD_LEVELS]),
    ]
    if last is not None:
        lines.append(
            ft.Text(
                say("mood.last", label=say(f"mood.level.{round(last.value)}")),
                size=13,
                color=theme.GOOD,
            )
        )
    lines += [
        ft.FilledButton(
            content=say("mood.save"),
            icon=ft.Icons.SAVE_OUTLINED,
            height=44,
            disabled=chosen is None,
            on_click=save,
        ),
        ft.Text(say("mood.note"), size=11, color=theme.MUTED),
    ]
    return card(ft.Column(spacing=10, controls=lines))


def _start(state: AppState, actions: Actions) -> None:
    state.start_pulse()
    actions.rerender()


# --- the mission ----------------------------------------------------------------------------------


def _mission(state: AppState, mission: PulseMission, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    number = _station_number(mission.station)
    key = _STATIONS[number - 1].value  # rest, locate, pressure, count

    def leave(_: object) -> None:
        state.cancel_pulse()
        actions.rerender()

    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Row(
                spacing=10,
                controls=[
                    ft.Text(
                        say("pulse.title"), size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT
                    ),
                    _points_chip(say("pulse.points", points=mission.points)),
                ],
            ),
            ft.TextButton(content=say("pulse.leave"), icon=ft.Icons.CLOSE, on_click=leave),
        ],
    )

    illustration = ft.Container(
        width=300,
        height=436,
        border_radius=16,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        border=ft.Border.all(1, theme.CARD_BORDER),
        content=ft.Image(
            src=f"pulse/{language.value}-step{number}.jpg",
            fit=ft.BoxFit.COVER,
            semantics_label=say(f"pulse.{key}.title"),
        ),
    )

    if mission.station is Station.RESULT:
        action: ft.Control = _result(state, mission, actions, say)
        title, body = say("pulse.result_title"), ""
    else:
        title = say(f"pulse.{key}.title")
        body = (
            say("pulse.count.body", seconds=mission.interval)
            if key == "count"
            else say(f"pulse.{key}.body")
        )
        action = _station_action(state, mission, actions, say)

    text_column = ft.Column(
        expand=True,
        spacing=12,
        controls=[
            ft.Text(say("pulse.station", n=number), size=12, color=theme.ACCENT),
            ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=theme.TEXT),
            *([ft.Text(body, size=15, color=theme.MUTED)] if body else []),
            action,
        ],
    )

    footer = ft.Text(
        f"{say('pulse.source')}  {say('pulse.illustrations')}", size=11, color=theme.MUTED
    )
    return ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            _rail(mission, say),
            ft.Row(
                spacing=24,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[illustration, text_column],
            ),
            footer,
        ],
    )


def _points_chip(text: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=5),
        border_radius=20,
        bgcolor=theme.ACCENT_SOFT,
        content=ft.Row(
            tight=True,
            spacing=6,
            controls=[
                ft.Icon(ft.Icons.STAR, size=16, color=theme.GOLD),
                ft.Text(text, size=13, color=theme.TEXT),
            ],
        ),
    )


def _rail(mission: PulseMission, say: Say) -> ft.Control:
    current = _station_number(mission.station)
    chips: list[ft.Control] = []
    for index, station in enumerate(_STATIONS, start=1):
        done = index < current or (
            mission.station is Station.RESULT and index == 4 and (mission.earned_badge)
        )
        active = index == current and not done
        color = theme.GOOD if done else theme.ACCENT if active else theme.MUTED
        chips.append(
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
                border=ft.Border.all(1, color),
                content=ft.Row(
                    tight=True,
                    spacing=6,
                    controls=[
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE if done else ft.Icons.RADIO_BUTTON_UNCHECKED,
                            size=16,
                            color=color,
                        ),
                        ft.Text(say(f"pulse.{station.value}.title"), size=12, color=color),
                    ],
                ),
            )
        )
    return ft.Row(wrap=True, spacing=8, run_spacing=8, controls=chips)


def _station_action(
    state: AppState, mission: PulseMission, actions: Actions, say: Say
) -> ft.Control:
    if mission.station is not Station.COUNT:

        def confirm(_: object) -> None:
            mission.complete_station()
            actions.rerender()

        return ft.FilledButton(
            content=say("pulse.next"), icon=ft.Icons.ARROW_FORWARD, height=46, on_click=confirm
        )
    return _count_area(state, mission, actions, say)


# --- the count ------------------------------------------------------------------------------------


def _count_area(state: AppState, mission: PulseMission, actions: Actions, say: Say) -> ft.Control:
    """Count with the fingers on the wrist, then type the number. Nothing to tap while counting."""
    timer_text = ft.Text("", size=14, color=theme.MUTED)
    timer_running = False

    def calculate(_: object) -> None:
        typed = (field.value or "").strip()
        if not (typed.isascii() and typed.isdigit()):
            field.error = say("pulse.beats_error")
            actions.refresh()
            return
        mission.submit_count(int(typed))
        actions.rerender()

    field = ft.TextField(
        label=say("pulse.beats_label", seconds=mission.interval),
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=3,
        width=320,
        border_radius=12,
        on_submit=calculate,
    )

    def choose(event: ft.Event[ft.SegmentedButton]) -> None:
        mission.set_interval(int(next(iter(event.control.selected))))
        actions.rerender()

    async def run_timer(_: object) -> None:
        # Optional helper: a countdown to watch while the fingers stay on the wrist.
        nonlocal timer_running
        if timer_running:
            return
        timer_running = True
        end = time.monotonic() + mission.interval
        while state.pulse is mission and mission.station is Station.COUNT:
            left = end - time.monotonic()
            if left <= 0:
                timer_text.value = say("pulse.timer_done")
                actions.refresh()
                break
            timer_text.value = say("pulse.seconds_left", s=int(left) + 1)
            actions.refresh()
            await asyncio.sleep(_TICK_SECONDS)
        timer_running = False

    return ft.Column(
        spacing=14,
        controls=[
            ft.Text(say("pulse.interval"), size=13, color=theme.MUTED),
            ft.SegmentedButton(
                selected=[str(mission.interval)],
                allow_empty_selection=False,
                segments=[
                    ft.Segment(value=str(seconds), label=ft.Text(say(f"pulse.interval_{seconds}")))
                    for seconds in INTERVALS
                ],
                on_change=choose,
            ),
            ft.OutlinedButton(
                content=say("pulse.timer_start", seconds=mission.interval),
                icon=ft.Icons.TIMER_OUTLINED,
                on_click=run_timer,
            ),
            timer_text,
            field,
            ft.FilledButton(
                content=say("pulse.calculate"),
                icon=ft.Icons.CALCULATE,
                height=46,
                on_click=calculate,
            ),
        ],
    )


# --- the result -----------------------------------------------------------------------------------


def _guidance(state: AppState, say: Say) -> list[ft.Control]:
    """What the count means for this person and what to do next (A5), before it is saved."""
    resolution = state.preview_pulse()
    if resolution is None:
        return []
    status = resolution.status
    outside = outside_band(resolution)
    guidance = pulse_guidance(status.status, outside)
    one_off = status.status is Status.OK and outside
    color = theme.GOLD if one_off else status_color(status.status)
    label = say("pulse.outside_one") if one_off else say(status_label_key(status.status))
    meaning: list[ft.Control] = [
        ft.Text(say("pulse.meaning_title"), size=15, weight=ft.FontWeight.W_600, color=theme.TEXT),
        ft.Row(
            spacing=8,
            controls=[
                ft.Container(width=14, height=14, border_radius=7, bgcolor=color),
                ft.Text(label, size=15, weight=ft.FontWeight.W_600, color=theme.TEXT),
            ],
        ),
    ]
    if status.baseline is not None:
        meaning.append(
            ft.Text(
                say(
                    "pulse.band",
                    low=round(status.baseline.low),
                    high=round(status.baseline.high),
                    days=status.baseline.n_days,
                ),
                size=13,
                color=theme.TEXT,
            )
        )
    if not one_off:  # for one count outside the band the reason would read "within your range"
        meaning.append(ft.Text(resolution.reason.text(state.language), size=13, color=theme.MUTED))
    meaning.append(ft.Text(reference_text(status, state.language), size=12, color=theme.MUTED))

    todo: list[ft.Control] = [
        ft.Text(say("pulse.todo_title"), size=15, weight=ft.FontWeight.W_600, color=theme.TEXT)
    ]
    todo += [
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=16, color=theme.ACCENT),
                ft.Text(say(step), size=13, color=theme.TEXT, expand=True),
            ],
        )
        for step in guidance.steps
    ]
    if guidance.escalation is not Escalation.SELF_CARE:
        todo += [
            ft.Text(say("pulse.todo.tell"), size=13, weight=ft.FontWeight.W_600, color=theme.GOLD),
            ft.Text(say(f"escalation.{guidance.escalation.value}"), size=13, color=theme.TEXT),
        ]
    todo.append(ft.Text(say("pulse.source"), size=11, color=theme.MUTED))
    return [
        card(ft.Column(spacing=6, controls=meaning), border_color=color),
        card(ft.Column(spacing=8, controls=todo)),
    ]


def _result(state: AppState, mission: PulseMission, actions: Actions, say: Say) -> ft.Control:
    result = mission.result
    assert result is not None
    formula = say(f"pulse.formula_{result.interval}", beats=result.beats, bpm=result.bpm)
    dots = ft.Container(
        width=480,
        content=ft.Row(
            wrap=True,
            spacing=4,
            run_spacing=4,
            controls=[ft.Icon(ft.Icons.FAVORITE, size=14, color=theme.ACCENT)]
            * min(result.beats, _MAX_DOTS),
        ),
    )
    summary: list[ft.Control] = [
        ft.Text(formula, size=26, weight=ft.FontWeight.BOLD, color=theme.TEXT),
        dots,
    ]

    if not result.valid:

        def again(_: object) -> None:
            mission.retry()
            actions.rerender()

        summary += [
            ft.Text(say("pulse.recount_body"), size=14, color=theme.GOLD),
            ft.FilledButton(
                content=say("pulse.recount"), icon=ft.Icons.REPLAY, height=46, on_click=again
            ),
        ]
        return ft.Column(spacing=14, controls=summary)

    def save(_: object) -> None:
        state.save_pulse()
        actions.rerender()

    summary += [
        *_guidance(state, say),
        card(
            ft.Row(
                spacing=14,
                controls=[
                    ft.Icon(ft.Icons.EMOJI_EVENTS, size=34, color=theme.GOLD),
                    ft.Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            ft.Text(
                                say("pulse.badge"),
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=theme.TEXT,
                            ),
                            ft.Text(say("pulse.badge_note"), size=12, color=theme.MUTED),
                            ft.Text(
                                say("pulse.points", points=mission.points),
                                size=13,
                                color=theme.GOLD,
                            ),
                            ft.Text(say("pulse.points_note"), size=12, color=theme.MUTED),
                        ],
                    ),
                ],
            ),
            border_color=theme.GOLD,
        ),
        ft.FilledButton(
            content=say("pulse.save"), icon=ft.Icons.SAVE_OUTLINED, height=46, on_click=save
        ),
    ]
    return ft.Column(spacing=14, controls=summary)
