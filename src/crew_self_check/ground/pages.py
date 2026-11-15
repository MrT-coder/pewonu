"""Server-rendered HTML of the ground view (G3, T3). No JavaScript, no external requests (offline).

Every value that came from a bundle is escaped. Color is never the only cue: each state also has
its text, and each chart has a text alternative. Reuses the cabin palette of the astronaut app by
value, not by import (D-017). The console leads with what the astronaut's own app flagged; it does
not compute a state of its own and it never diagnoses.
"""

from __future__ import annotations

from datetime import datetime
from html import escape

from crew_self_check.core.reasons import Language
from crew_self_check.ground import i18n
from crew_self_check.ground.i18n import STRINGS, text
from crew_self_check.ground.view_model import (
    CrewView,
    ReadingRow,
    StateRow,
    VoiceRow,
    attention_rows,
    system_levels,
    top_escalation,
    worst_status,
)

_UNIT = {"C": "°C"}  # the bundle carries the plain UCUM-style unit

_STATUS_COLOR = {
    "ok": "#34d399",
    "watch": "#fbbf24",
    "act": "#fb7185",
    "insufficient_data": "#64748b",
}
_SYSTEM_ORDER = ("cardiovascular", "vestibular", "sleep_brain", "mood", "immune")

_CSS = """
:root{color-scheme:dark}
*{box-sizing:border-box}
html{background:#04070d}
body{margin:0;min-height:100vh;
background:radial-gradient(1100px 500px at 15% -10%,#12294a,#04070d);
color:#e6edf7;font:16px/1.5 system-ui,Segoe UI,Roboto,sans-serif}
main{max-width:1040px;margin:0 auto;padding:20px 16px 48px}
a{color:#38bdf8;display:inline-block;min-height:24px;min-width:24px;padding:2px 0}
nav{display:flex;gap:16px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
h1{font-size:1.5rem;margin:.6rem 0 .2rem}
.brand{font-size:1.1rem;font-weight:700;letter-spacing:.2px}
h2{font-size:1.05rem;margin:1.6rem 0 .6rem;color:#cfe3f7}
.banner{background:#0c2a3f;border:1px solid #22314b;border-radius:10px;padding:8px 12px;color:#bcd}
.card{background:#0f1a2c;border:1px solid #22314b;border-radius:14px;
padding:14px 18px;margin:10px 0}
.crew{border-left:6px solid var(--c,#64748b)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.muted{color:#8fa0b8}.small{font-size:.85rem}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.pill{display:inline-flex;align-items:center;gap:6px;border:1px solid #22314b;border-radius:999px;
padding:3px 10px;font-size:.85rem;background:#0b1424}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #22314b;vertical-align:top}
th{color:#8fa0b8;font-weight:600;font-size:.85rem}
.chip{display:inline-flex;align-items:center;gap:6px;font-weight:600}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block;flex:none}
.table-wrap{overflow-x:auto}
.spark{display:block;width:100%;height:auto}
.head{display:flex;justify-content:space-between;gap:8px;align-items:baseline;flex-wrap:wrap}
.suggest{background:#2a1a0c;border:1px solid #5b3b14;border-radius:10px;
padding:6px 10px;margin-top:8px}
.suggest.act{background:#2a0f16;border-color:#6b1f2d}
"""


def _page(language: Language, title: str, body: str) -> str:
    """No timed refresh (WCAG 2.2.1): the person refreshes with the visible link."""
    other = "en" if language is Language.ES else "es"
    return (
        f'<!doctype html><html lang="{language.value}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<link rel="icon" href="data:,">'
        f"<title>{escape(title)}</title><style>{_CSS}</style></head><body><main>"
        f'<header><div class="brand">{escape(STRINGS["app.name"][language])}</div><nav>'
        f'<a href="?lang={language.value}">{escape(STRINGS["action.refresh"][language])}</a>'
        f'<a href="?lang={other}">{escape(STRINGS["lang.switch"][language])}</a></nav></header>'
        f'<p class="banner">{escape(STRINGS["banner"][language])}</p>{body}</main></body></html>'
    )


def _s(key: str, language: Language, **params: str) -> str:
    return escape(STRINGS[key][language].format(**params))


def _scroll(label: str, table: str) -> str:
    """A table that scrolls sideways on a phone must take focus and have a name (WCAG 2.1.1)."""
    return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}">{table}</div>'


def _packages(count: int, language: Language) -> str:
    key = "home.package_one" if count == 1 else "home.packages"
    return f"{count} {_s(key, language)}"


def _when(value: datetime | str) -> str:
    moment: datetime
    if isinstance(value, str):
        try:
            moment = datetime.fromisoformat(value)
        except ValueError:
            return escape(value)
    else:
        moment = value
    return escape(moment.strftime("%Y-%m-%d %H:%M UTC"))


def _status_chip(status: str, language: Language) -> str:
    color = _STATUS_COLOR.get(status, "#64748b")
    label = escape(text(i18n.STATUS, status, language))
    return f'<span class="chip"><span class="dot" style="background:{color}"></span>{label}</span>'


def _indicator(row: StateRow, language: Language) -> str:
    name = text(i18n.INDICATOR, row.indicator, language)
    place = text(i18n.ENVIRONMENT, row.environment, language)
    return f"{name} · {place}" if row.environment else name


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


# --- trends ---------------------------------------------------------------------------------------


def _spark(row: StateRow, language: Language) -> str:
    """The recent readings as a small line, with the person's usual band behind it."""
    if not row.trend:
        return ""
    width, height, pad = 240, 64, 8
    values = [v for _, v in row.trend]
    low, high = row.low, row.high
    edges = [*values, *([low, high] if low is not None and high is not None else [])]
    vmin, vmax = min(edges), max(edges)
    span = (vmax - vmin) or 1.0

    def y(v: float) -> float:
        return height - pad - (v - vmin) / span * (height - 2 * pad)

    def x(i: int) -> float:
        return width / 2 if len(values) == 1 else pad + i * (width - 2 * pad) / (len(values) - 1)

    color = _STATUS_COLOR.get(row.status, "#64748b")
    band = ""
    caption = _s("trend.no_band", language)
    if low is not None and high is not None:
        band = (
            f'<rect x="0" y="{y(high):.1f}" width="{width}" '
            f'height="{max(y(low) - y(high), 2):.1f}" '
            'fill="#38bdf8" opacity="0.18"/>'
        )
        caption = _s("trend.band", language, low=_number(low), high=_number(high))
    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
    dots = "".join(
        f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3" fill="{color}"/>'
        for i, v in enumerate(values)
    )
    name = text(i18n.INDICATOR, row.indicator, language)
    unit = _UNIT.get(row.unit, row.unit)
    label = escape(
        f"{name}: {_number(values[0])} → {_number(values[-1])} {unit}. "
        + STRINGS["trend.band" if low is not None and high is not None else "trend.no_band"][
            language
        ].format(
            low=_number(low) if low is not None else "",
            high=_number(high) if high is not None else "",
        )
    )
    return (
        f'<svg class="spark" viewBox="0 0 {width} {height}" role="img" aria-label="{label}">'
        f'{band}<polyline fill="none" stroke="{color}" stroke-width="2" '
        f'points="{points}"/>{dots}</svg>'
        f'<div class="muted small">{caption}</div>'
    )


def _trends(states: tuple[StateRow, ...], language: Language) -> str:
    cards = []
    for row in states:
        chart = _spark(row, language)
        if not chart:
            continue
        cards.append(
            '<div class="card">'
            f'<div class="head"><strong>{escape(_indicator(row, language))}</strong>'
            f"{_status_chip(row.status, language)}</div>{chart}</div>"
        )
    if not cards:
        return ""
    return f'<h2>{_s("crew.trends", language)}</h2><div class="grid">{"".join(cards)}</div>'


# --- tables ---------------------------------------------------------------------------------------


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


def _reading_name(reading: ReadingRow, language: Language) -> str:
    if reading.indicator:
        return text(i18n.INDICATOR, reading.indicator, language)
    return reading.label


def _reading_rows(readings: tuple[ReadingRow, ...], language: Language) -> str:
    return "".join(
        "<tr>"
        f"<td>{escape(_reading_name(r, language))}</td>"
        f"<td>{escape(r.value)} {escape(_UNIT.get(r.unit, r.unit))}</td>"
        f"<td>{escape(text(i18n.ENVIRONMENT, r.environment, language))}</td>"
        f"<td>{escape(text(i18n.ORIGIN, r.origin, language))}</td>"
        f"<td>{escape(text(i18n.METHOD, r.method, language)) if r.method else ''}</td>"
        f"<td>{_when(r.effective)}</td>"
        "</tr>"
        for r in readings
    )


def _voice_section(rows: tuple[VoiceRow, ...], language: Language) -> str:
    if not rows:
        return ""
    body = []
    for row in rows:
        if row.level == "different" and row.changed:
            what = ", ".join(
                text(i18n.VOICE_DIRECTION, f"{name}.{direction}", language)
                for name, direction in row.changed
            )
        else:
            what = text(i18n.VOICE_LEVEL, row.level, language)
        reference = text(i18n.REFERENCE, row.reference, language)
        if row.baseline_environment:
            reference += f" ({text(i18n.ENVIRONMENT, row.baseline_environment, language)})"
        body.append(
            "<tr>"
            f"<td>{_when(row.effective)}</td>"
            f"<td>{escape(text(i18n.ENVIRONMENT, row.environment, language))}</td>"
            f"<td>{escape(text(i18n.VOICE_LEVEL, row.level, language))}</td>"
            f"<td>{escape(what)}</td>"
            f"<td>{escape(reference)}</td>"
            "</tr>"
        )
    heads = "".join(
        f"<th>{_s(key, language)}</th>"
        for key in ("col.when", "col.where", "col.state", "col.voice_change", "col.compared")
    )
    table = _scroll(_s("crew.voice", language), f"<table><tr>{heads}</tr>{''.join(body)}</table>")
    return (
        f"<h2>{_s('crew.voice', language)}</h2>"
        f'<p class="muted">{_s("crew.voice_note", language)}</p>{table}'
    )


# --- shared blocks --------------------------------------------------------------------------------


def _system_pills(view: CrewView, language: Language) -> str:
    levels = system_levels(view)
    pills = []
    for system in _SYSTEM_ORDER:
        status = levels.get(system)
        if status is None:
            continue
        color = _STATUS_COLOR.get(status, "#64748b")
        pills.append(
            f'<span class="pill"><span class="dot" style="background:{color}"></span>'
            f"{escape(text(i18n.SYSTEM, system, language))} · "
            f'<span class="muted">{escape(text(i18n.STATUS_SHORT, status, language))}</span></span>'
        )
    return f'<div class="row">{"".join(pills)}</div>' if pills else ""


def _attention_block(view: CrewView, language: Language, reasons: bool = True) -> str:
    flagged = attention_rows(view)
    if not flagged:
        return f'<p class="muted">{_s("crew.attention_none", language)}</p>'
    items = "".join(
        f"<li>{escape(text(i18n.INDICATOR, s.indicator, language))} · "
        f"{_status_chip(s.status, language)}"
        + (f' · <span class="muted">{escape(s.reason)}</span>' if reasons else "")
        + "</li>"
        for s in flagged
    )
    suggestion = top_escalation(view)
    tone = " act" if worst_status(view) == "act" else ""
    return (
        f"<ul>{items}</ul>"
        f'<div class="suggest{tone}"><strong>{_s("home.suggestion", language)}:</strong> '
        f"{escape(text(i18n.ESCALATION, suggestion, language))}</div>"
    )


def _voice_chip(view: CrewView, language: Language) -> str:
    if not view.voice:
        return ""
    last = view.voice[-1]
    color = (
        "#fbbf24"
        if last.level == "different"
        else "#34d399"
        if last.level == "usual"
        else "#64748b"
    )
    return (
        f'<span class="pill"><span class="dot" style="background:{color}"></span>'
        f"{_s('crew.voice', language)} · "
        f'<span class="muted">{escape(text(i18n.VOICE_LEVEL, last.level, language))}</span></span>'
    )


def home_page(
    language: Language,
    views: tuple[CrewView, ...],
    delay_minutes: int,
    now: datetime,
    simulated_clock: bool,
) -> str:
    if views:
        cards = []
        for view in views:
            color = _STATUS_COLOR.get(worst_status(view), "#64748b")
            link = f"/crew/{escape(view.crew_id)}?lang={language.value}"
            cards.append(
                f'<div class="card crew" style="--c:{color}">'
                '<div class="head"><strong style="font-size:1.15rem">'
                f"{escape(view.crew_id)}</strong>"
                f'<span class="muted small">{_packages(view.bundles, language)} · '
                f"{_s('home.last', language)} {_when(view.last_arrival)}</span></div>"
                f'<h2 style="margin:.7rem 0 .3rem">{_s("crew.attention", language)}</h2>'
                f"{_attention_block(view, language, reasons=False)}"
                f'<div class="row" style="margin-top:10px">{_system_pills(view, language)}'
                f"{_voice_chip(view, language)}</div>"
                f'<p><a href="{link}">{_s("home.open", language)} →</a></p></div>'
            )
        items = f'<div class="grid">{"".join(cards)}</div>'
    else:
        items = f'<p class="card muted">{_s("home.nothing", language)}</p>'
    clock = _s("clock.simulated" if simulated_clock else "clock.real", language)
    body = (
        f"<h1>{_s('home.title', language)}</h1>"
        f'<p class="muted">{_s("home.only_shared", language)}</p>{items}'
        f'<p class="muted small">{_s("clock.title", language)}: {_when(now)} ({clock}) · '
        f"{_s('delay.title', language)}: {delay_minutes} {_s('delay.minutes', language)}</p>"
    )
    return _page(language, STRINGS["app.name"][language], body)


def not_found_page(language: Language) -> str:
    body = (
        f"<h1>{_s('crew.not_found', language)}</h1>"
        f'<p><a href="/?lang={language.value}">← {_s("crew.back", language)}</a></p>'
    )
    return _page(language, STRINGS["crew.not_found"][language], body)


def crew_page(language: Language, view: CrewView) -> str:
    heads_state = "".join(
        f"<th>{_s(k, language)}</th>"
        for k in ("col.indicator", "col.where", "col.state", "col.reason", "col.compared")
    )
    heads_state += f"<th>{_s('col.suggestion', language)}</th>"
    heads_read = "".join(
        f"<th>{_s(k, language)}</th>"
        for k in ("col.indicator", "col.value", "col.where", "col.origin", "col.method", "col.when")
    )
    states_table = _scroll(
        _s("crew.states", language),
        f"<table><tr>{heads_state}</tr>{_state_rows(view.states, language)}</table>",
    )
    readings_table = _scroll(
        _s("crew.readings", language),
        f"<table><tr>{heads_read}</tr>{_reading_rows(view.readings, language)}</table>",
    )
    color = _STATUS_COLOR.get(worst_status(view), "#64748b")
    body = (
        f'<p><a href="/?lang={language.value}">← {_s("crew.back", language)}</a></p>'
        f"<h1>{_s('crew.title', language, crew=view.crew_id)}</h1>"
        f'<p class="muted">{_packages(view.bundles, language)} · '
        f"{_s('home.last', language)} {_when(view.last_arrival)}</p>"
        f'<div class="card crew" style="--c:{color}"><h2 style="margin-top:0">'
        f"{_s('crew.attention', language)}</h2>{_attention_block(view, language)}"
        f'<div class="row" style="margin-top:10px">{_system_pills(view, language)}'
        f"{_voice_chip(view, language)}</div></div>"
        f"{_trends(view.states, language)}"
        f"<h2>{_s('crew.states', language)}</h2>"
        f"{states_table}"
        f"<h2>{_s('crew.readings', language)}</h2>"
        f"{readings_table}"
        f"{_voice_section(view.voice, language)}"
        f'<p class="card">{_s("crew.limits", language)}</p>'
    )
    return _page(language, f"{view.crew_id} · {STRINGS['app.name'][language]}", body)
