# Final system push (before the 13:00 Ecuador presentation, Sun 15 Nov 2026)

Branch: `app/hazards` (then `app/voice`, `ground/console`). Delivery: local merges to `develop`, no push. Runner: `uv run pytest`, `uv run ruff check .`, `uv run mypy`.

## Specs

- S1: "continuemos con el tema de los peligros, la voz y el sistema de la base en tierra" and "hay MUCHAS en verdad muchas mejoras visuales por hacer".
- S2: Hazards: the five NASA HRP hazards (radiation, isolation and confinement, distance from Earth, gravity fields, hostile/closed environments) become a visible frame of the app, with what each is, what applies in the current place, and which of the astronaut's indicators it touches. Source: https://www.nasa.gov/hrp/hazards/.
- S3: Voice log: "dejarle que hable que se desahogue con preguntas abiertas aleatorias ... no 30" and "hablar el tiempo que desee y de esa bitacora guardamos la info"; "nada de lo que el tripulante diga en si se guarda lo unico que guardamos es su fonetica ... y es lo que le llega a la base". Assumptions (to confirm): no emotion labels, change vs the person's own baseline, the pattern goes to the ground with a visible notice, never moves a state.
- S4: Ground base: "hay que analizar si en el reto esto es necesario" -> it is optional, so it gets a visual upgrade only (trends, attention first), not new scope.
- S5: Visual improvements across the app (monotone look).

## Tasks

- T1 hazards view (S2): route inline, commit: pending
- T2 voice log (S3): route inline, spike microphone first, commit: pending
- T3 ground console upgrade (S4): route inline, commit: pending
- T4 visual pass (S5): route inline, commit: pending

## Log

- L1 (user, 2026-11-14 night): "no aún no entrega primero quiero terminar el sistema, y hay MUCHAS en verdad muchas mejoras visuales por hacer, entonces continuemos con el tema de los peligros, la voz y el sistema de la base en tierra"
- L2: Flet 1.1.2 has no `AudioRecorder` (needs a separate package) and in web mode a recording stays in the browser, so the voice capture must come from the local server (sounddevice) or fall back to a labelled synthetic sample. numpy is not installed: the analysis is pure Python.
