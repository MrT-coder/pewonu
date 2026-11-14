# Prompts para NotebookLM: verificar research/09

Objetivo: conseguir las fuentes primarias de las afirmaciones marcadas `[SECUNDARIA]` y `[HUECO]` en [09-humanos-en-el-espacio.md](09-humanos-en-el-espacio.md).
Los prompts están en inglés porque la literatura está en inglés y así la búsqueda devuelve mejores resultados. Las respuestas se piden en español.

## Paso 1. Buscar fuentes (Discover sources / Deep Research)

Usa **un prompt por búsqueda**: NotebookLM devuelve pocas fuentes por búsqueda y mezclar temas las diluye. Importa solo artículos revisados por pares, informes técnicos de NASA o ESA y documentos oficiales; descarta blogs y notas de prensa, salvo que no haya alternativa.

**B1. Radiación en superficie (Marte y Luna)**
```
Find peer-reviewed primary sources measuring radiation dose on the surface of Mars and the Moon. Must include: Hassler et al. 2014 (Science, Curiosity RAD, Mars surface dose) and Zhang et al. 2020 (Science Advances, Chang'e-4 LND, lunar surface dose). Also include newer measurements or reviews from 2018-2026. Prefer journal articles and NASA/ESA technical reports. Exclude news and blogs.
```

**B2. Toxicidad del polvo lunar y marciano**
```
Find peer-reviewed studies from 2015-2026 on health risks of Martian and lunar dust for astronauts: silica and silicosis risk, perchlorate and thyroid effects, lunar dust toxicity and permissible exposure limits. Include Wang and Hynek 2025 (GeoHealth) if available and NASA Human Research Program evidence reports on celestial dust. Exclude news and blogs.
```

**B3. Lesiones de mano por guantes de EVA**
```
Find primary sources from 2010-2026 on hand and fingernail injuries (onycholysis) caused by pressurized spacesuit gloves during EVA: risk factors such as hand size, sex, EVA duration and glove fit. Include Opperman (MIT 2010) and NASA technical reports by Reid et al. Prefer NASA NTRS reports and peer-reviewed articles.
```

**B4. Glucosa y análisis de laboratorio en vuelo**
```
Find peer-reviewed or NASA/ESA sources from 2015-2026 on blood glucose measurement during spaceflight: continuous glucose monitors tested on the ISS (including the Axiom Ax-4 "Suite Ride" study), point-of-care blood analyzers (i-STAT) on the ISS, and how often crew blood glucose is actually measured in flight.
```

**B5. Subreporte de síntomas y evitación de atención médica**
```
Find peer-reviewed studies from 2015-2026 on symptom underreporting and healthcare avoidance by astronauts or pilots due to fear of losing flight or mission status. Must include Hoffman et al. 2019 and Hoffman et al. 2022 (J Occup Environ Med, pilot healthcare avoidance survey). Also any astronaut-specific evidence on medical disclosure and privacy.
```

**B6. Fenómeno del tercer cuarto**
```
Find peer-reviewed studies from 2000-2026 testing the "third-quarter phenomenon" in spaceflight and isolated, confined environments (Antarctica, Mars-500, HERA, ISS). Include Stuster 2010 (NASA astronaut journals), Kanas et al. studies with weekly mood questionnaires, and Kanas, Gushin and Yusupova 2021 "Whither the Third Quarter Phenomenon?".
```

**B7. Gravedad parcial y autoevaluaciones**
```
Find peer-reviewed sources from 2017-2026 on (1) human physiological effects of partial gravity (lunar 0.16 g, Mars 0.38 g) on bone, muscle, cardiovascular and vestibular systems, and (2) self-administered orthostatic or balance tests (sit-to-stand, stand test, tandem walk) performed by astronauts or analog crews without an examiner.
```

**B8. Rutina médica actual en la ISS**
```
Find NASA or ESA sources from 2018-2026 describing the current ISS crew medical routine: frequency of private medical conferences with flight surgeons, periodic health status exams performed by crew members, and Crew Medical Officer training hours. Prefer NASA NTRS reports, NASA-STD-3001 and peer-reviewed articles.
```

## Paso 2. Extraer y verificar (chat, con las fuentes ya cargadas)

```
Using ONLY the sources in this notebook, verify each claim below. For each one, answer in neutral Spanish with this table: | # | Claim | Verdict (CONFIRMADO / CONTRADICHO / NO ENCONTRADO) | Exact quote from the source (max 2 sentences, original language) | Source (authors, year, title, DOI or URL) | Page or section |.
Do not use outside knowledge. If a number differs from the claim, write the source's number.

1. Mars surface radiation dose is about 0.64 mSv/day (Hassler et al. 2014).
2. Lunar surface dose equivalent is about 1369 µSv/day during the lunar day (Chang'e-4, Zhang et al. 2020).
3. Martian dust contains silica and perchlorates that pose silicosis and thyroid risks to astronauts.
4. Fingernail delamination from EVA gloves is associated with small hand size, female sex, EVA duration and poor glove fit.
5. Continuous glucose monitors were tested on the ISS during the Ax-4 mission.
6. Blood glucose is NOT measured daily on the ISS; it is an occasional lab test.
7. 56.1% of 3765 pilots avoided healthcare for fear of losing their medical certificate (Hoffman et al. 2022).
8. Weekly mood questionnaires (Kanas et al.) found no third-quarter decline, contradicting Stuster's journal findings.
9. There are no long-term human data on partial gravity effects.
10. Astronauts perform balance or orthostatic self-tests without an examiner.
11. Private medical conferences are still weekly and periodic health exams are monthly on the ISS (2020 or later).
12. Crew Medical Officers receive about 25 hours of medical training.

After the table, list any new relevant finding from the sources that is not in the claims, with its quote and source.
```

## Paso 3. Devolver al repositorio

- Guarda los PDF en una carpeta y pasa la ruta al agente.
- Copia la tabla del Paso 2 en un archivo `research/notebooklm-verificacion.md`. El agente actualiza las etiquetas de research/09 a partir de ella.
- Registra el uso en [docs/uso-de-ia.md](../docs/uso-de-ia.md).
