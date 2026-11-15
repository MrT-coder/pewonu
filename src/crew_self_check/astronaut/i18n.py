"""Interface texts: English is the source, Spanish the translation (D-016).

Only say what is true of the prototype: no diagnosis, no unverifiable promise
(AGENTS.md, section 6).
"""

from __future__ import annotations

from crew_self_check.core.reasons import Language

_EN, _ES = Language.EN, Language.ES

# Keys that are the same in both languages on purpose (names and examples).
SAME_IN_BOTH = frozenset({"app.name", "login.code_hint", "value.no"})

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
    "login.code_help": {_EN: "AST stands for astronaut.", _ES: "AST significa astronauta."},
    "login.error.invalid_format": {
        _EN: "Use the format AST-0000 (AST = astronaut, then four digits).",
        _ES: "Usa el formato AST-0000 (AST = astronauta, luego cuatro dígitos).",
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
    "nav.glossary": {_EN: "Glossary", _ES: "Glosario"},
    "glossary.close": {_EN: "Close", _ES: "Cerrar"},
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
    "mood.prompt": {
        _EN: "How do you feel at the end of this shift?",
        _ES: "¿Cómo te sientes al cerrar este turno?",
    },
    "mood.level.1": {_EN: "Very low", _ES: "Muy bajo"},
    "mood.level.2": {_EN: "Low", _ES: "Bajo"},
    "mood.level.3": {_EN: "Okay", _ES: "Regular"},
    "mood.level.4": {_EN: "Good", _ES: "Bien"},
    "mood.level.5": {_EN: "Very good", _ES: "Muy bien"},
    "mood.save": {_EN: "Save how I feel", _ES: "Guardar cómo me siento"},
    "mood.last": {_EN: "Last check-in: {label}", _ES: "Último registro: {label}"},
    "mood.note": {
        _EN: "Saved on this computer. Nothing is sent without your confirmation.",
        _ES: "Se guarda en este equipo. Nada se envía sin tu confirmación.",
    },
    "pulse.title": {_EN: "Pulse mission", _ES: "Misión del pulso"},
    "pulse.hub_body": {
        _EN: "Count your own pulse at the wrist. The app does the math.",
        _ES: "Cuenta tu propio pulso en la muñeca. La app hace la cuenta.",
    },
    "pulse.start": {_EN: "Start the mission", _ES: "Empezar la misión"},
    "pulse.last": {
        _EN: "Last pulse recorded: {bpm} beats per minute (bpm)",
        _ES: "Último pulso registrado: {bpm} latidos por minuto (lpm)",
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
        _EN: "Count the beats you feel for {seconds} seconds, then enter how many you counted.",
        _ES: "Cuenta los latidos que sientas durante {seconds} segundos "
        "y escribe cuántos contaste.",
    },
    "pulse.interval": {_EN: "How long to count", _ES: "Cuánto tiempo contar"},
    "pulse.interval_30": {_EN: "30 seconds (×2)", _ES: "30 segundos (×2)"},  # noqa: RUF001
    "pulse.interval_60": {_EN: "60 seconds", _ES: "60 segundos"},
    "pulse.next": {_EN: "Done, next", _ES: "Listo, siguiente"},
    "pulse.timer_start": {
        _EN: "Start a {seconds}-second timer (optional)",
        _ES: "Iniciar un temporizador de {seconds} segundos (opcional)",
    },
    "pulse.timer_done": {
        _EN: "Time's up. Enter how many beats you counted.",
        _ES: "Se acabó el tiempo. Escribe cuántos latidos contaste.",
    },
    "pulse.beats_label": {
        _EN: "Beats counted in {seconds} seconds",
        _ES: "Latidos contados en {seconds} segundos",
    },
    "pulse.calculate": {_EN: "Calculate my pulse", _ES: "Calcular mi pulso"},
    "pulse.beats_error": {
        _EN: "Enter a whole number of beats.",
        _ES: "Escribe un número entero de latidos.",
    },
    "pulse.seconds_left": {_EN: "{s} s left", _ES: "{s} s restantes"},
    "pulse.result_title": {_EN: "Your count", _ES: "Tu conteo"},
    "pulse.formula_30": {
        _EN: "{beats} beats × 2 = {bpm} beats per minute (bpm)",  # noqa: RUF001
        _ES: "{beats} latidos × 2 = {bpm} latidos por minuto (lpm)",  # noqa: RUF001
    },
    "pulse.formula_60": {
        _EN: "{beats} beats in 60 s = {bpm} beats per minute (bpm)",
        _ES: "{beats} latidos en 60 s = {bpm} latidos por minuto (lpm)",
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
    "pulse.meaning_title": {_EN: "What your count means", _ES: "Qué significa tu conteo"},
    "pulse.outside_one": {
        _EN: "One count outside your usual range",
        _ES: "Un conteo fuera de tu rango habitual",
    },
    "pulse.band": {
        _EN: "Your usual range here: {low} to {high} bpm, from {days} days of readings.",
        _ES: "Tu rango habitual aquí: de {low} a {high} lpm, con {days} días de lecturas.",
    },
    "pulse.todo_title": {_EN: "What to do now", _ES: "Qué hacer ahora"},
    "pulse.todo.single": {
        _EN: "This count is outside your usual range, but one count is not a trend: the "
        "state only turns amber when several counts in a row stay outside.",
        _ES: "Este conteo está fuera de tu rango habitual, pero un conteo no es una "
        "tendencia: el estado solo pasa a ámbar si varios conteos seguidos se quedan fuera.",
    },
    "pulse.todo.rest": {
        _EN: "Rest sitting down for 10 minutes, then count again: a resting pulse needs at "
        "least 10 minutes of rest first.",
        _ES: "Descansa sentado 10 minutos y cuenta de nuevo: un pulso en reposo necesita al "
        "menos 10 minutos de descanso antes.",
    },
    "pulse.todo.recount": {
        _EN: "If the new count is still outside your range, the change is real and worth "
        "telling someone; if it comes back inside, it was probably the effort or the moment.",
        _ES: "Si el nuevo conteo sigue fuera de tu rango, el cambio es real y conviene "
        "avisar a alguien; si vuelve a entrar, probablemente fue el esfuerzo o el momento.",
    },
    "pulse.todo.fluids": {
        _EN: "A fast pulse can go with dehydration or an infection: think about whether you "
        "have drunk enough and how you feel.",
        _ES: "Un pulso rápido puede acompañar a la deshidratación o a una infección: piensa "
        "si has bebido lo suficiente y cómo te sientes.",
    },
    "pulse.todo.uneven": {
        _EN: "If the beats feel uneven, say so: an irregular pulse can also be a sign of a "
        "problem.",
        _ES: "Si los latidos se sienten irregulares, dilo: un pulso irregular también puede "
        "ser señal de un problema.",
    },
    "pulse.todo.same_time": {
        _EN: "Measure again tomorrow at the same time of day, at rest, so the comparison with "
        "your own baseline stays fair.",
        _ES: "Vuelve a medir mañana a la misma hora del día y en reposo, para que la "
        "comparación con tu propia línea base siga siendo justa.",
    },
    "pulse.todo.rest_first": {
        _EN: "Remember: rest for 10 minutes before every count.",
        _ES: "Recuerda: descansa 10 minutos antes de cada conteo.",
    },
    "pulse.todo.keep_measuring": {
        _EN: "Keep measuring every day at rest: the app needs more days to learn what is "
        "normal for you.",
        _ES: "Sigue midiendo cada día en reposo: la app necesita más días para aprender qué "
        "es normal en ti.",
    },
    "pulse.todo.tell": {_EN: "Who to tell", _ES: "A quién avisar"},
    "pulse.saved": {
        _EN: "Pulse saved to your record.",
        _ES: "Pulso guardado en tu registro.",
    },
    "pulse.source": {
        _EN: "Technique: MedlinePlus, from the United States National Institutes of Health (NIH).",
        _ES: "Técnica: MedlinePlus, de los Institutos Nacionales de Salud de Estados Unidos (NIH).",
    },
    "pulse.illustrations": {
        _EN: "Illustrations generated with artificial intelligence (AI).",
        _ES: "Ilustraciones generadas con inteligencia artificial (IA).",
    },
    "journey.title": {
        _EN: "Mission journey",
        _ES: "Viaje de la misión",
    },
    "journey.day": {
        _EN: "Day {label} · {place}",
        _ES: "Día {label} · {place}",
    },
    "journey.previous": {
        _EN: "Previous day",
        _ES: "Día anterior",
    },
    "journey.next": {
        _EN: "Next day",
        _ES: "Día siguiente",
    },
    "journey.note": {
        _EN: "Simulated time: each step moves the demo one day. E-n = days before "
        "leaving, T+n = days in transit, R+n = days since arrival.",
        _ES: "Tiempo simulado: cada paso avanza la demo un día. E-n = días antes de "
        "partir, T+n = días en tránsito, R+n = días desde la llegada.",
    },
    "env.earth": {
        _EN: "Earth",
        _ES: "Tierra",
    },
    "env.spacecraft": {
        _EN: "Spacecraft",
        _ES: "Nave",
    },
    "env.planet": {
        _EN: "Planet surface (Mars in the demo)",
        _ES: "Superficie del planeta (Marte en la demo)",
    },
    "env.earth.short": {
        _EN: "Earth",
        _ES: "Tierra",
    },
    "env.spacecraft.short": {
        _EN: "spacecraft",
        _ES: "nave",
    },
    "env.planet.short": {
        _EN: "planet",
        _ES: "planeta",
    },
    "system.cardiovascular": {
        _EN: "Heart and circulation",
        _ES: "Corazón y circulación",
    },
    "system.vestibular": {
        _EN: "Balance (inner ear)",
        _ES: "Equilibrio (oído interno)",
    },
    "system.sleep_brain": {
        _EN: "Sleep and brain",
        _ES: "Sueño y cerebro",
    },
    "system.mood": {
        _EN: "Mood",
        _ES: "Ánimo",
    },
    "system.immune": {
        _EN: "Immune system (body temperature)",
        _ES: "Sistema inmune (temperatura corporal)",
    },
    "system.bone_muscle": {
        _EN: "Bones and muscles",
        _ES: "Huesos y músculos",
    },
    "system.cardiovascular.what": {
        _EN: "Resting pulse, blood pressure, the pulse change when you stand up and "
        "oxygen saturation.",
        _ES: "Pulso en reposo, presión arterial, el cambio del pulso al ponerte de "
        "pie y la saturación de oxígeno.",
    },
    "system.cardiovascular.why": {
        _EN: "Gravity and a closed environment can change how the heart and blood "
        "vessels behave. NASA tracks cardiovascular adaptations as a "
        "spaceflight risk.",
        _ES: "La gravedad y un ambiente cerrado pueden cambiar cómo se comportan el "
        "corazón y los vasos sanguíneos. La NASA sigue las adaptaciones "
        "cardiovasculares como un riesgo del vuelo espacial.",
    },
    "system.vestibular.what": {
        _EN: "Balance and dizziness: your symptoms and the walk-in-a-line test.",
        _ES: "Equilibrio y mareo: tus síntomas y la prueba de caminar en línea.",
    },
    "system.vestibular.why": {
        _EN: "Moving between gravity levels can disturb the sense of balance. NASA "
        "tracks sensorimotor and vestibular function as a spaceflight risk.",
        _ES: "Pasar de un nivel de gravedad a otro puede alterar el sentido del "
        "equilibrio. La NASA sigue la función sensoriomotora y vestibular como "
        "un riesgo del vuelo espacial.",
    },
    "system.sleep_brain.what": {
        _EN: "Hours of sleep.",
        _ES: "Horas de sueño.",
    },
    "system.sleep_brain.why": {
        _EN: "Light, schedules and isolation can change how you sleep. NASA tracks "
        "inadequate sleep and irregular schedules as a spaceflight risk.",
        _ES: "La luz, los horarios y el aislamiento pueden cambiar cómo duermes. La "
        "NASA sigue el sueño inadecuado y los horarios irregulares como un "
        "riesgo del vuelo espacial.",
    },
    "system.mood.what": {
        _EN: "How you feel, from the five faces.",
        _ES: "Cómo te sientes, según las cinco caritas.",
    },
    "system.mood.why": {
        _EN: "Isolation and confinement can weigh on mood. NASA tracks behavioral "
        "changes as a spaceflight risk.",
        _ES: "El aislamiento y el confinamiento pueden pesar en el ánimo. La NASA "
        "sigue los cambios conductuales como un riesgo del vuelo espacial.",
    },
    "system.immune.what": {
        _EN: "Body temperature.",
        _ES: "Temperatura corporal.",
    },
    "system.immune.why": {
        _EN: "Closed environments can affect immune responses. NASA tracks altered "
        "immune responses as a spaceflight risk.",
        _ES: "Los ambientes cerrados pueden afectar las respuestas inmunes. La NASA "
        "sigue las respuestas inmunes alteradas como un riesgo del vuelo "
        "espacial.",
    },
    "system.bone_muscle.what": {
        _EN: "Nothing is measured for this yet.",
        _ES: "Todavía no se mide nada para esto.",
    },
    "system.bone_muscle.why": {
        _EN: "Long stays without gravity can change bones and muscles. NASA tracks "
        "bone changes and reduced fitness as spaceflight risks.",
        _ES: "Las estadías largas sin gravedad pueden cambiar huesos y músculos. La "
        "NASA sigue los cambios óseos y la menor aptitud física como riesgos "
        "del vuelo espacial.",
    },
    "status.ok": {
        _EN: "Within the range it is compared with",
        _ES: "Dentro del rango con el que se compara",
    },
    "status.watch": {
        _EN: "Outside the range it is compared with",
        _ES: "Fuera del rango con el que se compara",
    },
    "status.act": {
        _EN: "Far outside the range it is compared with",
        _ES: "Muy fuera del rango con el que se compara",
    },
    "status.insufficient_data": {
        _EN: "Not enough data yet",
        _ES: "Aún no hay datos suficientes",
    },
    "status.nothing": {
        _EN: "Nothing measured for this yet",
        _ES: "Todavía no se mide nada para esto",
    },
    "body.hint": {
        _EN: "Tap a zone to see what it shows and why.",
        _ES: "Toca una zona para ver qué muestra y por qué.",
    },
    "body.legend": {
        _EN: "What the colors mean",
        _ES: "Qué significan los colores",
    },
    "body.colors_note": {
        _EN: "A color is a comparison, not a diagnosis.",
        _ES: "Un color es una comparación, no un diagnóstico.",
    },
    "card.compared": {
        _EN: "Compared with: {what}",
        _ES: "Comparado con: {what}",
    },
    "reference.personal": {
        _EN: "your own baseline in this space",
        _ES: "tu propia línea base en este espacio",
    },
    "reference.transition": {
        _EN: "your previous baseline ({previous}); your own here is still building",
        _ES: "tu línea base anterior ({previous}); la propia aquí aún se construye",
    },
    "reference.population": {
        _EN: "a population reference for your age and sex, not your own baseline",
        _ES: "una referencia de población para tu edad y sexo, no tu propia línea base",
    },
    "card.indicators": {
        _EN: "What is measured",
        _ES: "Qué se mide",
    },
    "card.latest": {
        _EN: "Latest: {value}",
        _ES: "Último: {value}",
    },
    "card.no_reading": {
        _EN: "No reading yet",
        _ES: "Sin lecturas todavía",
    },
    "card.trend": {
        _EN: "Latest readings and the range they are compared with",
        _ES: "Últimas lecturas y el rango con el que se comparan",
    },
    "card.trend_empty": {
        _EN: "Not enough readings to draw a trend yet.",
        _ES: "Todavía no hay lecturas suficientes para dibujar una tendencia.",
    },
    "card.suggestion": {
        _EN: "Suggestion",
        _ES: "Sugerencia",
    },
    "escalation.self_care": {
        _EN: "Keep measuring and look after yourself.",
        _ES: "Sigue midiendo y cuídate.",
    },
    "escalation.crew_cmo": {
        _EN: "Consider telling the crew medical officer (CMO).",
        _ES: "Considera avisar al oficial médico de la tripulación (CMO).",
    },
    "escalation.ground_surgeon": {
        _EN: "Consider asking the flight surgeon on the ground to review it.",
        _ES: "Considera pedir al cirujano de vuelo en Tierra que lo revise.",
    },
    "card.nothing_sent": {
        _EN: "Nothing is sent unless you confirm it.",
        _ES: "Nada se envía si no lo confirmas.",
    },
    "card.what_to_do": {
        _EN: "What you can do",
        _ES: "Qué puedes hacer",
    },
    "card.todo.measure": {
        _EN: "Keep measuring: more days make your baseline more reliable.",
        _ES: "Sigue midiendo: más días hacen tu línea base más confiable.",
    },
    "card.todo.read": {
        _EN: "Read the reason: it says what the color was compared with.",
        _ES: "Lee la razón: dice con qué se comparó el color.",
    },
    "card.todo.escalate": {
        _EN: "If it stays amber or red, consider the suggestion above.",
        _ES: "Si sigue en ámbar o rojo, considera la sugerencia de arriba.",
    },
    "card.source": {
        _EN: "Source: NASA Human Research Program, risks of human spaceflight.",
        _ES: "Fuente: Programa de Investigación Humana de la NASA, riesgos del vuelo"
        " espacial humano.",
    },
    "card.source_open": {
        _EN: "Open the NASA page",
        _ES: "Abrir la página de la NASA",
    },
    "indicator.resting_hr": {
        _EN: "Resting pulse",
        _ES: "Pulso en reposo",
    },
    "indicator.systolic_bp": {
        _EN: "Systolic blood pressure",
        _ES: "Presión arterial sistólica",
    },
    "indicator.diastolic_bp": {
        _EN: "Diastolic blood pressure",
        _ES: "Presión arterial diastólica",
    },
    "indicator.blood_glucose": {
        _EN: "Blood glucose",
        _ES: "Glucosa en sangre",
    },
    "indicator.body_temp": {
        _EN: "Body temperature",
        _ES: "Temperatura corporal",
    },
    "indicator.sleep_hours": {
        _EN: "Sleep",
        _ES: "Sueño",
    },
    "indicator.mood": {
        _EN: "Mood",
        _ES: "Ánimo",
    },
    "indicator.spo2": {
        _EN: "Oxygen saturation",
        _ES: "Saturación de oxígeno",
    },
    "indicator.orthostatic_hr_delta": {
        _EN: "Pulse change on standing",
        _ES: "Cambio del pulso al ponerse de pie",
    },
    "indicator.vestibular_symptoms": {
        _EN: "Dizziness and balance symptoms",
        _ES: "Síntomas de mareo y equilibrio",
    },
    "indicator.tandem_walk_ok": {
        _EN: "Walk-in-a-line test",
        _ES: "Prueba de caminar en línea",
    },
    "value.yes": {
        _EN: "yes",
        _ES: "sí",
    },
    "value.no": {
        _EN: "no",
        _ES: "no",
    },
    "unit.points": {
        _EN: "points",
        _ES: "puntos",
    },
    "part.open": {
        _EN: "Open",
        _ES: "Abrir",
    },
    "summary.systems": {
        _EN: "Body systems",
        _ES: "Sistemas del cuerpo",
    },
    "summary.short.ok": {
        _EN: "In range",
        _ES: "En rango",
    },
    "summary.short.watch": {
        _EN: "Outside",
        _ES: "Fuera",
    },
    "summary.short.act": {
        _EN: "Far outside",
        _ES: "Muy fuera",
    },
    "summary.short.insufficient_data": {
        _EN: "No data yet",
        _ES: "Sin datos aún",
    },
    "summary.short.nothing": {
        _EN: "Not measured",
        _ES: "Sin medición",
    },
    "summary.checkin": {
        _EN: "Today's check-in",
        _ES: "Chequeo de hoy",
    },
    "summary.pulse_done": {
        _EN: "Pulse recorded",
        _ES: "Pulso registrado",
    },
    "summary.pulse_todo": {
        _EN: "Pulse not recorded yet",
        _ES: "Pulso aún sin registrar",
    },
    "summary.mood_done": {
        _EN: "Mood recorded",
        _ES: "Ánimo registrado",
    },
    "summary.mood_todo": {
        _EN: "Mood not recorded yet",
        _ES: "Ánimo aún sin registrar",
    },
    "summary.regularity": {
        _EN: "Regularity",
        _ES: "Constancia",
    },
    "summary.days": {
        _EN: "{n} of 7 days with readings",
        _ES: "{n} de 7 días con lecturas",
    },
    "summary.regularity_note": {
        _EN: "This counts how often you measure, not how you are.",
        _ES: "Esto cuenta con qué frecuencia mides, no cómo estás.",
    },
    "summary.baseline": {
        _EN: "Your baseline here",
        _ES: "Tu línea base aquí",
    },
    "summary.baseline_value": {
        _EN: "Ready for {ready} of {total} indicators",
        _ES: "Lista para {ready} de {total} indicadores",
    },
    "summary.baseline_none": {
        _EN: "No readings in this space yet",
        _ES: "Aún no hay lecturas en este espacio",
    },
    "summary.baseline_note": {
        _EN: "It gets better with every day you measure.",
        _ES: "Mejora con cada día que mides.",
    },
    "summary.attention": {
        _EN: "Needs your attention",
        _ES: "Requiere tu atención",
    },
    "summary.attention_none": {
        _EN: "Nothing is outside the range it is compared with today.",
        _ES: "Hoy nada está fuera del rango con el que se compara.",
    },
    "summary.latest": {
        _EN: "Latest readings",
        _ES: "Últimas lecturas",
    },
    "summary.col.indicator": {
        _EN: "Indicator",
        _ES: "Indicador",
    },
    "summary.col.latest": {
        _EN: "Latest",
        _ES: "Último",
    },
    "summary.col.state": {
        _EN: "State",
        _ES: "Estado",
    },
    "summary.col.compared": {
        _EN: "Compared with",
        _ES: "Comparado con",
    },
    "summary.open_body": {
        _EN: "See it on the body",
        _ES: "Verlo en el cuerpo",
    },
    "share.title": {
        _EN: "Share with the ground team",
        _ES: "Compartir con el equipo en Tierra",
    },
    "share.note": {
        _EN: "Nothing is sent unless you confirm it. You choose what goes.",
        _ES: "Nada se envía si no lo confirmas. Tú eliges qué va.",
    },
    "share.attention": {
        _EN: "Select what needs attention",
        _ES: "Seleccionar lo que requiere atención",
    },
    "share.all": {
        _EN: "Select all",
        _ES: "Seleccionar todo",
    },
    "share.clear": {
        _EN: "Clear the selection",
        _ES: "Quitar la selección",
    },
    "share.nothing": {
        _EN: "Nothing selected yet.",
        _ES: "Aún no hay nada seleccionado.",
    },
    "share.summary": {
        _EN: "{readings} readings and {states} states will be sent as a standard HL7 FHIR package.",
        _ES: "Se enviarán {readings} lecturas y {states} estados como un paquete "
        "estándar HL7 FHIR.",
    },
    "share.confirm": {
        _EN: "I confirm I want to send this to the ground team.",
        _ES: "Confirmo que quiero enviar esto al equipo en Tierra.",
    },
    "share.send": {
        _EN: "Send to the ground team",
        _ES: "Enviar al equipo en Tierra",
    },
    "share.sent_title": {
        _EN: "Sent packages",
        _ES: "Paquetes enviados",
    },
    "share.sent_empty": {
        _EN: "Nothing sent yet.",
        _ES: "Todavía no has enviado nada.",
    },
    "share.sent_line": {
        _EN: "Sent on day {label} · {readings} readings, {states} states",
        _ES: "Enviado el día {label} · {readings} lecturas, {states} estados",
    },
    "share.in_transit": {
        _EN: "In transit: it arrives after {minutes} minutes of simulated time.",
        _ES: "En camino: llega tras {minutes} minutos de tiempo simulado.",
    },
    "share.delivered": {
        _EN: "Delivered to the ground inbox (simulated).",
        _ES: "Entregado a la bandeja de Tierra (simulado).",
    },
    "share.delivered_linked": {
        _EN: "Delivered to the ground base.",
        _ES: "Entregado a la base en Tierra.",
    },
    "share.sim_note": {
        _EN: "The ground base is simulated: it is not built yet, so delivery only "
        "moves the package to a local inbox.",
        _ES: "La base en Tierra es simulada: aún no existe, así que la entrega solo "
        "mueve el paquete a una bandeja local.",
    },
    "share.waiting_ground": {
        _EN: "The ground base did not answer. The package is kept and will be sent again.",
        _ES: "La base en Tierra no respondió. El paquete se conserva y se enviará de nuevo.",
    },
    "share.linked_note": {
        _EN: "Sent to the ground base (a separate local system). It shows the package only "
        "after the simulated communication delay.",
        _ES: "Enviado a la base en Tierra (un sistema local aparte). Solo muestra el paquete "
        "tras el retraso de comunicación simulado.",
    },
    "share.show_data": {
        _EN: "Show the FHIR data",
        _ES: "Ver los datos FHIR",
    },
    "share.data_title": {
        _EN: "What was sent (FHIR)",
        _ES: "Lo que se envió (FHIR)",
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


# Every acronym the interface shows is spelled out here (D-024). A test fails if a new acronym
# appears in ``STRINGS`` without an entry, so nothing is left unexplained by accident.
GLOSSARY: tuple[dict[Language, tuple[str, str]], ...] = (
    {
        _EN: ("bpm", "beats per minute: how many times the heart beats in one minute"),
        _ES: (
            "lpm",
            "latidos por minuto (bpm en inglés): cuántas veces late el corazón en un minuto",
        ),
    },
    {
        _EN: ("AI", "artificial intelligence: software that can generate images or text"),
        _ES: (
            "IA",
            "inteligencia artificial (AI en inglés): software que puede generar imágenes o texto",
        ),
    },
    {
        _EN: (
            "NIH",
            "National Institutes of Health: the main United States government agency "
            "for health research",
        ),
        _ES: (
            "NIH",
            "Institutos Nacionales de Salud de Estados Unidos: la principal agencia del gobierno "
            "estadounidense para la investigación en salud",
        ),
    },
    {
        _EN: (
            "CMO",
            "crew medical officer: the crew member trained to give first medical care",
        ),
        _ES: (
            "CMO",
            "oficial médico de la tripulación (crew medical officer): el integrante "
            "entrenado para dar la primera atención médica",
        ),
    },
    {
        _EN: (
            "NASA",
            "National Aeronautics and Space Administration, the United States space agency",
        ),
        _ES: (
            "NASA",
            "Administración Nacional de Aeronáutica y del Espacio, la agencia espacial "
            "de Estados Unidos",
        ),
    },
    {
        _EN: (
            "FHIR",
            "Fast Healthcare Interoperability Resources: the standard format for exchanging "
            "health data",
        ),
        _ES: (
            "FHIR",
            "Fast Healthcare Interoperability Resources: el formato estándar para intercambiar "
            "datos de salud",
        ),
    },
    {
        _EN: (
            "HL7",
            "Health Level Seven: the organization that publishes the FHIR standard",
        ),
        _ES: (
            "HL7",
            "Health Level Seven: la organización que publica el estándar FHIR",
        ),
    },
    {
        _EN: ("AST", "astronaut: the first letters of your personal code, AST-0000"),
        _ES: ("AST", "astronauta: las primeras letras de tu código personal, AST-0000"),
    },
)


def glossary_terms(language: Language) -> frozenset[str]:
    return frozenset(entry[language][0] for entry in GLOSSARY)


def translate(key: str, language: Language, **params: object) -> str:
    """The text for ``key``; an unknown key or a missing parameter raises ``KeyError``."""
    return STRINGS[key][language].format(**params)
