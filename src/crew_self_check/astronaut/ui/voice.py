"""The voice log screens: a question, the recording, and what the numbers say (T2, D-028)."""

from __future__ import annotations

import asyncio
import time

import flet as ft

from crew_self_check.astronaut import theme
from crew_self_check.astronaut.i18n import translate
from crew_self_check.astronaut.state import AppState, VoiceResult, VoiceStage
from crew_self_check.astronaut.ui.common import Actions, card
from crew_self_check.core.voice_baseline import MIN_NOTES, VoiceComparison, VoiceLevel

_TICK_SECONDS = 0.2


def _text(value: str, size: int = 13, color: str = theme.TEXT, bold: bool = False) -> ft.Text:
    weight = ft.FontWeight.W_600 if bold else ft.FontWeight.NORMAL
    return ft.Text(value, size=size, color=color, weight=weight)


def build_voice(state: AppState, actions: Actions) -> ft.Control:
    if state.voice_stage is VoiceStage.RECORDING:
        return _recording(state, actions)
    if state.voice_stage is VoiceStage.RESULT and state.voice_result is not None:
        return _result(state, actions, state.voice_result)
    return _prompt(state, actions)


def _leave(state: AppState, actions: Actions) -> ft.Control:
    def back(_: object) -> None:
        state.cancel_voice()
        actions.rerender()

    return ft.TextButton(
        content=translate("pulse.leave", state.language), icon=ft.Icons.CLOSE, on_click=back
    )


def _prompt(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    def start(_: object) -> None:
        state.start_voice()
        actions.rerender()

    def another(_: object) -> None:
        state.new_voice_prompt()
        actions.rerender()

    def sample(_: object) -> None:
        state.use_synthetic_voice()
        actions.rerender()

    controls: list[ft.Control] = [
        _text(say("voice.intro"), 14, theme.MUTED),
        ft.Container(
            padding=20,
            border_radius=16,
            bgcolor=theme.ACCENT_SOFT,
            content=_text(say(state.voice_prompt), 22, theme.TEXT, True),
        ),
    ]
    if state.voice_available():
        if state.voice_synthetic():
            controls.append(_text(say("voice.synthetic"), 12, theme.GOLD))
        controls.append(
            ft.Row(
                spacing=12,
                controls=[
                    ft.FilledButton(
                        content=say("voice.start"), icon=ft.Icons.MIC, height=48, on_click=start
                    ),
                    ft.OutlinedButton(
                        content=say("voice.another"), icon=ft.Icons.SHUFFLE, on_click=another
                    ),
                ],
            )
        )
    else:
        controls += [
            _text(say("voice.no_mic"), 13, theme.GOLD),
            ft.OutlinedButton(
                content=say("voice.use_sample"), icon=ft.Icons.GRAPHIC_EQ, on_click=sample
            ),
        ]
    return ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        say("voice.title"), size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT
                    ),
                    _leave(state, actions),
                ],
            ),
            card(ft.Column(spacing=14, controls=controls)),
        ],
    )


def _recording(state: AppState, actions: Actions) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    started = time.monotonic()
    meter = ft.ProgressBar(value=0.0, color=theme.ACCENT, bgcolor=theme.CARD_BORDER, height=10)
    clock = _text(say("voice.elapsed", seconds=0), 14, theme.MUTED)

    def stop(_: object) -> None:
        state.stop_voice()
        actions.rerender()

    state.voice_tick += 1
    mine = state.voice_tick

    async def tick() -> None:
        # one loop per screen: a newer render takes over, leaving the stage ends it
        while state.voice_stage is VoiceStage.RECORDING and state.voice_tick == mine:
            meter.value = state.voice_level()
            clock.value = say("voice.elapsed", seconds=int(time.monotonic() - started))
            actions.refresh()
            await asyncio.sleep(_TICK_SECONDS)

    panel = card(
        ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.MIC, size=48, color=theme.ACCENT),
                _text(say(state.voice_prompt), 18, theme.TEXT, True),
                _text(say("voice.listening"), 14, theme.GOOD),
                meter,
                clock,
                ft.FilledButton(
                    content=say("voice.stop"), icon=ft.Icons.STOP, height=48, on_click=stop
                ),
            ],
        ),
        border_color=theme.ACCENT,
    )
    actions.run_task(tick)
    return ft.Column(
        spacing=16,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        say("voice.title"), size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT
                    ),
                    _leave(state, actions),
                ],
            ),
            panel,
        ],
    )


def _deviation_rows(comparison: VoiceComparison, state: AppState) -> list[ft.Control]:
    language = state.language
    rows: list[ft.Control] = []
    for item in comparison.deviations:
        name = translate(f"voice.feature.{item.name}", language)
        if item.direction is None:
            verdict, color = translate("voice.same", language), theme.GOOD
        else:
            verdict = translate(f"voice.dir.{item.name}.{item.direction}", language)
            color = theme.GOLD
        rows.append(
            ft.Row(
                spacing=12,
                controls=[
                    ft.Container(width=170, content=_text(name, 13, theme.TEXT)),
                    _text(verdict, 13, color, True),
                ],
            )
        )
    return rows


def _result(state: AppState, actions: Actions, result: VoiceResult) -> ft.Control:
    language = state.language

    def say(key: str, **params: object) -> str:
        return translate(key, language, **params)

    def again(_: object) -> None:
        state.new_voice_prompt()
        state.voice_result = None
        state.open_voice()
        actions.rerender()

    body: list[ft.Control] = []
    if not result.saved:
        body += [
            _text(say(f"voice.problem.{code}"), 14, theme.GOLD) for code in result.analysis.problems
        ]
    elif result.comparison is not None:
        comparison = result.comparison
        if comparison.level is VoiceLevel.BUILDING:
            body.append(
                _text(
                    say("voice.building", n=comparison.n_previous + 1, needed=MIN_NOTES + 1),
                    14,
                    theme.TEXT,
                )
            )
        else:
            headline = (
                "voice.level.different"
                if comparison.level is VoiceLevel.DIFFERENT
                else "voice.level.usual"
            )
            color = theme.GOLD if comparison.level is VoiceLevel.DIFFERENT else theme.GOOD
            body += [_text(say(headline), 16, color, True)]
            if comparison.reference == "transition" and comparison.baseline_environment is not None:
                previous = translate(f"env.{comparison.baseline_environment.value}.short", language)
                body.append(
                    _text(say("voice.reference.transition", previous=previous), 12, theme.MUTED)
                )
            else:
                body.append(_text(say("voice.reference.personal"), 12, theme.MUTED))
            body += _deviation_rows(comparison, state)
        body += [
            ft.Divider(height=6, color=theme.CARD_BORDER),
            _text(say("voice.discarded"), 12, theme.GOOD),
            _text(say("voice.shared" if result.shared else "voice.not_shared"), 12, theme.MUTED),
            _text(say("voice.not_a_diagnosis"), 12, theme.MUTED),
        ]
        if state.voice_synthetic():
            body.append(_text(say("voice.synthetic"), 12, theme.GOLD))
    return ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        say("voice.result_title"),
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=theme.TEXT,
                    ),
                    _leave(state, actions),
                ],
            ),
            card(ft.Column(spacing=10, controls=body)),
            ft.FilledButton(
                content=say("voice.again"), icon=ft.Icons.MIC, height=46, on_click=again
            ),
        ],
    )
