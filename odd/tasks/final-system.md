# Final system push (before the 13:00 Ecuador presentation, Sun 15 Nov 2026)

Branch: `app/hazards` (then `app/voice`, `ground/console`). Delivery: local merges to `develop`, no push. Runner: `uv run pytest`, `uv run ruff check .`, `uv run mypy`.

## Specs

- S1: "continuemos con el tema de los peligros, la voz y el sistema de la base en tierra" and "hay MUCHAS en verdad muchas mejoras visuales por hacer".
- S2: Hazards: the five NASA HRP hazards (radiation, isolation and confinement, distance from Earth, gravity fields, hostile/closed environments) become a visible frame of the app, with what each is, what applies in the current place, and which of the astronaut's indicators it touches. Source: https://www.nasa.gov/hrp/hazards/.
- S3: Voice log: "dejarle que hable que se desahogue con preguntas abiertas aleatorias ... no 30" and "hablar el tiempo que desee y de esa bitacora guardamos la info"; "nada de lo que el tripulante diga en si se guarda lo unico que guardamos es su fonetica ... y es lo que le llega a la base". Assumptions (to confirm): no emotion labels, change vs the person's own baseline, the pattern goes to the ground with a visible notice, never moves a state.
- S4: Ground base: "hay que analizar si en el reto esto es necesario" -> it is optional, so it gets a visual upgrade only (trends, attention first), not new scope.
- S5: Visual improvements across the app (monotone look).

## Tasks

- T1 hazards view (S2): route inline, DONE (develop 0b3c311)
- T2 voice log (S3): route inline, DONE (develop 93fe9fd); microphone captured silence in the probe, speaking test pending
- T3 ground console upgrade (S4): route inline, DONE on branch ground/console (attention first, trends with band)
- T4 visual pass (S5): design DONE as docs/ux-v2/mockup.html + body.svg (approved by the user); the Flet rebuild is T5
- T5 Flet rebuild of the UX v2 (S5): one stage screen (body + data panel + mission ring), modals for zones, pulse and share, draggable mood bubble (faces -> voice in the same modal), hazards as a second screen. Reuse AppState, hazards, intake, voice, pulse_guidance, i18n; change ui/shell.py and add ui/stage.py. Flet 1.1.2 has cv.Arc, GestureDetector.on_pan_update, page.show_dialog, Blur, RadialGradient (APIs checked, runtime spike pending). Body asset: astronaut/assets/body.svg (original). Status: DONE (develop, branch app/ux-v2); polish of the visuals continues
- T6 delivery branch: only src/crew_self_check/{core,astronaut,ground}, pyproject.toml, uv.lock, .gitignore, README.md (how a judge clones and runs both systems), LICENSE; NOT tests/, docs/, research/, odd/, .qa/, CI. Status: pending, no push without the user

## Log

- L1 (user, 2026-11-14 night): "no aún no entrega primero quiero terminar el sistema, y hay MUCHAS en verdad muchas mejoras visuales por hacer, entonces continuemos con el tema de los peligros, la voz y el sistema de la base en tierra"
- L2: Flet 1.1.2 has no `AudioRecorder` (needs a separate package) and in web mode a recording stays in the browser, so the voice capture must come from the local server (sounddevice) or fall back to a labelled synthetic sample. numpy is not installed: the analysis is pure Python.
- L3 (user): "en el repo debe ir lo necesario para que los jueces si desean puedan clonar y levantar el ecosistema tanto el sistema astronauta y el sistema base"; "cuando ya subamos esto al origin todo esto de pruebas y mas, no iria, solo va el tema del sistema de astronauta y sistema de la base".
- L4: the pasted body image was NOT used (unknown license; the submission form requires permission for every external asset): an original silhouette was drawn instead (.qa/make_body.py).

## PeWoNu scope (L5, 2026-11-15)

- S6: "se llama PeWoNu el sistema en general por que se enfoca en peace, wod y nutrition, el tema peace ya tenemos con salud mental, nos faltaria el tema wod y el tema nutrition, el tema wod lo deberiamos aliar con datos que tengamos como edad, peso, datos oseos y mas, y en base a eso recomendar ejercicios en las 3 maquinas que tienen las naves y estaciones ... caminadora, bicicleta y para peso, con esto tambien puede venir el tema de nutrition con la comida que consuman ahi en las misiones".
- T7 research (DONE): ISS devices T2 treadmill, CEVIS cycle ergometer, ARED resistive; ~2.5 h/day scheduled; bone loss 1-2%/month without countermeasures (NASA HRP); ARED + energy + vitamin D kept BMD near preflight (NTRS 2014); nutrition standards follow NIH DRI (NASA-STD-3001 Vol 2 7.1); CSA: 1,900-3,200 kcal by weight, sex, needs; shelf-stable food, fresh limited.
- T8 profile data (weight, height, preflight bone mineral density), simulated: DONE (224369b)
- T9 WOD engine (core/wod.py) + modal: DONE (7dadf04, 657730b)
- T10 Nutrition engine (core/nutrition.py) + modal: DONE (10001ee, 657730b); meal log in memory only, not yet SQLite
- T11 rename to PeWoNu in the interface, README and docs; decision D-030: pending
- Rules for T9/T10: educational, cite sources, label every assumption, no doses or supplements, no clinical thresholds, no medical diagnosis; effort by perceived exertion; ground exercise specialists set the real prescription.
