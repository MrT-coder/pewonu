"""The body figure of the ground console: the astronaut app's silhouette with each system's state.

The silhouette is the project's own drawing (the one the astronaut app uses, ``assets/body.svg``).
Zones take the color of the worst state the astronaut's own app sent for that system; the console
never calculates a state. ``ground`` does not import ``astronaut``, so the paths live here.
"""

from __future__ import annotations

from html import escape

from crew_self_check.core.reasons import Language
from crew_self_check.ground import i18n
from crew_self_check.ground.i18n import text

_BODY = (
    "M150.0,8.0 C144.7,8.0 138.5,8.5 134.0,11.0 C129.5,13.5 125.5,17.5 123.0,23.0 "
    "C120.5,28.5 119.2,37.3 119.0,44.0 C118.8,50.7 120.2,57.5 122.0,63.0 C123.8,68.5 "
    "127.5,73.3 130.0,77.0 C132.5,80.7 136.0,82.3 137.0,85.0 C138.0,87.7 136.2,90.3 "
    "136.0,93.0 C135.8,95.7 138.7,99.0 136.0,101.0 C133.3,103.0 126.0,103.8 120.0,105.0 "
    "C114.0,106.2 106.0,106.7 100.0,108.0 C94.0,109.3 88.7,110.3 84.0,113.0 C79.3,115.7 "
    "74.8,119.5 72.0,124.0 C69.2,128.5 65.7,133.3 67.0,140.0 C68.3,146.7 76.7,155.7 "
    "80.0,164.0 C83.3,172.3 84.5,181.3 87.0,190.0 C89.5,198.7 93.2,207.7 95.0,216.0 "
    "C96.8,224.3 98.2,231.7 98.0,240.0 C97.8,248.3 95.5,256.7 94.0,266.0 C92.5,275.3 "
    "90.0,285.0 89.0,296.0 C88.0,307.0 87.3,319.7 88.0,332.0 C88.7,344.3 91.5,358.0 "
    "93.0,370.0 C94.5,382.0 96.8,392.3 97.0,404.0 C97.2,415.7 94.2,427.7 94.0,440.0 "
    "C93.8,452.3 94.7,465.7 96.0,478.0 C97.3,490.3 101.0,504.3 102.0,514.0 C103.0,523.7 "
    "103.2,530.3 102.0,536.0 C100.8,541.7 98.0,544.7 95.0,548.0 C92.0,551.3 83.5,553.5 "
    "84.0,556.0 C84.5,558.5 92.0,562.8 98.0,563.0 C104.0,563.2 115.3,561.5 120.0,557.0 "
    "C124.7,552.5 125.0,545.5 126.0,536.0 C127.0,526.5 126.0,513.3 126.0,500.0 "
    "C126.0,486.7 125.5,471.0 126.0,456.0 C126.5,441.0 127.8,425.7 129.0,410.0 "
    "C130.2,394.3 131.2,376.7 133.0,362.0 C134.8,347.3 137.2,332.0 140.0,322.0 "
    "C142.8,312.0 146.7,302.0 150.0,302.0 C153.3,302.0 157.2,312.0 160.0,322.0 "
    "C162.8,332.0 165.2,347.3 167.0,362.0 C168.8,376.7 169.8,394.3 171.0,410.0 "
    "C172.2,425.7 173.5,441.0 174.0,456.0 C174.5,471.0 174.0,486.7 174.0,500.0 "
    "C174.0,513.3 173.0,526.5 174.0,536.0 C175.0,545.5 175.3,552.5 180.0,557.0 "
    "C184.7,561.5 196.0,563.2 202.0,563.0 C208.0,562.8 215.5,558.5 216.0,556.0 "
    "C216.5,553.5 208.0,551.3 205.0,548.0 C202.0,544.7 199.2,541.7 198.0,536.0 "
    "C196.8,530.3 197.0,523.7 198.0,514.0 C199.0,504.3 202.7,490.3 204.0,478.0 "
    "C205.3,465.7 206.2,452.3 206.0,440.0 C205.8,427.7 202.8,415.7 203.0,404.0 "
    "C203.2,392.3 205.5,382.0 207.0,370.0 C208.5,358.0 211.3,344.3 212.0,332.0 "
    "C212.7,319.7 212.0,307.0 211.0,296.0 C210.0,285.0 207.5,275.3 206.0,266.0 "
    "C204.5,256.7 202.2,248.3 202.0,240.0 C201.8,231.7 203.2,224.3 205.0,216.0 "
    "C206.8,207.7 210.5,198.7 213.0,190.0 C215.5,181.3 216.7,172.3 220.0,164.0 "
    "C223.3,155.7 231.7,146.7 233.0,140.0 C234.3,133.3 230.8,128.5 228.0,124.0 "
    "C225.2,119.5 220.7,115.7 216.0,113.0 C211.3,110.3 206.0,109.3 200.0,108.0 "
    "C194.0,106.7 186.0,106.2 180.0,105.0 C174.0,103.8 166.7,103.0 164.0,101.0 "
    "C161.3,99.0 164.2,95.7 164.0,93.0 C163.8,90.3 162.0,87.7 163.0,85.0 C164.0,82.3 "
    "167.5,80.7 170.0,77.0 C172.5,73.3 176.2,68.5 178.0,63.0 C179.8,57.5 181.2,50.7 "
    "181.0,44.0 C180.8,37.3 179.5,28.5 177.0,23.0 C174.5,17.5 170.5,13.5 166.0,11.0 "
    "C161.5,8.5 155.3,8.0 150.0,8.0Z"
)
_ARM_LEFT = (
    "M84.0,114.0 C81.0,113.0 73.7,116.7 70.0,122.0 C66.3,127.3 64.3,135.3 62.0,146.0 "
    "C59.7,156.7 58.0,172.0 56.0,186.0 C54.0,200.0 52.0,216.0 50.0,230.0 C48.0,244.0 "
    "46.3,259.0 44.0,270.0 C41.7,281.0 39.0,288.0 36.0,296.0 C33.0,304.0 28.3,311.7 "
    "26.0,318.0 C23.7,324.3 21.3,330.3 22.0,334.0 C22.7,337.7 28.0,336.3 30.0,340.0 "
    "C32.0,343.7 32.3,351.3 34.0,356.0 C35.7,360.7 37.7,366.3 40.0,368.0 C42.3,369.7 "
    "45.7,368.7 48.0,366.0 C50.3,363.3 52.3,357.0 54.0,352.0 C55.7,347.0 56.7,341.7 "
    "58.0,336.0 C59.3,330.3 60.7,324.7 62.0,318.0 C63.3,311.3 64.7,306.0 66.0,296.0 "
    "C67.3,286.0 68.3,271.3 70.0,258.0 C71.7,244.7 74.0,229.0 76.0,216.0 C78.0,203.0 "
    "80.3,191.0 82.0,180.0 C83.7,169.0 85.0,158.7 86.0,150.0 C87.0,141.3 88.3,134.0 "
    "88.0,128.0 C87.7,122.0 87.0,115.0 84.0,114.0Z"
)
_ARM_RIGHT = (
    "M216.0,114.0 C219.0,113.0 226.3,116.7 230.0,122.0 C233.7,127.3 235.7,135.3 "
    "238.0,146.0 C240.3,156.7 242.0,172.0 244.0,186.0 C246.0,200.0 248.0,216.0 "
    "250.0,230.0 C252.0,244.0 253.7,259.0 256.0,270.0 C258.3,281.0 261.0,288.0 "
    "264.0,296.0 C267.0,304.0 271.7,311.7 274.0,318.0 C276.3,324.3 278.7,330.3 "
    "278.0,334.0 C277.3,337.7 272.0,336.3 270.0,340.0 C268.0,343.7 267.7,351.3 "
    "266.0,356.0 C264.3,360.7 262.3,366.3 260.0,368.0 C257.7,369.7 254.3,368.7 "
    "252.0,366.0 C249.7,363.3 247.7,357.0 246.0,352.0 C244.3,347.0 243.3,341.7 "
    "242.0,336.0 C240.7,330.3 239.3,324.7 238.0,318.0 C236.7,311.3 235.3,306.0 "
    "234.0,296.0 C232.7,286.0 231.7,271.3 230.0,258.0 C228.3,244.7 226.0,229.0 "
    "224.0,216.0 C222.0,203.0 219.7,191.0 218.0,180.0 C216.3,169.0 215.0,158.7 "
    "214.0,150.0 C213.0,141.3 211.7,134.0 212.0,128.0 C212.3,122.0 213.0,115.0 "
    "216.0,114.0Z"
)

_COLOR = {
    "ok": "#34d399",
    "watch": "#fbbf24",
    "act": "#fb7185",
    "insufficient_data": "#64748b",
    "none": "#334155",
}

# system, shape in the silhouette's own units, zone center, label side and label height
_ZONES = (
    ("sleep_brain", '<circle cx="150" cy="46" r="24"/>', 150, 46, "r", 62),
    ("mood", '<circle cx="180" cy="22" r="9"/>', 180, 22, "r", 22),
    ("vestibular", '<ellipse cx="121" cy="52" rx="6" ry="10"/>', 121, 52, "l", 52),
    ("cardiovascular", '<ellipse cx="138" cy="160" rx="26" ry="30"/>', 138, 160, "r", 160),
    ("immune", '<rect x="112" y="205" width="76" height="40" rx="18"/>', 150, 225, "r", 225),
    ("bone_muscle", '<rect x="98" y="340" width="104" height="150" rx="30"/>', 150, 415, "r", 415),
)
_LEFT, _RIGHT = -150, 450  # the viewBox leaves room for the labels on both sides


def figure_svg(levels: dict[str, str], language: Language, labelled: bool = True) -> str:
    """The silhouette with one zone per system. ``levels`` maps a system to its worst state."""
    shapes: list[str] = []
    labels: list[str] = []
    lines: list[str] = []
    summary: list[str] = []
    for system, shape, cx, cy, side, ly in _ZONES:
        known = system in levels
        status = levels.get(system, "none")
        color = _COLOR.get(status, _COLOR["none"])
        name = text(i18n.SYSTEM, system, language)
        state = text(i18n.STATUS_SHORT, status, language)
        summary.append(f"{name}: {state}")
        flag = " flag" if status in ("watch", "act") else ""
        shapes.append(
            f'<g class="zone{flag}" fill="{color}" fill-opacity="{0.30 if known else 0.10}" '
            f'stroke="{color}" stroke-width="{3 if known else 1}">{shape}</g>'
        )
        if labelled:
            edge = 296 if side == "r" else 4
            anchor = "start" if side == "r" else "end"
            tx = edge + (10 if side == "r" else -10)
            lines.append(
                f'<line x1="{cx}" y1="{cy}" x2="{edge}" y2="{ly}" stroke="{color}" '
                'stroke-opacity="0.5" stroke-dasharray="3 4"/>'
            )
            labels.append(
                f'<text x="{tx}" y="{ly - 2}" text-anchor="{anchor}" class="zl">'
                f"{escape(name)}</text>"
                f'<text x="{tx}" y="{ly + 13}" text-anchor="{anchor}" class="zs" fill="{color}">'
                f"{escape(state)}</text>"
            )
    view = f"{_LEFT} 0 {_RIGHT - _LEFT} 580" if labelled else "0 0 300 580"
    aria = escape("; ".join(summary))
    body = "".join(lines) + "".join(shapes) + "".join(labels)
    return (
        f'<svg class="figure" viewBox="{view}" role="img" aria-label="{aria}">'
        '<defs><linearGradient id="bodyfill" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#0f9f92"/>'
        '</linearGradient><filter id="bodyglow" x="-20%" y="-10%" width="140%" height="120%">'
        '<feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/>'
        '<feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        '<g fill="url(#bodyfill)" stroke="#e6fffb" stroke-width="2.2" stroke-linejoin="round" '
        'filter="url(#bodyglow)" opacity="0.92">'
        f'<path d="{_BODY}"/><path d="{_ARM_LEFT}"/><path d="{_ARM_RIGHT}"/></g>{body}</svg>'
    )
