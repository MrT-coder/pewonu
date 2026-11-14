# Crew Self-Check

Prototype for the NASA Space Apps Challenge 2026, "Create Health Monitoring Software for Astronauts on Space Missions".

> **Status: work in progress (hackathon, 14-15 Nov 2026).** This is a prototype built with simulated, analog data. It does **not** diagnose, predict disease, or replace medical care. Nothing here has been validated for use in space.
>
> **Built so far:** data contract, personal baseline engine, labeled population reference, status and reasons in English and Spanish, simulated Earth-spacecraft-Mars scenario, device port, and the astronaut app shell (sign-in by code, guided manual-pulse mission, five-face mood check). **Not built yet:** body figure and cards, local database, voice log, FHIR export and the ground base. See [docs/tareas.md](docs/tareas.md).

## The idea

An astronaut compares themselves with **their own baseline**, not with a population average. Each body system is colored from the person's own history, and the system turns **gray when it does not have enough data to give an opinion**. It also says what to do and when to escalate to the crew medical officer or to the ground.

- **Three spaces:** Earth, spacecraft, planet (Mars in the demo). The baseline is kept per space.
- **Two systems:** the astronaut app (runs on board, works offline) and the ground base (receives what the astronaut chose to share, as FHIR).
- **Private by default:** nothing leaves the astronaut without their confirmation. There is no conversational AI and no emotion is inferred from the voice. The planned voice log discards the audio and keeps only numeric acoustic measures, shared only if the astronaut decides.
- **Bilingual:** English and Spanish.

## Repository layout

| Path | What it is |
|---|---|
| `src/crew_self_check/core` | Data contract, baseline engine, FHIR mapping (pure Python) |
| `src/crew_self_check/astronaut` | Astronaut app (Flet, local SQLite) |
| `src/crew_self_check/ground` | Ground base (FastAPI, SQLite) |
| `docs/` | Idea, decisions, data contract, tasks, AI-use log (Spanish, internal) |
| `research/` | Evidence behind the design, with verification labels |

## Development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev --extra astronaut
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
```

Run the astronaut app (local only, works without internet) and open http://127.0.0.1:8550. The simulated
demo crew signs in with the codes `AST-0001` and `AST-0002`:

```bash
uv run python -m crew_self_check.astronaut
```

Rules for people and AI agents: [AGENTS.md](AGENTS.md). Tasks: [docs/tareas.md](docs/tareas.md).

## Data and sources

- All crew data in the demo is **fictional and simulated**, and is labeled as such in the app.
- NASA and partner-agency sources used for guidance are cited in the app and listed in the project page. Research notes with verification labels are in `research/`.
- Population reference for resting heart rate: NCHS National Health Statistics Reports No. 41 (NHANES 1999-2008), six adult rows, labeled in the app. Details: [docs/pulso-referencia.md](docs/pulso-referencia.md).
- Manual pulse technique: [MedlinePlus (NIH)](https://medlineplus.gov/ency/article/003399.htm).
- Heart-rate export follows the [HL7 FHIR R4 Heart Rate profile](https://hl7.org/fhir/R4/heartrate.html), checked with the official HL7 validator.

## Use of AI

AI ("Super Intelligence") tools were used in this project, and we say where:

- **Code, tests and documentation:** written and reviewed with Claude Code (Anthropic). A person reviews and understands everything that is committed.
- **Research notes:** collected with NotebookLM (Google).
- **Images:** the pulse-guide illustrations in `src/crew_self_check/astronaut/assets/pulse/` were generated with Gemini and edited with Meta AI, by Kevin Toalombo. They are AI-generated and contain no NASA branding.

The full log is in [docs/uso-de-ia.md](docs/uso-de-ia.md) and is summarized on the project page. Text for the NASA form and the slides: [docs/submission-pack.md](docs/submission-pack.md).

## License

*To be decided by the team before the submission.*
