"""Interface texts: English is the source, Spanish the translation (D-016).

Only say what is true of the prototype: no diagnosis, no unverifiable promise
(AGENTS.md, section 6).
"""

from __future__ import annotations

from crew_self_check.core.reasons import Language

_EN, _ES = Language.EN, Language.ES

# Keys that are the same in both languages on purpose (names and examples).
SAME_IN_BOTH = frozenset(
    {"app.name", "login.code_hint", "value.no", "pewonu.title", "pewonu.wod", "food.tortilla"}
)

STRINGS: dict[str, dict[Language, str]] = {
    "app.name": {_EN: "PeWoNu", _ES: "PeWoNu"},
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
    "hazard.radiation": {_EN: "Space radiation", _ES: "Radiación espacial"},
    "hazard.radiation.what": {
        _EN: "Invisible radiation is one of the most dangerous parts of spaceflight.",
        _ES: "La radiación invisible es una de las partes más peligrosas del vuelo espacial.",
    },
    "hazard.isolation": {_EN: "Isolation and confinement", _ES: "Aislamiento y confinamiento"},
    "hazard.isolation.what": {
        _EN: "Crews living in small spaces far from Earth for long periods can show "
        "behavioral changes.",
        _ES: "Las tripulaciones que viven en espacios pequeños lejos de la Tierra durante "
        "mucho tiempo pueden mostrar cambios de comportamiento.",
    },
    "hazard.distance": {_EN: "Distance from Earth", _ES: "Distancia de la Tierra"},
    "hazard.distance.what": {
        _EN: "Getting supplies, instructions and medical care from home gets harder the "
        "farther astronauts travel.",
        _ES: "Recibir suministros, instrucciones y atención médica desde casa se vuelve más "
        "difícil cuanto más lejos viajan los astronautas.",
    },
    "hazard.gravity": {_EN: "Gravity fields", _ES: "Campos gravitatorios"},
    "hazard.gravity.what": {
        _EN: "The body must adjust to different gravity levels, including the return to Earth.",
        _ES: "El cuerpo debe adaptarse a distintos niveles de gravedad, incluido el regreso "
        "a la Tierra.",
    },
    "hazard.environment": {
        _EN: "Hostile and closed environments",
        _ES: "Ambientes hostiles y cerrados",
    },
    "hazard.environment.what": {
        _EN: "Keeping a spacecraft's temperature, pressure, light and air safe is difficult.",
        _ES: "Mantener seguros la temperatura, la presión, la luz y el aire de una nave es "
        "difícil.",
    },
    "hazard.source": {
        _EN: "Source: NASA Human Research Program, the five hazards of human spaceflight.",
        _ES: "Fuente: Programa de Investigación Humana de la NASA, los cinco peligros del "
        "vuelo espacial humano.",
    },
    "case.hazard_label": {
        _EN: "NASA hazard it stresses",
        _ES: "Peligro de la NASA que pone a prueba",
    },
    "case.system_label": {_EN: "How the system approaches it", _ES: "Cómo lo aborda el sistema"},
    "case.your_case": {_EN: "Your case in this demo", _ES: "Tu caso en esta demostración"},
    "case.simulated": {
        _EN: "Fictitious astronaut with simulated data, not a real person.",
        _ES: "Astronauta ficticio con datos simulados, no una persona real.",
    },
    "case.crew-01.title": {_EN: "Arrival adaptation", _ES: "Adaptación a la llegada"},
    "case.crew-01.story": {
        _EN: "Two weeks of personal history on Earth. Sleep dips in transit; on arrival the "
        "pulse, the pulse change on standing and the balance symptoms rise.",
        _ES: "Dos semanas de historial personal en la Tierra. El sueño baja en tránsito; al "
        "llegar suben el pulso, el cambio de pulso al pararse y los síntomas de equilibrio.",
    },
    "case.crew-01.system": {
        _EN: "Each reading is compared with this astronaut's own baseline in each place, the "
        "comparison is labelled when they change place, and when a change lasts the "
        "suggestion is to tell the crew medical officer.",
        _ES: "Cada lectura se compara con la línea base de este astronauta en cada lugar, la "
        "comparación se rotula cuando cambia de lugar, y si un cambio dura se sugiere "
        "avisar al oficial médico de la tripulación.",
    },
    "case.crew-02.title": {
        _EN: "No history: pulse counted by hand",
        _ES: "Sin historial: pulso contado a mano",
    },
    "case.crew-02.story": {
        _EN: "No personal history, and only the resting pulse, counted by hand. There is "
        "nothing of their own to compare with, and on arrival the pulse climbs far above "
        "the usual.",
        _ES: "Sin historial personal y solo el pulso en reposo, contado a mano. No hay nada "
        "propio con qué comparar, y al llegar el pulso sube muy por encima de lo habitual.",
    },
    "case.crew-02.system": {
        _EN: "With no baseline the pulse is compared with a labelled population reference; "
        "everything else stays gray instead of guessing. A pulse far outside turns red and "
        "the suggestion is to ask the flight surgeon to review it.",
        _ES: "Sin línea base el pulso se compara con una referencia poblacional rotulada; "
        "todo lo demás queda en gris en vez de adivinar. Un pulso muy fuera de rango pasa a "
        "rojo y se sugiere pedir revisión al cirujano de vuelo.",
    },
    "case.crew-03.title": {_EN: "Isolation: sleep and mood", _ES: "Aislamiento: sueño y ánimo"},
    "case.crew-03.story": {
        _EN: "Two weeks of personal history on Earth. In transit sleep falls and mood slips, "
        "while the pulse, the blood pressure and the balance stay in range.",
        _ES: "Dos semanas de historial personal en la Tierra. En tránsito el sueño baja y el "
        "ánimo decae, mientras el pulso, la presión y el equilibrio siguen en rango.",
    },
    "case.crew-03.system": {
        _EN: "Sleep and mood are flagged against the Earth baseline, then against the "
        "astronaut's own range in the spacecraft, with the suggestion to tell the crew "
        "medical officer. What stays in range stays green.",
        _ES: "El sueño y el ánimo se marcan contra la línea base de la Tierra y luego contra "
        "el rango propio en la nave, con la sugerencia de avisar al oficial médico. Lo que "
        "sigue en rango sigue en verde.",
    },
    "login.demo_title": {
        _EN: "Simulated demo crew",
        _ES: "Tripulación de demostración (simulada)",
    },
    "login.demo_codes": {_EN: "Try {codes}", _ES: "Prueba con {codes}"},
    "login.demo_pick": {
        _EN: "Three cases, each stressing a different NASA hazard. Tap one to fill the code.",
        _ES: "Tres casos, cada uno pone a prueba un peligro distinto de la NASA. Toca uno para "
        "llenar el código.",
    },
    "login.private": {
        _EN: "Your code opens only your own profile on this computer.",
        _ES: "Tu código abre solo tu propio perfil en este equipo.",
    },
    "nav.home": {_EN: "Home", _ES: "Inicio"},
    "nav.checkin": {_EN: "Check-in", _ES: "Chequeo"},
    "nav.body": {_EN: "Body", _ES: "Cuerpo"},
    "nav.summary": {_EN: "Summary", _ES: "Resumen"},
    "nav.data": {_EN: "Data", _ES: "Datos"},
    "part.data.title": {_EN: "Data intake", _ES: "Ingreso de datos"},
    "part.data.body": {
        _EN: "Every reading that came in, from which source, and what it shows.",
        _ES: "Cada lectura que entró, de qué fuente y qué muestra.",
    },
    "intake.empty": {
        _EN: "No data has come in yet.",
        _ES: "Todavía no ha entrado ningún dato.",
    },
    "intake.title": {_EN: "Data intake", _ES: "Ingreso de datos"},
    "intake.intro": {
        _EN: "In real use your devices send these readings by themselves. In this demo they "
        "are pre-loaded and arrive as the journey moves, so you can see them in the system.",
        _ES: "En uso real tus dispositivos envían estas lecturas solos. En esta demostración "
        "están precargadas y entran a medida que avanza el viaje, para que las veas en el "
        "sistema.",
    },
    "intake.totals": {
        _EN: "{n} readings in · {covered} of {total} indicators",
        _ES: "{n} lecturas ingresadas · {covered} de {total} indicadores",
    },
    "intake.sources_title": {_EN: "Where the data comes from", _ES: "De dónde vienen los datos"},
    "intake.source.wearable": {_EN: "Watch and band", _ES: "Reloj y pulsera"},
    "intake.source.wearable.what": {
        _EN: "Sends blood pressure, temperature, sleep and more by itself (simulated).",
        _ES: "Envía presión, temperatura, sueño y más por sí solo (simulado).",
    },
    "intake.source.survey": {_EN: "Short questions", _ES: "Preguntas cortas"},
    "intake.source.survey.what": {
        _EN: "Mood, balance symptoms and the line-walk test.",
        _ES: "Ánimo, síntomas de equilibrio y la prueba de caminar en línea.",
    },
    "intake.source.hand_pulse": {_EN: "Pulse counted by hand", _ES: "Pulso contado a mano"},
    "intake.source.hand_pulse.what": {
        _EN: "The resting pulse, counted on the wrist.",
        _ES: "El pulso en reposo, contado en la muñeca.",
    },
    "intake.source.entered": {_EN: "Entered by you here", _ES: "Ingresado por ti aquí"},
    "intake.source.entered.what": {
        _EN: "What you record in the check-in.",
        _ES: "Lo que registras en el chequeo.",
    },
    "intake.readings": {
        _EN: "{n} readings · last on {last}",
        _ES: "{n} lecturas · la última el {last}",
    },
    "intake.feed_title": {_EN: "Latest days", _ES: "Últimos días"},
    "intake.feed_line": {
        _EN: "{total} readings: {parts}",
        _ES: "{total} lecturas: {parts}",
    },
    "intake.short.wearable": {_EN: "device", _ES: "dispositivo"},
    "intake.short.survey": {_EN: "questions", _ES: "preguntas"},
    "intake.short.hand_pulse": {_EN: "by hand", _ES: "a mano"},
    "intake.short.entered": {_EN: "entered", _ES: "ingresadas"},
    "intake.shows_title": {_EN: "What this data shows now", _ES: "Qué muestra ahora este dato"},
    "intake.shows_body": {
        _EN: "Each color compares your readings with your own baseline in this place.",
        _ES: "Cada color compara tus lecturas con tu propia línea base en este lugar.",
    },
    "intake.open_body": {_EN: "Open the body view", _ES: "Abrir la vista del cuerpo"},
    "intake.origin_title": {_EN: "Origin of the data", _ES: "Origen de los datos"},
    "intake.origin_simulated": {
        _EN: "Simulated analog scenario: fictitious crew, not data of real astronauts.",
        _ES: "Escenario análogo simulado: tripulación ficticia, no son datos de astronautas "
        "reales.",
    },
    "intake.origin_other": {
        _EN: "Data from the sources listed above.",
        _ES: "Datos de las fuentes listadas arriba.",
    },
    "intake.origin_real": {
        _EN: "In a real mission the readings would arrive from the crew's devices; the cases "
        "follow the NASA Human Research Program hazards.",
        _ES: "En una misión real las lecturas llegarían de los dispositivos de la tripulación; "
        "los casos siguen los peligros del Programa de Investigación Humana de la NASA.",
    },
    "nav.hazards": {
        _EN: "Hazards",
        _ES: "Peligros",
    },
    "part.hazards.title": {
        _EN: "Mission hazards",
        _ES: "Peligros de la misión",
    },
    "part.hazards.body": {
        _EN: "The five NASA hazards of spaceflight and which of your indicators each one touches.",
        _ES: "Los cinco peligros del vuelo espacial de la NASA y qué indicadores tuyos toca cada "
        "uno.",
    },
    "hazards.title": {
        _EN: "The five hazards of human spaceflight",
        _ES: "Los cinco peligros del vuelo espacial humano",
    },
    "hazards.intro": {
        _EN: "NASA's Human Research Program groups the risks of a long mission into five hazards. "
        "Here is what each one means where you are now and which of your own indicators it "
        "touches.",
        _ES: "El Programa de Investigación Humana de la NASA agrupa los riesgos de una misión "
        "larga en cinco peligros. Aquí ves qué significa cada uno donde estás ahora y qué "
        "indicadores tuyos toca.",
    },
    "hazards.you_are": {
        _EN: "You are in: {place}",
        _ES: "Estás en: {place}",
    },
    "hazards.assumption": {
        _EN: "Which indicator belongs to which hazard is our reading of the NASA pages, not an "
        "official list.",
        _ES: "Qué indicador pertenece a qué peligro es nuestra lectura de las páginas de la NASA, "
        "no es una lista oficial.",
    },
    "hazards.touches": {
        _EN: "Your indicators it touches",
        _ES: "Tus indicadores que toca",
    },
    "hazards.not_measured": {
        _EN: "Not measured by this prototype",
        _ES: "Este prototipo no lo mide",
    },
    "hazards.not_measured.radiation": {
        _EN: "Radiation needs a dosimeter. The Canadian Space Agency is developing a "
        "compact, autonomous instrument (the Canadian Active Neutron Spectrometer) to "
        "measure neutron radiation exposure in space.",
        _ES: "La radiación necesita un dosímetro. La Agencia Espacial Canadiense desarrolla "
        "un instrumento compacto y autónomo (el espectrómetro activo canadiense de "
        "neutrones) para medir la exposición a neutrones en el espacio.",
    },
    "hazards.comm": {
        _EN: "A message to the ground takes about {minutes} minutes in this demo, so you act first"
        " on board and then ask the ground.",
        _ES: "Un mensaje a Tierra tarda unos {minutes} minutos en esta demostración, así que "
        "actúas primero a bordo y luego consultas a Tierra.",
    },
    "hazards.comm.what": {
        _EN: "The app keeps working without the ground and sends nothing until you confirm.",
        _ES: "La app funciona sin Tierra y no envía nada hasta que lo confirmes.",
    },
    "hazards.matrix_title": {
        _EN: "Where each hazard applies",
        _ES: "Dónde aplica cada peligro",
    },
    "hazards.stressed_by": {
        _EN: "Stressed by the case of {code}",
        _ES: "Lo pone a prueba el caso de {code}",
    },
    "hazards.state.comm": {
        _EN: "About the delay to Earth",
        _ES: "Sobre el retraso con la Tierra",
    },
    "hazards.state.flagged": {
        _EN: "Needs attention",
        _ES: "Requiere atención",
    },
    "hazards.state.ok": {
        _EN: "In range",
        _ES: "En rango",
    },
    "hazards.state.unknown": {
        _EN: "Not enough data yet",
        _ES: "Aún sin datos suficientes",
    },
    "hazards.here": {
        _EN: "Where you are now",
        _ES: "Donde estás ahora",
    },
    "hazard.radiation.here.earth": {
        _EN: "The atmosphere and Earth's magnetic field protect you.",
        _ES: "La atmósfera y el campo magnético de la Tierra te protegen.",
    },
    "hazard.radiation.here.spacecraft": {
        _EN: "Beyond Earth's protection: exposure to space radiation.",
        _ES: "Fuera de la protección de la Tierra: exposición a la radiación espacial.",
    },
    "hazard.radiation.here.planet": {
        _EN: "On the surface the thin atmosphere gives little protection.",
        _ES: "En la superficie la atmósfera delgada protege poco.",
    },
    "hazard.isolation.here.earth": {
        _EN: "Your usual people and surroundings are close.",
        _ES: "Tu gente y tu entorno habitual están cerca.",
    },
    "hazard.isolation.here.spacecraft": {
        _EN: "A small crew in a small space, far from home.",
        _ES: "Una tripulación pequeña en un espacio pequeño, lejos de casa.",
    },
    "hazard.isolation.here.planet": {
        _EN: "A small crew in a base, far from home.",
        _ES: "Una tripulación pequeña en una base, lejos de casa.",
    },
    "hazard.distance.here.earth": {
        _EN: "Help and supplies are close.",
        _ES: "La ayuda y los suministros están cerca.",
    },
    "hazard.distance.here.spacecraft": {
        _EN: "Messages take minutes and help cannot arrive quickly.",
        _ES: "Los mensajes tardan minutos y la ayuda no puede llegar rápido.",
    },
    "hazard.distance.here.planet": {
        _EN: "Messages take minutes and help is far away.",
        _ES: "Los mensajes tardan minutos y la ayuda está lejos.",
    },
    "hazard.gravity.here.earth": {
        _EN: "Normal gravity.",
        _ES: "Gravedad normal.",
    },
    "hazard.gravity.here.spacecraft": {
        _EN: "Microgravity: the body adjusts and loses conditioning.",
        _ES: "Microgravedad: el cuerpo se adapta y pierde acondicionamiento.",
    },
    "hazard.gravity.here.planet": {
        _EN: "Partial gravity: the body adjusts again.",
        _ES: "Gravedad parcial: el cuerpo se adapta de nuevo.",
    },
    "hazard.environment.here.earth": {
        _EN: "A familiar, open environment.",
        _ES: "Un entorno conocido y abierto.",
    },
    "hazard.environment.here.spacecraft": {
        _EN: "A closed environment: the ship manages air, temperature and pressure.",
        _ES: "Un entorno cerrado: la nave maneja el aire, la temperatura y la presión.",
    },
    "hazard.environment.here.planet": {
        _EN: "A habitat: the base manages air, temperature and pressure.",
        _ES: "Un hábitat: la base maneja el aire, la temperatura y la presión.",
    },
    "voice.prompt.1": {
        _EN: "Tell me about someone at home you are thinking of today.",
        _ES: "Cuéntame de alguien de casa en quien piensas hoy.",
    },
    "voice.prompt.2": {
        _EN: "What has been on your mind about the mission lately?",
        _ES: "¿Qué ha estado en tu mente últimamente sobre la misión?",
    },
    "voice.prompt.3": {
        _EN: "Describe a place from home that you miss, as if you were walking through it.",
        _ES: "Describe un lugar de casa que extrañas, como si caminaras por él.",
    },
    "voice.prompt.4": {
        _EN: "What is something that has surprised you since you left?",
        _ES: "¿Qué es algo que te ha sorprendido desde que partiste?",
    },
    "voice.prompt.5": {
        _EN: "Talk about what you want to do when this mission is over.",
        _ES: "Habla de lo que quieres hacer cuando termine esta misión.",
    },
    "voice.prompt.6": {
        _EN: "What was the hardest part of this week, and how did you get through it?",
        _ES: "¿Qué fue lo más difícil de esta semana y cómo lo superaste?",
    },
    "voice.prompt.7": {
        _EN: "Tell a story about a moment with your crew that you will remember.",
        _ES: "Cuenta una historia de un momento con tu tripulación que recordarás.",
    },
    "voice.prompt.8": {
        _EN: "What do you wish people on Earth understood about where you are?",
        _ES: "¿Qué te gustaría que la gente en la Tierra entendiera de dónde estás?",
    },
    "nav.voice": {
        _EN: "Voice log",
        _ES: "Bitácora de voz",
    },
    "voice.title": {
        _EN: "Voice log",
        _ES: "Bitácora de voz",
    },
    "voice.intro": {
        _EN: "A moment to let it out. Talk for as long as you want about the question below. What "
        "you say is not recorded or saved: only a few numbers about how your voice sounds.",
        _ES: "Un momento para desahogarte. Habla el tiempo que quieras sobre la pregunta de abajo."
        " Lo que digas no se graba ni se guarda: solo unos números sobre cómo suena tu voz.",
    },
    "voice.another": {
        _EN: "Another question",
        _ES: "Otra pregunta",
    },
    "voice.start": {
        _EN: "Start talking",
        _ES: "Empezar a hablar",
    },
    "voice.stop": {
        _EN: "I am done",
        _ES: "Terminé",
    },
    "voice.listening": {
        _EN: "Listening… take your time.",
        _ES: "Escuchando… tómate tu tiempo.",
    },
    "voice.elapsed": {
        _EN: "{seconds} s elapsed",
        _ES: "{seconds} s transcurridos",
    },
    "voice.analyzing": {
        _EN: "Turning your voice into numbers…",
        _ES: "Convirtiendo tu voz en números…",
    },
    "voice.no_mic": {
        _EN: "No microphone was found on this computer.",
        _ES: "No se encontró un micrófono en este equipo.",
    },
    "voice.use_sample": {
        _EN: "Use a sample voice note (synthetic)",
        _ES: "Usar una nota de voz de muestra (sintética)",
    },
    "voice.sample.usual": {
        _EN: "Sample: usual voice",
        _ES: "Muestra: voz habitual",
    },
    "voice.sample.slower": {
        _EN: "Sample: slower, more pauses",
        _ES: "Muestra: más lenta, con más pausas",
    },
    "voice.synthetic": {
        _EN: "This is a generated sample, not your voice.",
        _ES: "Esta es una muestra generada, no tu voz.",
    },
    "voice.discarded": {
        _EN: "The audio was discarded. Only these numbers were kept.",
        _ES: "El audio se descartó. Solo se guardaron estos números.",
    },
    "voice.result_title": {
        _EN: "Your voice today compared with your usual",
        _ES: "Tu voz de hoy frente a tu habitual",
    },
    "voice.building": {
        _EN: "Building your voice baseline: note {n} of {needed}. Keep talking on other days.",
        _ES: "Construyendo tu línea base de voz: nota {n} de {needed}. Sigue hablando otros días.",
    },
    "voice.level.usual": {
        _EN: "Your voice sounds like your usual.",
        _ES: "Tu voz suena como la habitual.",
    },
    "voice.level.different": {
        _EN: "Your voice differs from your usual in several ways.",
        _ES: "Tu voz se diferencia de la habitual en varios aspectos.",
    },
    "voice.reference.personal": {
        _EN: "Compared with your own notes in this place.",
        _ES: "Comparado con tus propias notas en este lugar.",
    },
    "voice.reference.transition": {
        _EN: "Compared with your notes in the previous place ({previous}), while your notes here "
        "build up.",
        _ES: "Comparado con tus notas del lugar anterior ({previous}), mientras se acumulan las de"
        " aquí.",
    },
    "voice.not_a_diagnosis": {
        _EN: "Experimental. These numbers do not say how you feel and do not change any color.",
        _ES: "Experimental. Estos números no dicen cómo te sientes ni cambian ningún color.",
    },
    "voice.shared": {
        _EN: "Shared with the ground base: only these numbers. You agreed to this when you joined "
        "the mission.",
        _ES: "Compartido con la base en Tierra: solo estos números. Lo aceptaste al unirte a la "
        "misión.",
    },
    "voice.not_shared": {
        _EN: "Not shared: the ground base is not connected.",
        _ES: "No compartido: la base en Tierra no está conectada.",
    },
    "voice.again": {
        _EN: "Record another note",
        _ES: "Grabar otra nota",
    },
    "voice.problem.too_short": {
        _EN: "The note was too short. Talk for at least 5 seconds.",
        _ES: "La nota fue muy corta. Habla al menos 5 segundos.",
    },
    "voice.problem.low_signal": {
        _EN: "I could barely hear you. Check the microphone and try again.",
        _ES: "Casi no te escuché. Revisa el micrófono y vuelve a intentar.",
    },
    "voice.problem.clipping": {
        _EN: "The sound was too loud and distorted. Move back a little.",
        _ES: "El sonido fue muy fuerte y se distorsionó. Aléjate un poco.",
    },
    "voice.problem.too_few_voiced": {
        _EN: "There was too little clear voice to measure.",
        _ES: "Hubo muy poca voz clara para medir.",
    },
    "voice.feature.pitchMeanHz": {
        _EN: "Pitch",
        _ES: "Tono",
    },
    "voice.feature.pitchVariation": {
        _EN: "Pitch variation",
        _ES: "Variación del tono",
    },
    "voice.feature.speechRate": {
        _EN: "Speech rate",
        _ES: "Ritmo del habla",
    },
    "voice.feature.pauseRatio": {
        _EN: "Pauses",
        _ES: "Pausas",
    },
    "voice.feature.loudnessDb": {
        _EN: "Loudness",
        _ES: "Volumen",
    },
    "voice.dir.pitchMeanHz.up": {
        _EN: "higher",
        _ES: "más agudo",
    },
    "voice.dir.pitchMeanHz.down": {
        _EN: "lower",
        _ES: "más grave",
    },
    "voice.dir.pitchVariation.up": {
        _EN: "more varied",
        _ES: "más variado",
    },
    "voice.dir.pitchVariation.down": {
        _EN: "flatter",
        _ES: "más plano",
    },
    "voice.dir.speechRate.up": {
        _EN: "faster",
        _ES: "más rápido",
    },
    "voice.dir.speechRate.down": {
        _EN: "slower",
        _ES: "más lento",
    },
    "voice.dir.pauseRatio.up": {
        _EN: "more pauses",
        _ES: "más pausas",
    },
    "voice.dir.pauseRatio.down": {
        _EN: "fewer pauses",
        _ES: "menos pausas",
    },
    "voice.dir.loudnessDb.up": {
        _EN: "louder",
        _ES: "más fuerte",
    },
    "voice.dir.loudnessDb.down": {
        _EN: "softer",
        _ES: "más suave",
    },
    "voice.same": {
        _EN: "as usual",
        _ES: "como siempre",
    },
    "part.voice.title": {
        _EN: "Voice log",
        _ES: "Bitácora de voz",
    },
    "part.voice.body": {
        _EN: "Talk about whatever you need. Only numbers about your voice are kept.",
        _ES: "Habla de lo que necesites. Solo se guardan números sobre tu voz.",
    },
    "stage.data_title": {
        _EN: "Your data",
        _ES: "Tus datos",
    },
    "zone.wrist": {
        _EN: "Pulse · wrist",
        _ES: "Pulso · muñeca",
    },
    "stage.hint": {
        _EN: "Tap a zone. The wrist opens your pulse.",
        _ES: "Toca una zona. La muñeca abre tu pulso.",
    },
    "journey.play": {
        _EN: "Play journey",
        _ES: "Reproducir viaje",
    },
    "journey.pause": {
        _EN: "Pause",
        _ES: "Pausar",
    },
    "pulse.tab.data": {
        _EN: "Collected data",
        _ES: "Datos recopilados",
    },
    "pulse.tab.hand": {
        _EN: "Measure by hand",
        _ES: "Medir a mano",
    },
    "pulse.take_now": {
        _EN: "Take my pulse now",
        _ES: "Tomar mi pulso ahora",
    },
    "pulse.where_from": {
        _EN: "Where it comes from",
        _ES: "De dónde viene",
    },
    "pulse.latest": {
        _EN: "Latest resting pulse",
        _ES: "Último pulso en reposo",
    },
    "modal.close": {
        _EN: "Close",
        _ES: "Cerrar",
    },
    "bubble.tip": {
        _EN: "How are you? Drag me",
        _ES: "¿Cómo estás? Arrástrame",
    },
    "bubble.label": {
        _EN: "Mood and voice log",
        _ES: "Ánimo y bitácora de voz",
    },
    "bubble.save_continue": {
        _EN: "Save and continue to the voice log",
        _ES: "Guardar y seguir a la bitácora de voz",
    },
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
    "share.sent_voice": {
        _EN: "Sent on day {label} · {voices} voice note (numbers only)",
        _ES: "Enviado el día {label} · {voices} nota de voz (solo números)",
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
    "pewonu.title": {
        _EN: "PeWoNu",
        _ES: "PeWoNu",
    },
    "pewonu.tagline": {
        _EN: "Peace · WOD · Nutrition",
        _ES: "Paz · WOD · Nutrición",
    },
    "pewonu.peace": {
        _EN: "Peace",
        _ES: "Paz",
    },
    "pewonu.peace.sub": {
        _EN: "How are you feeling? Talk it out.",
        _ES: "¿Cómo te sientes? Desahógate.",
    },
    "pewonu.wod": {
        _EN: "WOD",
        _ES: "WOD",
    },
    "pewonu.wod.sub": {
        _EN: "Today's workout on the three machines",
        _ES: "El entrenamiento de hoy en las tres máquinas",
    },
    "pewonu.nutrition": {
        _EN: "Nutrition",
        _ES: "Nutrición",
    },
    "pewonu.nutrition.sub": {
        _EN: "Your food of the day",
        _ES: "Tu comida del día",
    },
    "wod.title": {
        _EN: "Workout of the day",
        _ES: "Entrenamiento del día",
    },
    "wod.total": {
        _EN: "{minutes} min in total",
        _ES: "{minutes} min en total",
    },
    "wod.minutes": {
        _EN: "{minutes} min",
        _ES: "{minutes} minutos",
    },
    "wod.rpe": {
        _EN: "Perceived effort {low} to {high} out of 10",
        _ES: "Esfuerzo percibido de {low} a {high} sobre 10",
    },
    "wod.kind.legs_and_easy_bike": {
        _EN: "Legs and easy bike",
        _ES: "Piernas y bicicleta suave",
    },
    "wod.kind.run_intervals_and_upper": {
        _EN: "Run intervals and upper body",
        _ES: "Intervalos de carrera y torso",
    },
    "wod.kind.steady_bike_and_full": {
        _EN: "Steady bike and full body",
        _ES: "Bicicleta constante y cuerpo completo",
    },
    "wod.kind.steady_run_and_legs": {
        _EN: "Steady run and legs",
        _ES: "Carrera constante y piernas",
    },
    "wod.kind.bike_intervals_and_upper": {
        _EN: "Bike intervals and upper body",
        _ES: "Intervalos en bicicleta y torso",
    },
    "wod.kind.circuit": {
        _EN: "Three-machine circuit",
        _ES: "Circuito de tres máquinas",
    },
    "wod.kind.active_recovery": {
        _EN: "Active recovery",
        _ES: "Recuperación activa",
    },
    "wod.machine.treadmill": {
        _EN: "Treadmill",
        _ES: "Caminadora",
    },
    "wod.machine.cycle": {
        _EN: "Cycle ergometer",
        _ES: "Bicicleta ergométrica",
    },
    "wod.machine.resistive": {
        _EN: "Resistive exercise device",
        _ES: "Dispositivo de ejercicio de resistencia",
    },
    "wod.effort.easy": {
        _EN: "Easy",
        _ES: "Suave",
    },
    "wod.effort.moderate": {
        _EN: "Moderate",
        _ES: "Moderado",
    },
    "wod.effort.hard": {
        _EN: "Hard",
        _ES: "Intenso",
    },
    "wod.focus.intervals": {
        _EN: "Intervals",
        _ES: "Intervalos",
    },
    "wod.focus.steady": {
        _EN: "Steady pace",
        _ES: "Ritmo constante",
    },
    "wod.focus.legs": {
        _EN: "Legs and hips",
        _ES: "Piernas y caderas",
    },
    "wod.focus.upper": {
        _EN: "Upper body",
        _ES: "Torso y brazos",
    },
    "wod.focus.full": {
        _EN: "Full body",
        _ES: "Cuerpo completo",
    },
    "wod.focus.easy": {
        _EN: "Easy pace",
        _ES: "Ritmo suave",
    },
    "wod.adj.lighter_sleep": {
        _EN: ("Shorter and never hard today: your sleep readings are outside your usual range."),
        _ES: (
            "Más corto y sin esfuerzo intenso hoy: tus lecturas de sueño están "
            "fuera de tu rango habitual."
        ),
    },
    "wod.adj.no_treadmill": {
        _EN: (
            "The bike replaces the treadmill today: your balance readings are "
            "outside your usual range."
        ),
        _ES: (
            "La bicicleta reemplaza la caminadora hoy: tus lecturas de equilibrio "
            "están fuera de tu rango habitual."
        ),
    },
    "wod.adj.tell_cmo": {
        _EN: ("Tell the crew medical officer before you train, and keep the effort moderate."),
        _ES: (
            "Avisa al oficial médico de la tripulación antes de entrenar y mantén "
            "el esfuerzo moderado."
        ),
    },
    "wod.adj.mood_note": {
        _EN: (
            "Your mood looks low. Training can help; keep it at a pace you enjoy "
            "and talk to someone you trust."
        ),
        _ES: (
            "Tu ánimo se ve bajo. Entrenar puede ayudar; mantén un ritmo que "
            "disfrutes y habla con alguien de confianza."
        ),
    },
    "wod.adj.extra_loading": {
        _EN: (
            "Time in space lowers the load on your bones, so the resistive device "
            "is the key session of the week."
        ),
        _ES: (
            "El tiempo en el espacio reduce la carga sobre tus huesos, así que el "
            "dispositivo de resistencia es la sesión clave de la semana."
        ),
    },
    "wod.hr": {
        _EN: (
            "Heart-rate reference for your age: about {low} to {high} beats per "
            "minute for moderate effort, with a rough maximum of {maximum}. It is "
            "only a rule of thumb, not a measurement."
        ),
        _ES: (
            "Referencia de pulso para tu edad: unos {low} a {high} latidos por "
            "minuto en esfuerzo moderado, con un máximo aproximado de {maximum}. Es"
            " solo una regla general, no una medición."
        ),
    },
    "wod.energy": {
        _EN: "About {kcal} kcal for this session at your weight (an estimate).",
        _ES: "Unas {kcal} kcal en esta sesión con tu peso (una estimación).",
    },
    "wod.bone": {
        _EN: (
            "Your preflight bone density was {baseline} g/cm². Without exercise, "
            "bone loss in space is about 1 to 2 percent a month (NASA Human "
            "Research Program). After {months} months that would be {low} to {high}"
            " percent. Loading the bones is why this plan always includes resistive"
            " work."
        ),
        _ES: (
            "Tu densidad ósea antes del vuelo fue {baseline} g/cm². Sin ejercicio, "
            "la pérdida ósea en el espacio es de 1 a 2 por ciento al mes (Programa "
            "de Investigación Humana de la NASA). Tras {months} meses serían de "
            "{low} a {high} por ciento. Cargar los huesos es la razón por la que "
            "este plan siempre incluye trabajo de resistencia."
        ),
    },
    "wod.bone_earth": {
        _EN: (
            "Your preflight bone density was {baseline} g/cm². In space, without "
            "exercise, bone loss is about 1 to 2 percent a month (NASA Human "
            "Research Program). Loading the bones is why this plan always includes "
            "resistive work."
        ),
        _ES: (
            "Tu densidad ósea antes del vuelo fue {baseline} g/cm². En el espacio, "
            "sin ejercicio, la pérdida ósea es de 1 a 2 por ciento al mes (Programa "
            "de Investigación Humana de la NASA). Cargar los huesos es la razón por "
            "la que este plan siempre incluye trabajo de resistencia."
        ),
    },
    "wod.disclaimer": {
        _EN: (
            "Educational and simulated. The ground exercise specialists set your real prescription."
        ),
        _ES: (
            "Educativo y simulado. Los especialistas en ejercicio de tierra definen"
            " tu prescripción real."
        ),
    },
    "wod.mark_done": {
        _EN: "Mark as done",
        _ES: "Marcar como hecho",
    },
    "wod.done": {
        _EN: "Done today",
        _ES: "Hecho hoy",
    },
    "wod.no_profile": {
        _EN: "There is no profile data for a plan.",
        _ES: "No hay datos de perfil para un plan.",
    },
    "nutrition.title": {
        _EN: "Food of the day",
        _ES: "Comida del día",
    },
    "nutrition.energy": {
        _EN: (
            "Energy estimate: about {kcal} kcal today, with the exercise planned. "
            "Station dietitians work in a range of 1,900 to 3,200 kcal depending on"
            " weight, sex and needs (Canadian Space Agency)."
        ),
        _ES: (
            "Estimación de energía: unas {kcal} kcal hoy, con el ejercicio "
            "previsto. Los dietistas de la estación trabajan en un rango de 1.900 a"
            " 3.200 kcal según peso, sexo y necesidades (Agencia Espacial "
            "Canadiense)."
        ),
    },
    "nutrition.protein": {
        _EN: (
            "Protein reference: about {grams} g (0.8 g per kg of body weight, the "
            "dietary reference intake)."
        ),
        _ES: (
            "Referencia de proteína: unos {grams} g (0,8 g por kg de peso, la "
            "ingesta dietética de referencia)."
        ),
    },
    "nutrition.logged": {
        _EN: "Eaten today",
        _ES: "Comido hoy",
    },
    "nutrition.totals": {
        _EN: ("{kcal} kcal · {protein} g protein · {carbs} g carbohydrate · {fat} g fat"),
        _ES: ("{kcal} kcal · {protein} g proteína · {carbs} g carbohidratos · {fat} g grasa"),
    },
    "nutrition.shares": {
        _EN: (
            "Share of energy: {protein} percent protein, {carbs} percent "
            "carbohydrate, {fat} percent fat. Common reference ranges are 10 to 35,"
            " 45 to 65 and 20 to 35 percent."
        ),
        _ES: (
            "Reparto de energía: {protein} por ciento proteína, {carbs} por ciento "
            "carbohidratos, {fat} por ciento grasa. Los rangos de referencia "
            "habituales son 10 a 35, 45 a 65 y 20 a 35 por ciento."
        ),
    },
    "nutrition.empty": {
        _EN: "Nothing logged yet. Tap a food to add it.",
        _ES: "Aún no hay nada. Toca un alimento para agregarlo.",
    },
    "nutrition.add": {
        _EN: "Add a food",
        _ES: "Agregar un alimento",
    },
    "nutrition.remove": {
        _EN: "Remove {food}",
        _ES: "Quitar {food}",
    },
    "nutrition.progress": {
        _EN: "Energy {kcal} of about {target} kcal",
        _ES: "Energía {kcal} de unas {target} kcal",
    },
    "nutrition.disclaimer": {
        _EN: (
            "Simulated, illustrative foods by station food type, not the real menu."
            " No supplements or doses. The ground dietitians set your real plan."
        ),
        _ES: (
            "Alimentos simulados e ilustrativos por tipo de comida de la estación, "
            "no el menú real. Sin suplementos ni dosis. Los dietistas de tierra "
            "definen tu plan real."
        ),
    },
    "nutrition.no_profile": {
        _EN: "There is no weight and height for an estimate.",
        _ES: "No hay peso y estatura para una estimación.",
    },
    "food.cat.rehydratable": {
        _EN: "Rehydratable",
        _ES: "Rehidratable",
    },
    "food.cat.thermostabilized": {
        _EN: "Heat-treated pouch",
        _ES: "Bolsa tratada con calor",
    },
    "food.cat.intermediate": {
        _EN: "Intermediate moisture",
        _ES: "Humedad intermedia",
    },
    "food.cat.irradiated": {
        _EN: "Irradiated",
        _ES: "Irradiado",
    },
    "food.cat.natural": {
        _EN: "Natural form",
        _ES: "Forma natural",
    },
    "food.cat.fresh": {
        _EN: "Fresh",
        _ES: "Fresco",
    },
    "food.scrambled_eggs": {
        _EN: "Scrambled eggs",
        _ES: "Huevos revueltos",
    },
    "food.oatmeal": {
        _EN: "Oatmeal",
        _ES: "Avena",
    },
    "food.macaroni_cheese": {
        _EN: "Macaroni and cheese",
        _ES: "Macarrones con queso",
    },
    "food.beef_stew": {
        _EN: "Beef stew",
        _ES: "Estofado de res",
    },
    "food.chicken_rice": {
        _EN: "Chicken and rice",
        _ES: "Pollo con arroz",
    },
    "food.tuna_pouch": {
        _EN: "Tuna pouch",
        _ES: "Bolsa de atún",
    },
    "food.lentil_soup": {
        _EN: "Lentil soup",
        _ES: "Sopa de lentejas",
    },
    "food.fruit_cup": {
        _EN: "Fruit cup",
        _ES: "Vaso de fruta",
    },
    "food.granola_bar": {
        _EN: "Granola bar",
        _ES: "Barra de granola",
    },
    "food.dried_apricots": {
        _EN: "Dried apricots",
        _ES: "Duraznos secos",
    },
    "food.smoked_turkey": {
        _EN: "Smoked turkey",
        _ES: "Pavo ahumado",
    },
    "food.beef_jerky": {
        _EN: "Beef jerky",
        _ES: "Carne seca",
    },
    "food.almonds": {
        _EN: "Almonds",
        _ES: "Almendras",
    },
    "food.peanut_butter": {
        _EN: "Peanut butter",
        _ES: "Mantequilla de maní",
    },
    "food.tortilla": {
        _EN: "Tortilla",
        _ES: "Tortilla",
    },
    "food.cookies": {
        _EN: "Cookies",
        _ES: "Galletas",
    },
    "food.fresh_apple": {
        _EN: "Fresh apple",
        _ES: "Manzana fresca",
    },
    "food.fresh_greens": {
        _EN: "Fresh greens",
        _ES: "Verduras frescas",
    },
}


# Every acronym the interface shows is spelled out here (D-024). A test fails if a new acronym
# appears in ``STRINGS`` without an entry, so nothing is left unexplained by accident.
GLOSSARY: tuple[dict[Language, tuple[str, str]], ...] = (
    {
        _EN: ("WOD", "workout of the day: the exercise plan for today"),
        _ES: (
            "WOD",
            "entrenamiento del día (workout of the day en inglés): el plan de ejercicio de hoy",
        ),
    },
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
