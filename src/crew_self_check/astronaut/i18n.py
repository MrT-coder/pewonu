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
