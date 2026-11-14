# 11. Recursos oficiales del reto (pestaña Resources)

Fuente: https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/?tab=resources
Leída el 13 nov 2026 (día de publicación) con Playwright headless. [VERIFICADO]

## Conclusión

- [VERIFICADO] La pestaña **no incluye datasets ni APIs**: solo 3 enlaces de NASA y 2 de la CSA, todos de lectura (artículos de contexto).
- [VERIFICADO] Refuerza lo ya registrado en [08](08-enunciado-oficial.md): no hay datos oficiales de salud de astronautas; los datos análogos o simulados (rotulados como tales) siguen siendo el camino.
- [SUPOSICION] Estos enlaces sirven como fuentes citables para la orientación educativa (guidance); falta leerlos y extraer qué respalda cada afirmación.

## NASA

| Recurso | URL | Descripción oficial (resumen) |
|---|---|---|
| 5 Hazards of Human Spaceflight | https://www.nasa.gov/hrp/hazards/ | Información básica del HRP sobre los peligros principales; enlaza a reportes detallados. |
| Risks of Human Spaceflight | https://www.nasa.gov/hrp/risks/ | Información básica del HRP sobre los riesgos principales; enlaza a reportes detallados. |
| Ongoing HRP Research in Space | https://www.nasa.gov/hrp/ongoing-hrp-research/ | Artículos sobre investigación en curso del HRP. |

## CSA (Canadian Space Agency)

| Recurso | URL | Descripción oficial (resumen) |
|---|---|---|
| Monitoring Radiation for Astronaut Health | https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp | Cómo la CSA monitorea la radiación espacial en misiones largas. |
| Why Do We Conduct Science Experiments in Space? | https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp | Por qué se hace ciencia en el espacio y su aporte a la salud humana. |

## Contenido leído (13 nov 2026)

### NASA HRP: Five Hazards (actualizada 12 jun 2026)
- [VERIFICADO] Cinco peligros: radiación espacial, aislamiento y confinamiento, distancia a la Tierra, gravedad (o su ausencia) y ambientes hostiles o cerrados.
- [VERIFICADO] "These hazards do not stand alone": se refuerzan entre sí. Se estudian con análogos terrestres, laboratorios y la ISS.
- [VERIFICADO] Ambientes cerrados: temperatura, presión, iluminación, ruido, comunidades microbianas y respuestas inmunes.
- [VERIFICADO] Distancia: Marte está a ~140 millones de millas (promedio); ~3 años de misión frente a 3 días a la Luna; la autonomía es clave.

### NASA HRP: Risks (actualizada 21 jul 2026)
Lista oficial de riesgos, agrupados en tres categorías. [VERIFICADO]
- **Fisiología (11):** respuestas inmunes alteradas, función sensoriomotora y vestibular, adaptaciones cardiovasculares, enfermedad por descompresión, interacciones huésped-microorganismo, hipoxia, alimentación y nutrición inadecuadas, lesiones y rendimiento en caminatas espaciales, menor aptitud cardiorrespiratoria y musculoesquelética, SANS (síndrome neuro-ocular), cambios óseos.
- **Conducta y factores humanos (6):** cambios conductuales y trastornos psiquiátricos, trabajo en equipo inadecuado, sueño inadecuado y horarios irregulares, soporte inadecuado de operaciones de sistemas, lesiones por cargas dinámicas.
- **Radiación (1):** cánceres inducidos por radiación.
- [VERIFICADO] Los efectos varían según el destino (órbita baja, Luna o Marte).
- **Efecto para nosotros:** esta lista es el vocabulario oficial para rotular dominios (sueño, ejercicio, nutrición, estado de ánimo, etc.) y para citar el porqué de cada guidance.

### NASA HRP: Ongoing Research (actualizada 18 ago 2026)
- [VERIFICADO] Artemis II: ARCHeR (bienestar, actividad y sueño), Immune Biomarkers (sangre y saliva), Artemis II Standard Measures (banco de datos comparable).
- [VERIFICADO] Órbita baja: B-Complex, Brain Fluid Pressure, CIPHER, Standard Measures, Thigh Cuff, Venous Haemostasis, Zero T2 (ejercicio sin cinta), entre otros.
- [VERIFICADO] Pasados: Altered Immunity, Food Acceptability, Omics Archive, Space Gardening, Spinal Health, **Tempus Pro** (dispositivo comercial de telemedicina que integra datos de salud, "potentially enabling remote, near real-time diagnoses"), Veggie Monitoring.
- **Efecto para nosotros:** ARCHeR y Standard Measures son referencias directas para "monitoreo de bienestar, actividad y sueño" y para un conjunto estándar de medidas. Tempus Pro es antecedente del reto. [SUPOSICION] Conviene leer sus fichas ("Read About ...") para ver qué variables miden.

### Fichas de investigación (leídas 13 nov 2026)

**ARCHeR** (Artemis Research for Crew Health & Readiness) — https://www.nasa.gov/reference/archer/ (actualizada 17 mar 2026)
- [VERIFICADO] Mide bienestar, actividad, patrones de sueño e interacciones durante la campaña Artemis.
- [VERIFICADO] Método: **actigrafía** (antes, durante y después de la misión) y **encuestas de desempeño conductual** (antes y después).
- [VERIFICADO] Riesgos que aborda: trabajo en equipo inadecuado, sueño inadecuado y horarios irregulares, condiciones conductuales y trastornos psiquiátricos.
- [VERIFICADO] Objetivo: entender el efecto combinado de los peligros sobre bienestar y desempeño, y desarrollar protocolos, intervenciones y tecnologías.

**Spaceflight Standard Measures** — https://www.nasa.gov/reference/standard-measures/ (actualizada 4 jun 2025)
- [VERIFICADO] Conjunto estandarizado de medidas en varios sistemas y momentos (antes, durante y después de la misión).
- [VERIFICADO] Variables: actividad y exposición a la luz (sensor de muñeca), reportes de sueño, fluidos (dieta y nutrición), saliva (función inmune), pruebas cognitivas, pruebas sensoriomotoras (equilibrio y oído interno), prueba de fuerza corporal total y muestras fecales (microbioma).

**Artemis II Standard Measures** — https://www.nasa.gov/reference/artemis-ii-standard-measures/ (actualizada 17 mar 2026)
- [VERIFICADO] Rama nueva de Standard Measures, que empezó en 2018 y tiene datos de más de 30 astronautas en órbita baja.
- [VERIFICADO] Añade sangre, saliva y orina (nutrición, cardiovascular, inmune), MRI (ojos y cerebro), equilibrio, mareo por movimiento, rendimiento muscular, microbioma y pruebas físicas al regreso (salir de la cápsula, caminata lunar simulada en traje presurizado).
- [VERIFICADO] Riesgos principales: función sensoriomotora y vestibular, cambios óseos, adaptaciones cardiovasculares.

**Efecto para nosotros**
- [SUPOSICION] Las variables que un software de monitoreo puede tocar sin hardware clínico coinciden con las de estas fichas: sueño, actividad, luz, cognición, ánimo y bienestar autoinformado. Las muestras biológicas, MRI y pruebas de fuerza quedan fuera de alcance.
- [VERIFICADO] El diseño "antes, durante y después" de la misma persona respalda la línea base personal del contrato de datos.
- [HUECO] Estas fichas no publican datos descargables ni umbrales; solo describen los estudios.

### CSA: Monitoring Radiation for Astronaut Health (26 feb 2026)
- [VERIFICADO] Contrato de 5,5 millones de dólares canadienses a Bubble Technology Industries para el CANS (Canadian Active Neutron Spectrometer), un instrumento compacto y autónomo que mide neutrones.
- [VERIFICADO] Los neutrones aportan ~30% de la radiación total en la ISS. [HUECO] el texto no aclara el tipo de medida (dosis o flujo); no usar la cifra como parte de la dosis. Artículo leído completo el 14 nov y analizado en [12-radiacion.md](12-radiacion.md).
- [VERIFICADO] Antecedentes canadienses en la ISS: MOSFET, EVARM, Radi-N y Radi-N2.

### CSA: Why Do We Conduct Science Experiments in Space? (modificada 28 oct 2025)
- [VERIFICADO] Para misiones a la Luna y Marte aumentan: tiempo en ausencia de gravedad, radiación, aislamiento, retrasos de comunicación y dependencia de recursos propios (comida, materiales, asistencia médica de emergencia).
- [VERIFICADO] "The effects observed in astronauts are similar to accelerated aging and health problems caused by a sedentary lifestyle."
- [VERIFICADO] Hay ~200 experimentos internacionales a bordo de la ISS en cualquier momento.

## Nota de uso

- [VERIFICADO] La página advierte que NASA no avala entidades no estadounidenses y que para sitios externos se deben cumplir sus parámetros de uso de datos.
- Hay que citar estas fuentes en la app y el pitch si las usamos (requisito de envío, ver AGENTS.md §6).
- [HUECO] Las subpáginas "Read About ..." de cada riesgo e investigación (donde están las variables y evidencias detalladas) no se leyeron.
