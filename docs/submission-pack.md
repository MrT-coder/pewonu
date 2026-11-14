# Crew Self-Check: submission pack

Everything the team needs for the NASA Space Apps 2026 project form and for the slides. Written in English because it is a deliverable. Source of truth for the claims: [decisiones.md](decisiones.md), [contrato-datos.md](contrato-datos.md), [tareas.md](tareas.md) and the code.

**How to read the labels**
- `[BUILT]` exists in the repository and was checked by tests or by running the app.
- `[PENDING]` is designed or decided but **not built yet**. Do not claim it in the final text unless it is done before submitting. Section 1 has a table of what each claim needs.
- Nothing here is a clinical claim: the data is simulated and analog.

Submission window closes **Sunday 15 November, 23:59, local event time**. Only the last click on "Submit for Judging" is reviewed.

---

## 0. Blockers to fix before submitting

| # | What the form requires | Where we are | Action |
|---|---|---|---|
| 1 | **Images made with SI must carry a visible watermark** saying they are SI-generated. | The eight pulse-guide illustrations (Gemini, edited with Meta AI) have **no watermark**. The app only says "Illustrations generated with AI." in small text under the picture. | Add a visible mark on the images, or an overlay badge in the app. Same for any slide that uses them. **Decide who and how.** |
| 2 | **Code and data must acknowledge SI generation in descriptive text and metadata.** | `README.md` now has an AI-use statement (section "Use of AI"). Commits carry no AI trailer, by team rule. | Keep the README statement. Optionally repeat it in the repository description. |
| 3 | **SI content may not use NASA branding** (logos, flags, mission identifiers). | The illustrations show a generic astronaut patch with a star, not a NASA emblem. | Re-check every image and slide before submitting. |
| 4 | **Project link must be public** (no password, permission or registration). | The repository is local. There is no public URL yet. | Publish the repository (team decision) and put its full URL in the form. |
| 5 | **Demo link** (7 slides or 30 s video) must be public and open without registration. | Not created yet. | Build the slides from section 4 and host them (Google Drive, GitHub, YouTube...). |
| 6 | **License** of the repository. | Undecided. | Decide before publishing. |
| 7 | **Project name.** The form shows "Project PeWoNu". | The product is called **Crew Self-Check**. | Confirm which name goes in the title field. |

---

## 1. What is built and what is not

| Capability | Status | Needs (task) |
|---|---|---|
| Data contract 0.3 (six typed objects, JSON, validation) | `[BUILT]` | C1 |
| Personal baseline per person, indicator and space (median with a robust band) | `[BUILT]` | C3 |
| Gray ("insufficient data") when there is not enough history | `[BUILT]` | C3 |
| Sustained-deviation rule (three readings outside the band) | `[BUILT]` | C3 |
| Transition reference: a new space is compared with the previous space's baseline | `[BUILT]` | C4 |
| Population reference for resting pulse (NHSR no. 41), always labeled | `[BUILT]` | C2, C4 |
| Plain-language reasons in English and Spanish, no AI model in the alert path | `[BUILT]` | C4 |
| Simulated trip Earth, spacecraft, Mars with a fictitious crew | `[BUILT]` | C5 |
| Device port and a simulated watch and band | `[BUILT]` | C6 |
| Astronaut app: sign-in by personal code, English and Spanish, limits screen | `[BUILT]` | A2 (partly), A9 |
| Guided, gamified manual pulse ("pulse mission") | `[BUILT]` | A5 |
| Mood check with five faces | `[BUILT]` | A6 (survey part) |
| Works without internet | `[BUILT]` (spike A1) | A1 |
| Body figure colored by system status, system cards with citations | `[PENDING]` | A3, A4 |
| One-page summary per astronaut ("human KPIs") | `[PENDING]` | part 4 of D-020 |
| Local database (SQLite) | `[PENDING]` | A2 |
| Voice log (audio discarded, numeric acoustic measures kept) | `[PENDING]` | A6 (audio part) |
| Standardized export to FHIR R4 | `[PENDING]` (mapping verified, exporter not written) | C8 |
| Ground base that receives FHIR with a simulated delay | `[PENDING]` | G1 to G3 |
| Escalation the astronaut confirms before anything is sent | `[PENDING]` | A10 |
| Trip player and routine reminders | `[PENDING]` | A7, A8 |
| ISS-analog spacecraft profile, emergency screen, adherence streak | `[PENDING]` | C7, A11, A12 |

Engineering facts you can quote `[BUILT]`: 371 automated tests; strict type checking; contract of six objects; two simulated crew members over a 28-day trip (14 days on Earth, 10 in the spacecraft, 4 on arrival at Mars); engine defaults are 5 days of history, 3 sustained readings and a 2.5 robust-deviation band.

---

## 2. Project form, ready to paste

### Project name
`Crew Self-Check` (confirm: the form currently shows "Project PeWoNu").

### Summary (limit 1500 characters; 50 to 200 words suggested)

Safe version, only claims what is built (about 170 words):

> Crew Self-Check is a health self-assessment prototype for astronauts on long missions, built with simulated, analog data. Instead of comparing an astronaut with an average person, it compares them with **their own baseline**, kept separately for Earth, the spacecraft and a planet's surface. When it does not have enough data it says so (gray) instead of guessing. The astronaut signs in with a personal code, answers a five-face mood check and takes a manually counted pulse through a guided, gamified "pulse mission" that teaches the wrist technique step by step; the game rewards good technique, never the value of the pulse. The rules that decide a status are deterministic and explained in plain English and Spanish: no AI model is in the alert path, and nothing is diagnosed. The design is private by default: data stays on the crew computer and only what the astronaut chooses to share is meant to travel to the ground team, standardized as HL7 FHIR R4. The app runs locally and works without internet.

Add this sentence only if it is true at submission time:

> `[PENDING A3, A4]` Each body system is shown on a body figure and colored against the astronaut's own baseline, with a card that explains why.
> `[PENDING C8, G1 to G3, A10]` What the astronaut confirms is sent to a ground-base system as an HL7 FHIR Bundle, after a simulated communication delay.

### Project Details (long field)

> **What it does.** Crew Self-Check helps an astronaut understand their own health data when the medical team is minutes or months away. It turns a few simple entries (a mood check, a manually counted resting pulse, readings from simulated wearables) into a status for each indicator: green, amber, red or gray. The color always means "compared with what", and the app says which reference was used.
>
> **How it works.** A personal baseline is built per person, per indicator and per space (Earth, spacecraft, planet) from the median of the person's history with a robust band. Three consecutive readings outside the band on the same side raise amber. A new space starts gray, and during the first days it is compared with the previous space's baseline, labeled as a transition. Only while there is no personal baseline, the resting pulse is compared with a labeled population reference (NCHS National Health Statistics Reports No. 41), and every state shows which reference was used. Reasons are short templates in English and Spanish. The logic is deterministic: there is no AI model in the alert path, and the app never diagnoses.
>
> **The astronaut experience.** The astronaut signs in with a personal code. A five-face check records how they feel. The resting pulse is taken by hand, because that is what is possible without equipment: a four-station "pulse mission" (rest, find the artery, press lightly, count) with illustrations, an optional timer, a field to enter the beats you counted and a simple explanatory graph, followed by points and a badge for **technique and regularity, never for the value of the pulse**. Everything is bilingual and a "Limits" screen is available from every screen.
>
> **Privacy and the ground base.** Data is private by default and stays on the crew computer. Nothing is meant to leave without the astronaut's confirmation. What is shared is standardized as HL7 FHIR R4 (a heart-rate `Observation` with LOINC 8867-4 and unit `/min`) so a ground team can read it. We checked the mapping against the official HL7 profile and validator. `[PENDING C8, G1 to G3]` The exporter and the ground base are not finished.
>
> **Benefits and intended impact.** Fewer false alarms and less false reassurance (gray instead of a guess), advice that fits each person and each environment, and a clear way to share only what the astronaut decides. It also works as a model for analog missions on Earth.
>
> **Tools.** Python 3.12, Flet (user interface, served locally and offline), a pure-Python core with a ports-and-adapters layout, pytest, ruff and mypy (strict), the official HL7 FHIR validator (Java), and Playwright for visual checks.
>
> **What is creative.** The color is relative to the person, not to a population; the gray is honest about missing data; the transition reference handles the change of environment; and the manual pulse is turned into a short guided game that rewards how you measure, not what you measure.
>
> **Factors we considered.** Astronauts fear that health reports can affect mission selection, so reporting must feel safe (privacy by default, escalation that suggests and never notifies on its own). The crew medical officer is not a physician, so we give checklists and sources, never diagnoses or doses. Communication with Earth is delayed, so the first decisions are made on board. All data is simulated and labeled as such.
>
> **Honest limits.** Analog and simulated data only; nothing validated in orbit; no diagnosis; thresholds are statistical conventions of the prototype, not clinical limits.

### Use of Super Intelligence (SI): what to select

I could not see the exact checkbox labels, so match these to the closest option:

| Type | Used? | Tool | What for | Where it is acknowledged |
|---|---|---|---|---|
| Code | **Yes** | Claude Code (Anthropic) | Most of the source code, tests and documentation, written and reviewed with the team | README "Use of AI", `docs/uso-de-ia.md`, project details |
| Text and data | **Yes** | Claude Code; NotebookLM (Google, Gemini) | Research notes, source inventory, drafts of documentation | `docs/uso-de-ia.md`, project details |
| Images | **Yes** | Gemini (generation) and Meta AI (editing), by Kevin Toalombo | Eight illustrations of the manual pulse technique, in Spanish and English | `docs/uso-de-ia.md`, app footer, **watermark pending (blocker 1)** |
| Video | Not yet | n/a | A demo video, if the team chooses video over slides, must also carry a watermark | n/a |
| Audio | No | n/a | The app does not generate or store audio | n/a |

The team's full log is [uso-de-ia.md](uso-de-ia.md).

### NASA Data (Link Text / Link URL)

No NASA datasets were used: the challenge page lists none (see [research/11](../research/11-recursos-oficiales.md)). These NASA **resources** were read on 13 November 2026 and shaped the design:

| Link Text | Link URL |
|---|---|
| NASA HRP: Five Hazards of Human Spaceflight | https://www.nasa.gov/hrp/hazards/ |
| NASA HRP: Risks of Human Spaceflight | https://www.nasa.gov/hrp/risks/ |
| NASA HRP: Ongoing HRP Research in Space | https://www.nasa.gov/hrp/ongoing-hrp-research/ |
| NASA ARCHeR (Artemis Research for Crew Health & Readiness) | https://www.nasa.gov/reference/archer/ |
| NASA Spaceflight Standard Measures | https://www.nasa.gov/reference/standard-measures/ |
| NASA Artemis II Standard Measures | https://www.nasa.gov/reference/artemis-ii-standard-measures/ |
| NASA Space Apps: Create Health Monitoring Software for Astronauts (challenge page) | https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/ |

What each one supports: the HRP pages give the official list of hazards and risks (we use that vocabulary for the body systems and for guidance); ARCHeR and Standard Measures measure the same person before, during and after a mission, which backs the personal baseline.

### Space Agency Partner & Other Data (Link Text / Link URL)

| Link Text | Link URL | Used for |
|---|---|---|
| CSA: Why Do We Conduct Science Experiments in Space? | https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp | Context on longer, farther missions |
| NCHS National Health Statistics Reports No. 41 (resting pulse reference, NHANES 1999-2008) | https://www.cdc.gov/nchs/data/nhsr/nhsr041.pdf | Labeled population reference for the resting pulse (six adult rows) |
| MedlinePlus (NIH): Pulse | https://medlineplus.gov/ency/article/003399.htm | Manual pulse technique |
| HL7 FHIR R4: Heart Rate profile | https://hl7.org/fhir/R4/heartrate.html | Standardized export of the pulse |
| HL7 FHIR Validator (`validator_cli.jar`) | https://github.com/hapifhir/org.hl7.fhir.core | Checking FHIR output |
| LOINC 8867-4 "Heart rate" | https://loinc.org/8867-4 | Observation code |
| UCUM | https://ucum.org | Unit `/min` |
| Flet | https://flet.dev | User interface framework |
| Python | https://www.python.org | Language |
| pytest, ruff, mypy, uv | https://docs.pytest.org, https://docs.astral.sh/ruff, https://mypy-lang.org, https://docs.astral.sh/uv | Testing, linting, typing, packaging |
| Playwright | https://playwright.dev | Visual checks of the running app |
| Claude Code | https://claude.com/claude-code | SI tool (code, tests, docs) |
| Gemini | https://gemini.google.com | SI tool (images) |
| Meta AI | https://www.meta.ai | SI tool (image editing) |
| NotebookLM | https://notebooklm.google.com | SI tool (research notes) |

`[HUECO]` Licenses are not all checked. Before ticking "All work is original", confirm the license of Flet and of the bundled icons and font, and that LOINC attribution is satisfied.

### Links

| Field | Value |
|---|---|
| Project | `[HUECO]` full public URL of the repository |
| Project Demonstration | `[HUECO]` full public URL of the slides or the video |

---

## 3. One-paragraph pitch (for the first slide notes)

Astronauts will soon be too far from Earth for real-time medical help. Averages do not help them, because gravity, light and isolation change what normal means for each person. Crew Self-Check compares every astronaut with themselves, says "I do not know yet" when it does not have enough data, labels what it compared against, keeps data private by default and shares only what the astronaut chooses, in a standard format the ground team already understands.

---

## 4. Slides (maximum 7 including title and introduction)

Keep text short: judges read these without a presenter. Put the SI watermark on every generated image. Cite sources in small print on the slide. **Spell out every acronym the first time it appears on a slide**, for example "beats per minute (bpm)"; the glossary in section 7 has the expansions.

**Slide 1: Title and introduction**
- Crew Self-Check. "Know your own baseline."
- Health self-assessment for astronauts on long missions. NASA Space Apps 2026.
- Prototype with **simulated, analog data**. No diagnosis.
- Team names and the project name as confirmed (blocker 7).
- Visual: the sign-in screen.

**Slide 2: The problem**
- On long missions the crew is far from Earth and from its doctors; communication is delayed (about 3 to 22 minutes one way to Mars, per team research note).
- NASA lists five hazards: radiation, isolation and confinement, distance from Earth, gravity, and hostile or closed environments. They reinforce one another. (NASA HRP.)
- "Normal" is personal and changes with the environment. A population average can raise false alarms or false comfort.
- Visual: a simple Earth, spacecraft, Mars line.

**Slide 3: The idea**
- Compare each astronaut with **their own baseline**, per space: Earth, spacecraft, planet.
- **Honest gray:** "not enough data yet" instead of a guess.
- **Transition:** a new space is compared with the previous one and labeled as such.
- Every state says what it was compared with.
- Visual: three baselines and a traffic-light legend with gray.

**Slide 4: How it works**
- Intake: five-face mood check, manually counted pulse, simulated wearables.
- Engine: personal baseline (median and robust band), sustained deviation, labeled references.
- Output: status per indicator and per system, with a plain reason in English and Spanish.
- **Deterministic. No AI model in the alert path.**
- Privacy: data stays on board; only what the astronaut confirms is shared, as HL7 FHIR R4. `[PENDING C8]` for the exporter.
- Visual: a left-to-right flow diagram.

**Slide 5: Demo**
- Sign in with a personal code. Switch English and Spanish.
- The **pulse mission**: four stations, count with your fingers on the wrist and enter the beats, "34 beats x 2 = 68 bpm", points and a badge for technique only.
- Mood check with five faces.
- Earth to Mars scenario with the four states (green, amber, red, gray). `[PENDING A3, A7]` for the body figure and the trip player.
- Visual: three or four screenshots (they exist for sign-in, pulse mission and mood). Pulse illustrations need the SI watermark.

**Slide 6: Trust, privacy and limits**
- Private by default; escalation suggests and never notifies by itself.
- No diagnosis, no medication, no clinical thresholds; the "Limits" screen is always one tap away.
- Population reference only for the resting pulse, only without a personal baseline, always labeled.
- FHIR mapping checked against the official HL7 profile and validator.
- SI disclosure: code and text written with Claude Code; research notes with NotebookLM; illustrations by Gemini and Meta AI (watermarked).

**Slide 7: Impact, sources and next steps**
- Impact: safer self-assessment far from help; a model for analog missions on Earth.
- Next: body figure and system cards, ground base with delay, voice log, real device sources.
- Sources: NASA HRP (hazards, risks, ongoing research, ARCHeR, Standard Measures); CSA; NCHS NHSR 41; MedlinePlus; HL7 FHIR. Full list in the project page.
- Visual: repository link and QR code once it is public.

---

## 5. If the team prefers a 30-second video

Hard limit: 30 seconds. Subtitles in English if the narration is in Spanish. Add the SI watermark to any generated image.

| Time | Shot | Voice / caption |
|---|---|---|
| 0 to 4 s | Earth, spacecraft, Mars line | "Far from Earth, normal is personal." |
| 4 to 10 s | Sign in with the code, switch language | "Crew Self-Check compares each astronaut with themselves." |
| 10 to 18 s | Pulse mission: enter the counted beats, result, badge | "Even a manual pulse becomes a guided game that rewards good technique." |
| 18 to 24 s | Four states, gray highlighted `[PENDING A3, A7]` | "When it does not know, it says gray. It always shows what it compared against." |
| 24 to 30 s | Privacy lock, FHIR, limits | "Private by default. Standard FHIR for the ground team. No diagnosis." |

---

## 6. Facts that need a source before they go on a slide

| Claim | Status |
|---|---|
| Five hazards and the list of risks | `[VERIFICADO]` NASA HRP pages, read 13 Nov 2026 |
| Missions to the Moon and Mars bring more radiation, isolation, delay and dependence on own resources | `[VERIFICADO]` CSA page, read 14 Nov 2026 |
| Sleep on the ISS is shorter than scheduled; resting pulse changes on landing | Do **not** quote numbers: they come from search summaries and the articles were not opened (D-013) |
| One-way delay Earth to Mars about 3 to 22 minutes | From the team's research note ([research/10](../research/10-plataforma-offline-y-dispositivos.md)); confirm the source before quoting |
| Heart-rate Observation: category vital-signs, LOINC 8867-4, unit `/min` | `[VERIFICADO]` HL7 FHIR R4 Heart Rate profile; official validator gave 0 errors on a sample |
| Wrist technique: index and middle fingers, light pressure, count 30 s x 2 or 60 s, rest 10 minutes | `[VERIFICADO]` MedlinePlus (the team's illustrations differ in a few labels, see D-021) |

---

## 7. Glossary (spell these out on first use in the form and on the slides)

| Acronym | Meaning |
|---|---|
| AI | Artificial intelligence |
| SI | "Super Intelligence": the term NASA Space Apps uses for AI tools |
| ARCHeR | Artemis Research for Crew Health & Readiness (a NASA study) |
| bpm | Beats per minute (Spanish: lpm, latidos por minuto) |
| CSA | Canadian Space Agency |
| FHIR | Fast Healthcare Interoperability Resources: the HL7 standard for exchanging health data |
| HL7 | Health Level Seven International: the standards organization behind FHIR |
| HRP | Human Research Program (NASA) |
| ISS | International Space Station |
| JSON | JavaScript Object Notation: a plain-text data format |
| KPIs | Key performance indicators: here, a short summary per astronaut |
| LOINC | Logical Observation Identifiers Names and Codes: standard codes for measurements |
| NASA | National Aeronautics and Space Administration |
| NCHS | National Center for Health Statistics (United States) |
| NHANES | National Health and Nutrition Examination Survey (United States) |
| NHSR | National Health Statistics Reports |
| NIH | National Institutes of Health (United States) |
| QR | Quick-response code |
| SQLite | A small database stored in a single file |
| UCUM | Unified Code for Units of Measure |
| URL | Web address |

The astronaut app has the same idea built in: every acronym it shows is spelled out where it matters and listed in a Glossary dialog, available from every screen (D-024).
