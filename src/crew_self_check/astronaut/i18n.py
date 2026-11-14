"""Interface texts: English is the source, Spanish the translation (D-016).

Only say what is true of the prototype: no diagnosis, no unverifiable promise
(AGENTS.md, section 6).
"""

from __future__ import annotations

from crew_self_check.core.reasons import Language

_EN, _ES = Language.EN, Language.ES

# Keys that are the same in both languages on purpose (names and examples).
SAME_IN_BOTH = frozenset({"app.name", "login.code_hint"})

STRINGS: dict[str, dict[Language, str]] = {
    "app.name": {_EN: "Crew Self-Check", _ES: "Crew Self-Check"},
    "app.tagline": {
        _EN: "Know your own baseline.",
        _ES: "Conoce tu propia línea base.",
    },
    "login.title": {
        _EN: "Sign in with your astronaut code",
        _ES: "Ingresa con tu código de astronauta",
    },
    "login.code_label": {_EN: "Astronaut code", _ES: "Código de astronauta"},
    "login.code_hint": {_EN: "AST-0000", _ES: "AST-0000"},
    "login.enter": {_EN: "Enter", _ES: "Entrar"},
    "login.error.invalid_format": {
        _EN: "Use the format AST-0000.",
        _ES: "Usa el formato AST-0000.",
    },
    "login.error.unknown_code": {
        _EN: "Code not registered on this computer.",
        _ES: "Código no registrado en este equipo.",
    },
    "login.demo_title": {
        _EN: "Simulated demo crew",
        _ES: "Tripulación de demostración (simulada)",
    },
    "login.demo_codes": {_EN: "Try {codes}", _ES: "Prueba con {codes}"},
    "login.private": {
        _EN: "Your code opens only your own profile on this computer.",
        _ES: "Tu código abre solo tu propio perfil en este equipo.",
    },
    "nav.home": {_EN: "Home", _ES: "Inicio"},
    "nav.checkin": {_EN: "Check-in", _ES: "Chequeo"},
    "nav.body": {_EN: "Body", _ES: "Cuerpo"},
    "nav.summary": {_EN: "Summary", _ES: "Resumen"},
    "nav.limits": {_EN: "Limits", _ES: "Límites"},
    "nav.logout": {_EN: "Sign out", _ES: "Salir"},
    "home.greeting": {_EN: "Hello, {code}", _ES: "Hola, {code}"},
    "home.subtitle": {
        _EN: "Each color is relative to your own baseline, not to a population.",
        _ES: "Cada color es relativo a tu propia línea base, no a una población.",
    },
    "home.privacy_title": {_EN: "Private by default", _ES: "Privado por defecto"},
    "home.privacy_body": {
        _EN: "What you enter stays on this computer. "
        "Nothing is sent to the ground team unless you confirm it.",
        _ES: "Lo que ingresas se queda en este equipo. "
        "Nada se envía al equipo en Tierra si no lo confirmas.",
    },
    "home.parts_title": {_EN: "What you will do here", _ES: "Qué harás aquí"},
    "home.cta": {_EN: "Start today's check-in", _ES: "Empezar el chequeo de hoy"},
    "part.coming": {_EN: "Coming next", _ES: "Próximamente"},
    "part.checkin.title": {_EN: "Daily check-in", _ES: "Chequeo diario"},
    "part.checkin.body": {
        _EN: "How you feel (five faces), your pulse counted by hand and an optional voice log.",
        _ES: "Cómo te sientes (cinco caritas), tu pulso contado a mano "
        "y una bitácora de voz opcional.",
    },
    "part.body.title": {_EN: "Body view", _ES: "Vista del cuerpo"},
    "part.body.body": {
        _EN: "Each system colored against your own baseline, with a card that explains it.",
        _ES: "Cada sistema coloreado frente a tu propia línea base, "
        "con una tarjeta que lo explica.",
    },
    "part.summary.title": {_EN: "Your summary", _ES: "Tu resumen"},
    "part.summary.body": {
        _EN: "Your readings and states in one place, and what you can choose to share.",
        _ES: "Tus lecturas y estados en un solo lugar, y lo que puedes elegir compartir.",
    },
    "checkin.title": {_EN: "Daily check-in", _ES: "Chequeo diario"},
    "checkin.subtitle": {
        _EN: "Two quick entries today: your pulse and how you feel.",
        _ES: "Dos registros rápidos hoy: tu pulso y cómo te sientes.",
    },
    "checkin.mood.title": {_EN: "How you feel", _ES: "Cómo te sientes"},
    "checkin.mood.body": {
        _EN: "Five faces, one tap.",
        _ES: "Cinco caritas, un toque.",
    },
    "pulse.title": {_EN: "Pulse mission", _ES: "Misión del pulso"},
    "pulse.hub_body": {
        _EN: "Count your own pulse at the wrist. The app does the math.",
        _ES: "Cuenta tu propio pulso en la muñeca. La app hace la cuenta.",
    },
    "pulse.start": {_EN: "Start the mission", _ES: "Empezar la misión"},
    "pulse.last": {
        _EN: "Last pulse recorded: {bpm} bpm",
        _ES: "Último pulso registrado: {bpm} lpm",
    },
    "pulse.station": {_EN: "Station {n} of 4", _ES: "Estación {n} de 4"},
    "pulse.rest.title": {_EN: "Rest first", _ES: "Descansa primero"},
    "pulse.rest.body": {
        _EN: "Sit or lie down and rest completely for at least 10 minutes before measuring.",
        _ES: "Siéntate o acuéstate y descansa por completo al menos 10 minutos antes de medir.",
    },
    "pulse.locate.title": {_EN: "Find the artery", _ES: "Ubica la arteria"},
    "pulse.locate.body": {
        _EN: "Place your index and middle fingers together on the inside of your wrist, "
        "on the thumb side. Do not use your thumb.",
        _ES: "Coloca juntos los dedos índice y medio en la parte interna de la muñeca, "
        "del lado del pulgar. No uses el pulgar.",
    },
    "pulse.pressure.title": {_EN: "Press lightly", _ES: "Presiona suave"},
    "pulse.pressure.body": {
        _EN: "Press lightly with flat fingers until you feel the beats. Do not block the flow.",
        _ES: "Presiona suave con los dedos planos hasta sentir los latidos. No bloquees el flujo.",
    },
    "pulse.count.title": {_EN: "Count the beats", _ES: "Cuenta los latidos"},
    "pulse.count.body": {
        _EN: "Tap the big button on every beat you feel. We count for {seconds} seconds.",
        _ES: "Toca el botón grande con cada latido que sientas. "
        "Contamos durante {seconds} segundos.",
    },
    "pulse.interval": {_EN: "How long to count", _ES: "Cuánto tiempo contar"},
    "pulse.interval_30": {_EN: "30 seconds (×2)", _ES: "30 segundos (×2)"},
    "pulse.interval_60": {_EN: "60 seconds", _ES: "60 segundos"},
    "pulse.next": {_EN: "Done, next", _ES: "Listo, siguiente"},
    "pulse.begin_count": {_EN: "Start counting", _ES: "Empezar a contar"},
    "pulse.tap": {_EN: "Tap on each beat", _ES: "Toca con cada latido"},
    "pulse.beats": {_EN: "{n} beats", _ES: "{n} latidos"},
    "pulse.seconds_left": {_EN: "{s} s left", _ES: "{s} s restantes"},
    "pulse.result_title": {_EN: "Your count", _ES: "Tu conteo"},
    "pulse.formula_30": {
        _EN: "{taps} beats × 2 = {bpm} bpm",
        _ES: "{taps} latidos × 2 = {bpm} lpm",
    },
    "pulse.formula_60": {
        _EN: "{taps} beats in 60 s = {bpm} bpm",
        _ES: "{taps} latidos en 60 s = {bpm} lpm",
    },
    "pulse.recount_body": {
        _EN: "That count looks off, you may have lost count. Try again.",
        _ES: "Ese conteo parece raro, quizá perdiste la cuenta. Inténtalo de nuevo.",
    },
    "pulse.recount": {_EN: "Count again", _ES: "Contar de nuevo"},
    "pulse.save": {_EN: "Save to my record", _ES: "Guardar en mi registro"},
    "pulse.leave": {_EN: "Leave the mission", _ES: "Salir de la misión"},
    "pulse.points": {_EN: "{points} points", _ES: "{points} puntos"},
    "pulse.points_note": {
        _EN: "Points reward the technique, not the value of your pulse.",
        _ES: "Los puntos premian la técnica, no el valor de tu pulso.",
    },
    "pulse.badge": {_EN: "Pulse scout", _ES: "Explorador del pulso"},
    "pulse.badge_note": {
        _EN: "Every complete measurement earns it.",
        _ES: "Cada medición completa lo gana.",
    },
    "pulse.saved": {
        _EN: "Pulse saved to your record.",
        _ES: "Pulso guardado en tu registro.",
    },
    "pulse.source": {_EN: "Technique: MedlinePlus (NIH).", _ES: "Técnica: MedlinePlus (NIH)."},
    "pulse.illustrations": {
        _EN: "Illustrations generated with AI.",
        _ES: "Ilustraciones generadas con IA.",
    },
    "limits.title": {_EN: "Limits of this prototype", _ES: "Límites de este prototipo"},
    "limits.body": {
        _EN: "Analog and simulated data: not from real astronauts. "
        "Nothing here has been validated in orbit. "
        "This tool does not diagnose and does not replace medical care; "
        "it compares you with your own baseline.",
        _ES: "Datos análogos y simulados: no son de astronautas reales. "
        "Nada aquí está validado en órbita. "
        "Esta herramienta no diagnostica ni reemplaza la atención médica; "
        "te compara con tu propia línea base.",
    },
    "limits.close": {_EN: "Close", _ES: "Cerrar"},
}


def translate(key: str, language: Language, **params: object) -> str:
    """The text for ``key``; an unknown key or a missing parameter raises ``KeyError``."""
    return STRINGS[key][language].format(**params)
