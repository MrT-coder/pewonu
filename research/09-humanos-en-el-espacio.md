# 09 - Humanos en el espacio: realismo para el producto

Fecha: 2026-10-28. Etiquetas: [VERIFICADO] leído en la fuente (con URL); [SECUNDARIA] solo en resumen de búsqueda, prensa o comunicación de empresa; [SUPOSICION] inferencia propia; [HUECO] no confirmado.
Método: cuatro investigaciones paralelas con fuentes primarias (NTRS de NASA, Evidence Reports del HRP, NASA-STD-3001, PMC/PubMed, National Academies, CSA). Se hizo una verificación cruzada propia del dato de Artemis.
Complementa a [01-fisiologia.md](01-fisiologia.md) y [02-estado-del-arte.md](02-estado-del-arte.md); no repite lo que ya está ahí.

---

## 1. Qué se mide realmente a bordo, quién lo mide y con qué

### 1.1 Equipo médico (ISS)
- [VERIFICADO] El sistema médico de la ISS (CHeCS) tiene tres subsistemas: mantenimiento ambiental, contramedidas y mantenimiento de la salud. El kit tiene 9 packs. El Medical Diagnostics Pack incluye "blood pressure cuffs, a stethoscope, a tonometer". También hay pack de emergencia, camilla de restricción apta para desfibrilación y oxígeno. https://ntrs.nasa.gov/api/citations/20110011351/downloads/20110011351.pdf
- [VERIFICADO] Ha volado hardware como el analizador de sangre portátil PCBA, un AED, un desfibrilador Zoll y una bomba de infusión. El PCBA corre un panel "from a single drop of blood". https://ntrs.nasa.gov/api/citations/20080010877/downloads/20080010877.pdf
- [VERIFICADO] En el transbordador, un PCBA comercial midió glucosa, electrolitos, pH, calcio ionizado y hematocrito con fiabilidad (Smith et al. 1997). https://pubmed.ncbi.nlm.nih.gov/9191561/
- [SECUNDARIA] Se probaron monitores continuos de glucosa en la ISS durante la misión Ax-4 (comunicación de Axiom). https://axiomspace.com/research/suite-ride
- [HUECO] No hay evidencia primaria de que la glucosa se mida **a diario** en la ISS. [SUPOSICION] Es una medición ocasional de laboratorio.

### 1.2 Wearables y sueño
- [VERIFICADO] El Bio-Monitor (Astroskin) de la CSA es una camiseta con cinta para la cabeza y una app en tableta. Mide ECG y pulso, presión arterial, respiración, temperatura de piel, SpO₂ y actividad, también durante el sueño y el ejercicio. https://www.asc-csa.gc.ca/eng/sciences/astroskin.asp
- [VERIFICADO] En la ISS, 21 astronautas durmieron en promedio **6,09 h por noche** (actigrafía de muñeca y diarios). 12 de 16 tripulantes reportaron usar fármacos para dormir (Barger et al., Lancet Neurol 2014). https://pubmed.ncbi.nlm.nih.gov/25127232/

### 1.3 Ultrasonido con operadores no expertos
- [VERIFICADO] Un CMO no médico, con entrenamiento mínimo, obtuvo imágenes diagnósticas guiado por voz desde Houston (Jones, Sargsyan et al. 2009). https://pubmed.ncbi.nlm.nih.gov/19427106/
- [VERIFICADO] Dos tripulantes recibieron 2 h de entrenamiento 8 meses antes y un repaso multimedia 6 días antes del examen. Luego completaron un estudio guiado de 35 min con 2 s de latencia (Foale et al. 2005). https://pubmed.ncbi.nlm.nih.gov/15945407/
- [VERIFICADO] Retardo de la luz en un sentido: 1,3 s a la Luna y de 181,6 s a 1337,6 s (~3 a 22 min) a Marte. https://ntrs.nasa.gov/api/citations/20170011337/downloads/20170011337.pdf
- [VERIFICADO] Con el software AMOS de instrucción "just-in-time", dos tripulantes hicieron ecografías de vejiga y riñón **sin guía de tierra** y lograron imágenes adecuadas en casi todas las vistas (Ebert et al. 2026). https://pubmed.ncbi.nlm.nih.gov/41778279/

### 1.4 El CMO y la rutina médica
- [VERIFICADO] El rol de CMO se aprende en unas **25 h** de entrenamiento. El CMO típico tiene formación técnica o de ingeniería y trabaja con la "ISS Medical Checklist". https://ntrs.nasa.gov/api/citations/20110010924/downloads/20110010924.pdf
- [VERIFICADO] Los excomandantes describen al CMO como "healthcare extender" de los flight surgeons y, para misiones de exploración, preferirían un médico. https://ntrs.nasa.gov/api/citations/20230013415/downloads/IWS_CMO.pdf
- [VERIFICADO] NASA-STD-3001 pide al menos un médico en misiones planetarias. Las conferencias médicas y psicológicas privadas "will need to change as these become asynchronous". https://ntrs.nasa.gov/api/citations/20205008928/downloads/The%20Exploration%20Rev.pdf
- [VERIFICADO] Los exámenes de salud periódicos (PHS) se hacen **mensualmente entre tripulantes** y hay una **conferencia médica privada (PMC) semanal** con el flight surgeon (Roden y Ewert 2006). https://ntrs.nasa.gov/api/citations/20060051792/downloads/20060051792.pdf
- [HUECO] No hay confirmación de la frecuencia actual (2020 en adelante).

### 1.5 Condiciones médicas más probables
- [VERIFICADO] La tabla E.2-2 de NASA-STD-3001 lista las condiciones más comunes "for any mission duration": dolor de espalda, estreñimiento, cefalea (incluida la asociada a CO₂), congestión nasal, mareo espacial, problemas urinarios, alergias, lesiones oculares, intolerancia ortostática en cambios de gravedad, diarrea, infecciones urinarias, problemas de piel, estrés agudo, ansiedad, "Insomnia/sleep disturbances/circadian misalignment", conflicto interpersonal y "Mood disturbance". https://www.nasa.gov/reference/appendix-e-health-and-medical-care-technical-requirements/

---

## 2. Diferencias por entorno

### 2.1 Gravedad parcial
- [VERIFICADO] Una revisión sistemática (Richter et al. 2017) concluye que una gravedad menor a 0,4 g "seems to be insufficient to maintain musculoskeletal and cardiopulmonary properties in the long-term". Esto abarca la Luna (0,16 g) y Marte (0,38 g). Ninguno de los 43 estudios evaluó efectos de largo plazo. https://pmc.ncbi.nlm.nih.gov/articles/PMC5559498/
- [HUECO] No hay datos humanos de larga duración en gravedad parcial. Que proteja **no está demostrado**.

### 2.2 Polvo lunar y regolito marciano
- [VERIFICADO] En Apolo 17, un tripulante tuvo "symptoms that you might associate with hay fever" al quitarse el casco: congestión nasal que afectó el habla y desapareció en ~2 h. Para la Luna se fijó un límite de exposición (PEL) de **0,3 mg/m³** para exposición episódica durante 6 meses. El límite para el polvo marciano "remains to be accomplished". https://ntrs.nasa.gov/api/citations/20150016031/downloads/20150016031.pdf
- [SECUNDARIA] El polvo marciano tendría sílice (riesgo de silicosis) y percloratos (riesgo para la tiroides). https://www.colorado.edu/today/2025/03/31/martian-dust-could-pose-health-risks-future-astronauts

### 2.3 Radiación
- [VERIFICADO] En el crucero a Marte, el instrumento RAD midió ~**1,8 mSv/día**: ~0,66 Sv solo para ida y vuelta (Zeitlin et al. 2013). El blindaje apenas frena los rayos cósmicos y para eventos solares se recomienda un refugio. https://www.swri.org/newsroom/press-releases/swri-led-team-calculates-the-radiation-exposure-associated-trip-mars
- [SECUNDARIA] En la superficie de Marte, ~0,64 mSv/día (Hassler et al. 2014). https://elib.dlr.de/106090
- [SECUNDARIA] En la superficie lunar, ~1369 µSv/día durante el día lunar (Chang'e-4, Zhang et al. 2020). https://www.dlr.de/en/latest/news/2020/03/20200925_how-intense-and-dangerous-is-cosmic-radiation-on-the-moon

### 2.4 EVA (caminatas fuera de la nave o del hábitat)
- [VERIFICADO] NASA estudia una atmósfera de hábitat de 8,2 psia con 34 % de O₂ para reducir la prerrespiración de oxígeno antes de una EVA, de ~6,5-7 h a 0-0,5 h. https://ntrs.nasa.gov/api/citations/20220005709/downloads/AsMA%202022%20-%20Abercromby%20-%20DCS%20Strategic%20Plan%20v2.pdf
- [SECUNDARIA] El desprendimiento de uñas por guantes presurizados se asocia a mano pequeña, sexo femenino, duración de la EVA y mal ajuste del guante. https://ntrs.nasa.gov/api/citations/20140014058/downloads/20140014058.pdf

### 2.5 Rover presurizado
- [VERIFICADO] El Small Pressurized Rover de NASA es para **2 personas**. Se probó en simulaciones de 3, 7 y 14 días con la tripulación viviendo dentro. https://ntrs.nasa.gov/citations/20205007271
- [SUPOSICION] En un rover no hay médico ni equipo amplio: la autoevaluación tiene que ser breve y cubrir a ambos tripulantes.

### 2.6 Estado de Artemis (corrección)
- [VERIFICADO, verificación cruzada propia] Artemis II se completó en abril de 2026. **Artemis III (2027) es un vuelo de prueba de ~2 semanas en órbita terrestre baja**, sin ir a la Luna. Tripulación: Bresnik, Parmitano (ESA), Douglas y Rubio. Artemis IV es "the first planned crewed mission to the lunar South Pole in 2028". https://www.nasa.gov/news-release/nasa-marches-toward-artemis-iii-mission-in-2027-names-crew-members/
- No decir en el pitch que "Artemis III alunizará".

### 2.7 Resumen por entorno

| Entorno | Riesgos principales | Qué priorizar en la app | Qué NO afirmar |
|---|---|---|---|
| Tránsito / estación (0 g) | Hueso y músculo, desacondicionamiento cardiovascular, radiación, sueño | Cumplimiento del ejercicio, sueño y ánimo frente a la línea base, dosis acumulada del dosímetro | Diagnosticar pérdida ósea sin imagen; estimar dosis sin dosímetro |
| Superficie lunar | Polvo, EVA, radiación sin magnetosfera, eventos solares | Síntomas respiratorios y oculares tras la EVA, molestias de manos, aviso de refugio | Que 1/6 g protege el hueso |
| Superficie de Marte | Readaptación tras el tránsito, polvo (sílice y percloratos), retraso de comunicaciones | Pruebas ortostáticas y vestibulares en los primeros días, autonomía a bordo | Umbrales validados para 0,38 g o para perclorato |
| Rover / hábitat pequeño | 2 tripulantes, equipo mínimo, EVA frecuentes, conflicto | Chequeo rápido de los dos tripulantes | Diagnóstico completo con equipo de rover |

---

## 3. Transiciones de gravedad

### 3.1 Al entrar en microgravedad: mareo espacial
- [VERIFICADO] La incidencia del mareo espacial fue de 35 % en Apolo, 60 % en Skylab y 67 % en tripulantes primerizos de los primeros vuelos del transbordador. Es más relevante "during the first few days of space flight". ~10 % sufre una ilusión de inversión ("the downs") durante 2-3 días. https://humanresearchroadmap.nasa.gov/evidence/reports/SM.pdf
- [VERIFICADO] En las misiones STS-1 a STS-94 tuvieron síntomas ~40 % (150 de 317). La prometazina fue el fármaco más usado y NASA trata tras la aparición de síntomas, no de forma preventiva. https://ntrs.nasa.gov/citations/20110020471
- [VERIFICADO] Una revisión sistemática estima ~70 % en las primeras 72 h, con mayor intensidad entre los días 1 y 5, y reaparición en los primeros 10 días tras volver a la Tierra. https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2023.1150233/full

### 3.2 Tras aterrizar: intolerancia ortostática y equilibrio
- [VERIFICADO] Tras ~6 meses de vuelo, **más del 60 %** no completó una prueba de inclinación de 10 min el día del aterrizaje, con recuperación sustancial en 24 h. Una prenda de compresión graduada evitó la taquicardia al ponerse de pie (Lee et al. 2020). https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2020.00784/full
- [VERIFICADO] Tras misiones de 3-6 meses, el mareo persistió "a week or more". La ataxia postural puede durar meses. Tras volver de la ISS no se conduce durante 8-12 días. https://humanresearchroadmap.nasa.gov/evidence/reports/SM.pdf
- [VERIFICADO] El Field Test evaluó pruebas de sentarse y levantarse, mantenerse de pie, marcha en tándem y obstáculos en las primeras 2 h, a las ~12 h, a las ~24 h y en días posteriores. Hubo mejora fuerte en 24 h, sin recuperación completa en la misión de un año. https://ntrs.nasa.gov/api/citations/20160013695/downloads/20160013695.pdf
- [VERIFICADO] El ejercicio por sí solo no evitó los déficits de control postural (Functional Task Test). https://ntrs.nasa.gov/api/citations/20170001370/downloads/20170001370.pdf

### 3.3 Implicación para Marte
- [VERIFICADO] NASA señala el mayor riesgo "during and soon after G-transitions ... (landing, immediate egress following landing)". Marte preocupa por el tránsito prolongado seguido de tareas de aterrizaje. El efecto de una transición menor (a 3/8 g) es "unknown". https://humanresearchroadmap.nasa.gov/evidence/reports/SM.pdf
- [VERIFICADO] Un análogo real es la **Expedición 6**: aterrizaje balístico a ~475 km del punto previsto y ~5 h sin rescate. La tripulación salió sola de la cápsula. Pettit relató "I had trouble walking but could crawl" y recomendó para Marte "a few days for adaptation". Misma fuente.

### 3.4 Automediciones con respaldo
- [VERIFICADO] Prueba de pie: frecuencia cardíaca y presión acostado y luego de pie. Antes del vuelo el aumento típico de FC al pararse fue de ~+10 lpm (Lee et al. 2020).
- [VERIFICADO] Tareas del Field Test sin equipo pesado: sentarse y levantarse, mantenerse de pie, marcha en tándem.
- [VERIFICADO] Cuestionario estandarizado de 21 síntomas neurovestibulares tras el vuelo, con la advertencia de que el autorreporte es subjetivo y puede subreportarse (SM.pdf).
- [HUECO] No hay umbrales validados de automonitoreo ni evidencia de que los astronautas hagan pruebas de equilibrio sin un examinador.

---

## 4. Subreporte de síntomas, privacidad y autonomía

### 4.1 Por qué los astronautas callan síntomas
- [VERIFICADO] *Safe Passage* (IOM 2001), cap. 6:
  - "The fear of mission disqualification increases their reluctance to report medical information" (p. 174).
  - La cultura del cuerpo de astronautas "values stoicism and a 'can-do' attitude" (p. 174).
  - "Astronauts are reluctant to reveal medical incidents or complaints and to report symptoms during space missions" (p. 183).
  - https://www.nationalacademies.org/read/10218/chapter/8
- [SECUNDARIA, análogo con pilotos] El 56,1 % de 3765 pilotos evitó atención médica por miedo a perder su certificado (Hoffman et al. 2022). https://pubmed.ncbi.nlm.nih.gov/35166258/
- [HUECO] No hay datos cuantitativos recientes sobre astronautas.

### 4.2 Privacidad médica
- [VERIFICADO] Los flight surgeons tienen "weekly private medical conferences with the astronauts". https://www.nasa.gov/directorates/esdmd/hhp/flight-surgeons
- [VERIFICADO] La Privacy Act se interpreta "to strictly forbid disclosure of any astronaut medical data in any form" (*Safe Passage*, p. 176).
- [VERIFICADO] En LSAH, "Individual astronaut data are not downloadable". https://ntrs.nasa.gov/api/citations/20170009502/downloads/20170009502.pdf

### 4.3 Autorreporte conductual
- [VERIFICADO] En los diarios de astronautas (Stuster 2010) hay "evidence of a decline in morale during the third quarters". Escribir los diarios los benefició. https://ntrs.nasa.gov/citations/20100026549
- [SECUNDARIA] Los cuestionarios de Kanas no muestran ese efecto, así que el "fenómeno del tercer cuarto" sigue en discusión.

### 4.4 Autonomía con retraso
- [VERIFICADO] En el piloto de 105 días de Mars-500 hubo 5 semanas de alta autonomía con 40 min de retraso. "High work autonomy was well-received by the crew ... no adverse effects". El control de misión mostró "more anxiety and work role confusion". https://iafastro.directory/iac/archive/browse/IAC-10/A1/1/6839/

### 4.5 Ética (IOM 2014)
- [VERIFICADO] Principios: evitar daño, beneficencia, respeto a la autonomía, equidad y fidelidad. Responsabilidades: informar plenamente los riesgos y proteger "the privacy and confidentiality" de los datos. https://www.nationalacademies.org/read/18576/chapter/2

---

## 5. Implicaciones para el producto

1. **Indicadores realistas de ingreso diario:** FC, presión arterial, SpO₂, temperatura y actividad (equipos tipo Bio-Monitor o del Medical Diagnostics Pack); sueño (actigrafía); autorreporte de ánimo, estrés, dolor (espalda, cabeza), congestión y síntomas digestivos o urinarios, que coinciden con las condiciones comunes de NASA-STD-3001.
2. **Glucosa de baja frecuencia:** se trata como un análisis ocasional, no diario. El gris por datos insuficientes es su estado normal entre mediciones, no una alarma.
3. **Modo entorno = qué preguntar y priorizar, no umbrales distintos:** no hay evidencia para fijar umbrales clínicos por gravedad.
4. **Escenario de demo documentado: llegada a Marte**, días R+0 a R+3. Prueba de pie, cuestionario vestibular, marcha en tándem y autoevaluación visual. Resultado: cardiovascular en ámbar y vestibular en rojo. Se recomienda descanso e hidratación y **no hacer EVA ni conducir el rover**. Se escala al CMO y a Tierra de forma asíncrona. Se basa en la Expedición 6 y en la recomendación de Pettit.
5. **Privado por defecto:** los datos crudos solo los ve el astronauta. El CMO o Tierra reciben un resumen **si el astronauta lo comparte**. La interfaz deja claro que esos datos no se usan para decidir si sigue apto para la misión. Así se ataca la causa documentada del subreporte.
6. **El escalamiento sugiere, no notifica automáticamente.** La excepción serían emergencias predefinidas aceptadas por la tripulación [SUPOSICION de diseño]. Registro de accesos visible para el astronauta.
7. **Pasos tipo checklist, no diagnósticos:** el CMO no es médico y tiene ~25 h de entrenamiento. La ecografía se presenta como adquisición guiada (como AMOS), no como interpretación automática.
8. **Cadencia natural:** recordatorio diario, chequeo entre tripulantes mensual y resumen semanal (equivalente a la PMC), asíncrono en Marte.
9. **Diario privado opcional:** en Stuster, los diarios captaron lo que los cuestionarios no.

## 6. Qué NO decir en la app ni en el pitch

- Que la app diagnostica, prescribe o indica dosis.
- Que la glucosa se mide a diario en la ISS.
- Umbrales validados para Marte, para gravedad parcial o para perclorato.
- Que el ejercicio por sí solo previene los déficits de equilibrio.
- Que Artemis III aluniza.
- Cifras marcadas [SECUNDARIA] como si fueran primarias.
