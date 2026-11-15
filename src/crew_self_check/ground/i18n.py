"""Texts of the ground view in English (source language) and Spanish (D-016).

``ground`` does not import ``astronaut``, so it carries its own small catalogue. Reasons are shown
as the astronaut app wrote them inside the bundle: they are data, not interface text.
"""

from __future__ import annotations

from crew_self_check.core.reasons import Language

_EN, _ES = Language.EN, Language.ES

STRINGS: dict[str, dict[Language, str]] = {
    "app.name": {_EN: "Crew Self-Check · Ground base", _ES: "Crew Self-Check · Base en Tierra"},
    "banner": {
        _EN: "Simulated crew and simulated data. This is a prototype, not a medical system.",
        _ES: "Tripulación y datos simulados. Es un prototipo, no un sistema médico.",
    },
    "home.title": {_EN: "Crew members", _ES: "Tripulantes"},
    "home.only_shared": {
        _EN: "You only see what each astronaut chose to send, after the communication delay.",
        _ES: "Solo ves lo que cada astronauta eligió enviar, después del retraso de comunicación.",
    },
    "home.nothing": {
        _EN: "Nothing has arrived yet.",
        _ES: "Aún no ha llegado nada.",
    },
    "home.packages": {_EN: "packages received", _ES: "paquetes recibidos"},
    "home.package_one": {_EN: "package received", _ES: "paquete recibido"},
    "action.refresh": {_EN: "Refresh", _ES: "Actualizar"},
    "home.last": {_EN: "last arrival", _ES: "última llegada"},
    "home.open": {_EN: "Open", _ES: "Abrir"},
    "clock.title": {_EN: "Ground clock", _ES: "Reloj de la base"},
    "clock.simulated": {_EN: "simulated (follows the journey)", _ES: "simulado (sigue el viaje)"},
    "clock.real": {_EN: "real time", _ES: "tiempo real"},
    "delay.title": {_EN: "Communication delay", _ES: "Retraso de comunicación"},
    "delay.minutes": {_EN: "minutes", _ES: "minutos"},
    "crew.not_found": {
        _EN: "Nothing from this crew member has arrived.",
        _ES: "Nada de este tripulante ha llegado.",
    },
    "crew.back": {_EN: "All crew members", _ES: "Todos los tripulantes"},
    "crew.title": {_EN: "Crew member {crew}", _ES: "Tripulante {crew}"},
    "crew.states": {_EN: "State by indicator", _ES: "Estado por indicador"},
    "crew.readings": {_EN: "Latest readings sent", _ES: "Últimas lecturas enviadas"},
    "crew.attention": {_EN: "Needs attention", _ES: "Requiere atención"},
    "crew.attention_none": {
        _EN: "Nothing outside the usual range was sent.",
        _ES: "No se envió nada fuera del rango habitual.",
    },
    "crew.limits": {
        _EN: "This is not a diagnosis. States compare each reading with the person's own "
        "baseline or a labelled reference, and the ground cannot ask for more data.",
        _ES: "Esto no es un diagnóstico. Los estados comparan cada lectura con la línea base "
        "de la persona o con una referencia rotulada, y la base no puede pedir más datos.",
    },
    "col.indicator": {_EN: "Indicator", _ES: "Indicador"},
    "col.where": {_EN: "Where", _ES: "Dónde"},
    "col.state": {_EN: "State", _ES: "Estado"},
    "col.reason": {_EN: "Why", _ES: "Por qué"},
    "col.compared": {_EN: "Compared with", _ES: "Comparado con"},
    "col.suggestion": {_EN: "Suggestion", _ES: "Sugerencia"},
    "col.value": {_EN: "Value", _ES: "Valor"},
    "col.origin": {_EN: "Origin", _ES: "Origen"},
    "col.method": {_EN: "Method", _ES: "Método"},
    "col.when": {_EN: "When", _ES: "Cuándo"},
    "lang.switch": {_EN: "Español", _ES: "English"},
}

STATUS: dict[str, dict[Language, str]] = {
    "ok": {_EN: "Green · within range", _ES: "Verde · dentro del rango"},
    "watch": {_EN: "Amber · outside range", _ES: "Ámbar · fuera del rango"},
    "act": {_EN: "Red · far outside range", _ES: "Rojo · muy fuera del rango"},
    "insufficient_data": {_EN: "Gray · not enough data", _ES: "Gris · datos insuficientes"},
}

ESCALATION: dict[str, dict[Language, str]] = {
    "self_care": {_EN: "Self-care", _ES: "Autocuidado"},
    "crew_cmo": {_EN: "Ask the crew medical officer", _ES: "Consultar al oficial médico"},
    "ground_surgeon": {_EN: "Flight surgeon review", _ES: "Revisión del cirujano de vuelo"},
}

REFERENCE: dict[str, dict[Language, str]] = {
    "personal": {_EN: "personal baseline", _ES: "línea base personal"},
    "transition": {_EN: "transition reference", _ES: "referencia de transición"},
    "population": {_EN: "population reference", _ES: "referencia poblacional"},
}

ENVIRONMENT: dict[str, dict[Language, str]] = {
    "earth": {_EN: "Earth", _ES: "Tierra"},
    "spacecraft": {_EN: "Spacecraft", _ES: "Nave"},
    "planet": {_EN: "Mars", _ES: "Marte"},
}

INDICATOR: dict[str, dict[Language, str]] = {
    "resting_hr": {_EN: "Resting heart rate", _ES: "Pulso en reposo"},
    "systolic_bp": {_EN: "Systolic blood pressure", _ES: "Presión sistólica"},
    "diastolic_bp": {_EN: "Diastolic blood pressure", _ES: "Presión diastólica"},
    "blood_glucose": {_EN: "Blood glucose", _ES: "Glucosa en sangre"},
    "body_temp": {_EN: "Body temperature", _ES: "Temperatura corporal"},
    "sleep_hours": {_EN: "Sleep", _ES: "Sueño"},
    "mood": {_EN: "Mood", _ES: "Ánimo"},
    "spo2": {_EN: "Oxygen saturation", _ES: "Saturación de oxígeno"},
    "orthostatic_hr_delta": {_EN: "Pulse change on standing", _ES: "Cambio de pulso al pararse"},
    "vestibular_symptoms": {_EN: "Vestibular symptoms", _ES: "Síntomas vestibulares"},
    "tandem_walk_ok": {_EN: "Tandem walk", _ES: "Caminata en tándem"},
}

ORIGIN: dict[str, dict[Language, str]] = {
    "simulated-scenario": {_EN: "Simulated scenario", _ES: "Escenario simulado"},
    "manual": {_EN: "Entered by the astronaut", _ES: "Ingresado por el astronauta"},
    "sleep-accel": {_EN: "Sleep accelerometer", _ES: "Acelerómetro de sueño"},
    "official-2026": {_EN: "Official 2026 data", _ES: "Datos oficiales 2026"},
}

METHOD: dict[str, dict[Language, str]] = {
    "palpation": {_EN: "counted by hand", _ES: "contado a mano"},
    "device": {_EN: "device", _ES: "dispositivo"},
    "survey": {_EN: "survey", _ES: "encuesta"},
}


def text(table: dict[str, dict[Language, str]], key: str, language: Language) -> str:
    """The text for ``key``; a code this catalogue does not know is shown as it came."""
    entry = table.get(key)
    return entry[language] if entry else key


def language_from(value: str | None) -> Language:
    return Language.ES if value == "es" else Language.EN
