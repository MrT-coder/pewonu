"""Server-rendered HTML of the ground view (G3). No JavaScript, no external requests (offline).

Every value that came from a bundle is escaped. Color is never the only cue: each state also has
its text. Reuses the cabin palette of the astronaut app by value, not by import (D-017).
"""

from __future__ import annotations

from datetime import datetime
from html import escape

from crew_self_check.core.reasons import Language
from crew_self_check.ground import i18n
from crew_self_check.ground.i18n import STRINGS, text
from crew_self_check.ground.view_model import CrewView, ReadingRow, StateRow

_STATUS_COLOR = {
    "ok": "#34d399",
    "watch": "#fbbf24",
    "act": "#fb7185",
    "insufficient_data": "#64748b",
}

_CSS = """
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:linear-gradient(#0b1424,#04070d) fixed;color:#e6edf7;
font:16px/1.5 system-ui,Segoe UI,Roboto,sans-serif}
main{max-width:960px;margin:0 auto;padding:16px}
a{color:#38bdf8}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
h1{font-size:1.4rem;margin:.5rem 0}h2{font-size:1.1rem;margin:1.5rem 0 .5rem}
.banner{background:#0c2a3f;border:1px solid #22314b;border-radius:10px;padding:8px 12px;
color:#bcd}
.card{background:#0f1a2c;border:1px solid #22314b;border-radius:12px;padding:12px 16px;
margin:8px 0}
.muted{color:#8fa0b8}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #22314b;vertical-align:top}
th{color:#8fa0b8;font-weight:600;font-size:.85rem}
.chip{display:inline-flex;align-items:center;gap:6px;font-weight:600}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block}
.table-wrap{overflow-x:auto}
"""


def _page(language: Language, title: str, body: str, refresh: bool = True) -> str:
    other = "en" if language is Language.ES else "es"
    meta = '<meta http-equiv="refresh" content="10">' if refresh else ""
    return (
        f'<!doctype html><html lang="{language.value}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"{meta}<title>{escape(title)}</title><style>{_CSS}</style></head><body><main>"
        f"<header><h1>{escape(STRINGS['app.name'][language])}</h1>"
        f'<a href="?lang={other}">{escape(STRINGS["lang.switch"][language])}</a></header>'
        f'<p class="banner">{escape(STRINGS["banner"][language])}</p>{body}</main></body></html>'
    )


def _s(key: str, language: Language, **params: str) -> str:
    return escape(STRINGS[key][language].format(**params))


def _when(value: datetime | str) -> str:
    return escape(value.strftime("%Y-%m-%d %H:%M UTC") if isinstance(value, datetime) else value)


def _status_chip(status: str, language: Language) -> str:
    color = _STATUS_COLOR.get(status, "#64748b")
    label = escape(text(i18n.STATUS, status, language))
    return f'<span class="chip"><span class="dot" style="background:{color}"></span>{label}</span>'


def _state_rows(states: tuple[StateRow, ...], language: Language) -> str:
    rows = []
    for s in states:
        rows.append(
            "<tr>"
            f"<td>{escape(text(i18n.INDICATOR, s.indicator, language))}</td>"
            f"<td>{escape(text(i18n.ENVIRONMENT, s.environment, language))}</td>"
            f"<td>{_status_chip(s.status, language)}</td>"
            f"<td>{escape(s.reason)}</td>"
            f"<td>{escape(text(i18n.REFERENCE, s.reference, language))}</td>"
            f"<td>{escape(text(i18n.ESCALATION, s.escalation, language))}</td>"
            "</tr>"
        )
    return "".join(rows)


def _reading_rows(readings: tuple[ReadingRow, ...], language: Language) -> str:
    return "".join(
        "<tr>"
        f"<td>{escape(r.label)}</td>"
        f"<td>{escape(r.value)} {escape(r.unit)}</td>"
        f"<td>{escape(text(i18n.ENVIRONMENT, r.environment, language))}</td>"
        f"<td>{escape(r.origin)}</td>"
        f"<td>{escape(text(i18n.METHOD, r.method, language)) if r.method else ''}</td>"
        f"<td>{_when(r.effective)}</td>"
        "</tr>"
        for r in readings
    )


def home_page(
    language: Language,
    crews: tuple[tuple[str, int, datetime], ...],
    delay_minutes: int,
    now: datetime,
    simulated_clock: bool,
) -> str:
    if crews:
        items = "".join(
            f'<div class="card"><strong>{escape(crew)}</strong> · {count} '
            f"{_s('home.packages', language)} · {_s('home.last', language)} {_when(last)} · "
            f'<a href="/crew/{escape(crew)}?lang={language.value}">{_s("home.open", language)}</a>'
            "</div>"
            for crew, count, last in crews
        )
    else:
        items = f'<p class="card muted">{_s("home.nothing", language)}</p>'
    clock = _s("clock.simulated" if simulated_clock else "clock.real", language)
    body = (
        f"<h2>{_s('home.title', language)}</h2>"
        f'<p class="muted">{_s("home.only_shared", language)}</p>{items}'
        f'<p class="muted">{_s("clock.title", language)}: {_when(now)} ({clock}) · '
        f"{_s('delay.title', language)}: {delay_minutes} {_s('delay.minutes', language)}</p>"
    )
    return _page(language, STRINGS["app.name"][language], body)


def crew_page(language: Language, view: CrewView) -> str:
    attention = [s for s in view.states if s.status in ("watch", "act")]
    if attention:
        needs = "".join(
            f"<li>{escape(text(i18n.INDICATOR, s.indicator, language))} · "
            f"{_status_chip(s.status, language)} · "
            f"{escape(text(i18n.ESCALATION, s.escalation, language))}</li>"
            for s in attention
        )
        needs_block = f"<ul>{needs}</ul>"
    else:
        needs_block = f'<p class="muted">{_s("crew.attention_none", language)}</p>'
    heads_state = "".join(
        f"<th>{_s(k, language)}</th>"
        for k in ("col.indicator", "col.where", "col.state", "col.reason", "col.compared")
    )
    heads_state += f"<th>{_s('col.suggestion', language)}</th>"
    heads_read = "".join(
        f"<th>{_s(k, language)}</th>"
        for k in ("col.indicator", "col.value", "col.where", "col.origin", "col.method", "col.when")
    )
    body = (
        f'<p><a href="/?lang={language.value}">← {_s("crew.back", language)}</a></p>'
        f"<h1>{_s('crew.title', language, crew=view.crew_id)}</h1>"
        f'<p class="muted">{view.bundles} {_s("home.packages", language)} · '
        f"{_s('home.last', language)} {_when(view.last_arrival)}</p>"
        f"<h2>{_s('crew.attention', language)}</h2>{needs_block}"
        f"<h2>{_s('crew.states', language)}</h2>"
        f'<div class="table-wrap"><table><tr>{heads_state}</tr>'
        f"{_state_rows(view.states, language)}</table></div>"
        f"<h2>{_s('crew.readings', language)}</h2>"
        f'<div class="table-wrap"><table><tr>{heads_read}</tr>'
        f"{_reading_rows(view.readings, language)}</table></div>"
        f'<p class="card">{_s("crew.limits", language)}</p>'
    )
    return _page(language, f"{view.crew_id} · {STRINGS['app.name'][language]}", body)
