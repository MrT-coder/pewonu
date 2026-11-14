# Crew Self-Check

Prototype for the NASA Space Apps Challenge 2026, "Create Health Monitoring Software for Astronauts on Space Missions".

> **Status: work in progress (hackathon, 14-15 Nov 2026).** This is a prototype built with simulated, analog data. It does **not** diagnose, predict disease, or replace medical care. Nothing here has been validated for use in space.

## The idea

An astronaut compares themselves with **their own baseline**, not with a population average. Each body system is colored from the person's own history, and the system turns **gray when it does not have enough data to give an opinion**. It also says what to do and when to escalate to the crew medical officer or to the ground.

- **Three spaces:** Earth, spacecraft, planet (Mars in the demo). The baseline is kept per space.
- **Two systems:** the astronaut app (runs on board, works offline) and the ground base (receives what the astronaut chose to share, as FHIR).
- **Private by default:** nothing leaves the astronaut without their confirmation. Conversations with the AI assistant are not sent to the ground; only numeric acoustic measures are, and only if the astronaut decides.
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
uv sync --group dev          # add --extra astronaut for the app
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
```

Rules for people and AI agents: [AGENTS.md](AGENTS.md). Tasks: [docs/tareas.md](docs/tareas.md).

## Data and sources

- All crew data in the demo is **fictional and simulated**, and is labeled as such in the app.
- NASA and partner-agency sources used for guidance are cited in the app and listed in the project page. Research notes with verification labels are in `research/`.
- Population reference for resting heart rate: NCHS National Health Statistics Reports No. 41 (NHANES 1999-2008). *To be completed with the exact tables.*

## Use of AI

AI tools were used during development. The log is in [docs/uso-de-ia.md](docs/uso-de-ia.md) and is summarized on the project page.

## License

*To be decided by the team before the submission.*
