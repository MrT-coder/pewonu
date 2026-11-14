# 07 - Angulos de idea previos al enunciado oficial

Fecha: 2026-10-02. Reto: "Create Health Monitoring Software for Astronauts on Space Missions" (enunciado y datasets el 28 oct; hackathon 14-15 nov).
Etiquetas: [VERIFICADO] visto en la fuente citada (pagina abierta o resumen de busqueda, se indica); [SUPOSICION] inferencia propia; [HUECO] no confirmado.
No repite lo de 01-04; solo anade angulos y evidencia nueva. Las fuentes marcadas "(busqueda)" se vieron solo como resultado de busqueda, no se abrieron completas.

---

## 1. Linea base personal (N-of-1), cambio de punto e incertidumbre calibrada

**Que es.** Detectar cambios respecto a la propia historia de la persona (detector tipo CUSUM sobre FC en reposo, sueno, pasos) y acompanar cada salida con un intervalo calibrado (conformal) y una regla de abstencion.

**Evidencia.**
- [VERIFICADO] Mishra et al. 2020 (Nat Biomed Eng), 32 casos COVID-19 de ~5.300 participantes: 26 (81 %) mostraron alteraciones en FC, pasos o sueno; 22 de 25 con datos de sintomas se detectaron antes o en el inicio de sintomas; 63 % detectables en tiempo real con un sistema de dos niveles sobre elevaciones extremas de FC en reposo respecto a la linea base individual. https://www.medrxiv.org/content/10.1101/2020.07.06.20147512v1 (busqueda; resumen)
- [VERIFICADO] Scripps DETECT: mismo principio de linea base individual, AUC 0,80 combinando sintomas reportados con sueno y FC en reposo. https://blog.google/products-and-platforms/devices/fitbit/fitbit-detect/ (busqueda)
- [VERIFICADO] Conformal + wearable: Strickland et al. (Coventry, nov 2025), temperatura corporal central con intervalos calibrados, error de prueba 0,29 C, >140.000 mediciones en seis dominios operativos, motor de alertas configurable segun confianza del modelo. https://pureportal.coventry.ac.uk/en/publications/degrees-of-uncertainty-conformal-deep-learning-for-non-invasive-c/ (abierta)
- [VERIFICADO] La conformal en series temporales viola la intercambiabilidad; existen variantes online para deriva (resultado de busqueda, sin fuente primaria abierta). [HUECO] elegir una referencia primaria (p. ej. Angelopoulos y Bates, "A Gentle Introduction", https://people.eecs.berkeley.edu/~angelopoulos/publications/downloads/gentle_intro_conformal_dfuq.pdf, aparece en busqueda; no se abrio).

**Demo 48 h con datos abiertos.** Sleep-Accel por sujeto: ventana de linea base, CUSUM/EWMA sobre FC nocturna y sueno, intervalo conformal split sobre residuos de la linea base, y salida de tres estados (dentro de lo esperado / cambio / `insufficient_data`). Mostrar cobertura empirica (por ejemplo "el 90 % nominal cubre X %") en las noches de calibracion y un ejemplo de abstencion al inyectar huecos. Cabe en 48 h.

**Riesgos.** Sleep-Accel no contiene eventos clinicos etiquetados: solo se puede validar cobertura estadistica, no deteccion de enfermedad [SUPOSICION]. Intercambiabilidad violada en series con deriva, hay que decirlo. Ya cubierto parcialmente por Concepto A de 04; lo nuevo es la cobertura empirica visible y el detector CUSUM con referencia publicada.

**Etiqueta.** Evidencia terrestre [VERIFICADO]; aplicabilidad a astronautas [SUPOSICION] (01-fisiologia lo marca HUECO para umbrales en orbita).

---

## 2. Inferencia en el borde / offline y autonomia medica

**Que es.** Motor de reglas o modelo pequeno que corre sin enlace, con cola local y sincronizacion diferida.

**Evidencia.**
- [VERIFICADO] EIMO ConOps: transferir cuidado de Tierra a sistemas a bordo por retrasos e imposibilidad de evacuar; sistema medico como "sistema de sistemas" con sensores portables, diagnostico en punto de atencion y bases de referencia; revision con escenarios nuevos de barotrauma/autocuidado y salud conductual/cronicas, informada por reuniones sobre datos y entrenamiento. https://ntrs.nasa.gov/citations/20250000009 (abierta)
- [VERIFICADO] CDSS para EIMO: el sistema debe operar con retrasos de comunicacion y restricciones de computo, masa, volumen y energia; debe reducir carga cognitiva y mantener conciencia situacional. Los autores reconocen que la validez clinica y operativa "no ha sido revisada por pares". https://pmc.ncbi.nlm.nih.gov/articles/PMC10284846/ (abierta)
- [VERIFICADO] CMO-DA (TRISH + Google Cloud): asistente CDSS multimodal (texto, imagen, voz) entrenado en literatura de vuelo, evaluado con marco OSCE; resultados "prometedores", sin metricas numericas publicas; fase de prueba de concepto. https://cloud.google.com/blog/topics/public-sector/how-google-and-nasa-are-testing-ai-for-medical-care-in-space (abierta). Este item sustituye al blog no primario citado en 02 (hueco cerrado parcialmente).
- [VERIFICADO] TinyML permite inferencia local en microcontroladores con menos energia y sin transmision continua; ejemplos de ECG con modelos cuantizados (resultado de busqueda, no abierto). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12031393/
- [VERIFICADO] Retraso Marte: el CDSS paper dice "mayor de 20 minutos"; 02-estado-del-arte ya trae 3-22 min.

**Demo 48 h.** PWA instalable con service worker, IndexedDB, cola con reintentos y un conmutador "enlace Tierra" con retraso configurable; reglas del angulo 1 corriendo localmente. Es Concepto B de 04; lo nuevo es medir y mostrar un presupuesto de recursos (latencia por inferencia, KB de modelo, bytes sincronizados por dia).

**Riesgos.** Es el angulo mas predecible (varios equipos lo propondran) [SUPOSICION]. Diferenciacion depende de la honestidad (angulo 1) y de la presentacion.

**Etiqueta.** Necesidad [VERIFICADO]; novedad [SUPOSICION: baja]; cifras de recursos reales de la nave [HUECO].

---

## 3. Explicabilidad y apoyo a la decision para la tripulacion

**Que es.** Salida orientada a la accion del CMO: "que hacer ahora, por que, como se llego a la decision", con trazabilidad y nivel de confianza.

**Evidencia.**
- [VERIFICADO] Requisito literal en el paper CDSS: "concise logical interactions detailing what to do now, why to do it, how the decision was reached"; estresores de vuelo (sobrecarga auditiva, CO2 elevado) afectan la cognicion; el alcance cognitivo pesa mas que las habilidades procedimentales; simulaciones sugieren que subir al equipo de nivel paramedico a medico reduce muertes de mision en al menos 34 %. https://pmc.ncbi.nlm.nih.gov/articles/PMC10284846/ (abierta)
- [VERIFICADO] Gap ExMC Medical-701 ("aumentar capacidades medicas en vuelo... minimizando costos de recursos") y la Medical Data Architecture como plataforma para el CDS. Resultado de busqueda sobre NTRS (https://ntrs.nasa.gov/citations/20220017869 y vecinos, no abiertos). [HUECO] numeracion vigente en el Human Research Roadmap; no se pudo abrir la lista actual.
- [VERIFICADO] Gap 2.02 sobre el valor cuantitativo de tener un CMO con formacion clinica (resultado de busqueda en NTRS 20100028273/20100029652; no abierto en detalle). 02 cita el gap 3.01 de entrenamiento; son numeraciones antiguas (2010).

**Demo 48 h.** Pantalla "tarjeta de decision": estado, razon (que serie cambio y cuanto), banda de incertidumbre, accion sugerida de un protocolo ficticio (sin afirmar clinica) y enlace a "ver datos". Probar con 2-3 personas el tiempo hasta entender la alerta (mini prueba de usabilidad, n pequeno y declarada como tal).

**Riesgos.** Sugerir acciones medicas sin validacion clinica; usar un LLM aumenta riesgo de afirmaciones falsas [SUPOSICION]. Mantener reglas deterministas y texto plantillado.

**Etiqueta.** Requisitos [VERIFICADO]; implementacion [SUPOSICION].

---

## 4. Salud conductual y cognicion en aislamiento (medidas ligeras validadas)

**Que es.** Indicadores breves y repetibles (PVT-B, sueno/actividad, estado de animo, habla) combinados en una linea base personal.

**Evidencia.**
- [VERIFICADO] PVT Self Test / "Reaction Self Test": 3 minutos, sin efecto de aprendizaje apreciable, en uso en ISS desde 2009; se desarrollo en NEEMO. https://www.psytoolkit.org/library/pvtb.html y https://www.thedp.com/article/2009/09/med_school_researcher_david_dinges_creates_stress_tests_for_astronauts (busqueda). Software de alerta de Pulsar Informatics financiado por SBIR/JSC, https://ntrs.nasa.gov/citations/20140000075 (abierta; no da metricas).
- [VERIFICADO] Bateria Cognition: 10 tests, ~20 min, 11 aplicaciones en 6 meses en ISS, parte de las "Standard Measures" de NASA; 15 versiones por test. https://www.med.upenn.edu/uep/cognition.html (busqueda) y https://pmc.ncbi.nlm.nih.gov/articles/PMC7198903/ (abierta, HERA).
- [VERIFICADO] Mars-500: medidas semanales BDI-II, POMS, conflictos, PVT-B y escalas visuales analogicas; actigrafia y luz continuas; diferencias individuales fuertes, un tripulante con ciclo de 25 h y otro con insomnio y mas errores en PVT. https://www.med.upenn.edu/uep/assets/user-content/documents/PNAS2013Basner1212646110withSupportingAppendix.pdf (busqueda)
- [VERIFICADO] HERA: sueno restringido empeora reconocimiento de emociones; privacion total ralentiza PVT y velocidad cognitiva. Datos crudos solo via LSDA con IRB (no usables en 48 h). https://pmc.ncbi.nlm.nih.gov/articles/PMC7198903/ (abierta)
- [VERIFICADO con reservas] SIRIUS: estudio de caracteristicas acusticas del habla con aumento de shimmer y numero de impulsos de voz; solo resumen de congreso. https://p.iafastro.directory/iac/paper/id/63717/abstract-pdf/IAC-21,A1,1,3,x63717.brief.pdf (busqueda). [HUECO] datos de habla de HI-SEAS/SIRIUS no se encontraron como descarga abierta.
- [VERIFICADO] "Detachment" de control de mision en analogos (Mars-500, SIRIUS), con depresion y menor motivacion segun nota de prensa (https://www.frontiersin.org/news/2021/11/09/isolation-mars-communication-sirius-russia, busqueda).
- [HUECO] No se hallaron resultados publicados de CHAPEA 1 (ya registrado en 02). Una nota de NASA de 200 dias existe (https://www.nasa.gov/humans-in-space/nasas-simulated-mars-mission-marks-200-days-inside-habitat/, no abierta).

**Demo 48 h.** Implementar un PVT de 3 min en el navegador (tiempos de reaccion, lapsos >500 ms, falsos arranques; criterio de la literatura PVT-B) y combinarlo con sueno de Sleep-Accel de otro sujeto como "demo de integracion", etiquetandolo claramente. Un test propio genera datos reales de los jueces/asistentes: es la forma de tener "datos de usuario" sin datos NASA, con consentimiento y sin guardar nada identificable.

**Riesgos.** Implementar fielmente la PVT-B y su puntuacion exige cuidado (latencia del navegador, ~10-50 ms de jitter [SUPOSICION]). No hay dataset abierto de habla en aislamiento verificado; el modulo de voz seria solo hipotesis.

**Etiqueta.** Medidas y analogos [VERIFICADO]; voz [HUECO/SUPOSICION].

---

## 5. Fusion multisenal con manejo explicito de calidad de datos

**Que es.** Un indice de calidad por ventana (muestras perdidas, artefactos de movimiento) que condiciona el peso de cada senal en la fusion y fuerza la abstencion.

**Evidencia.**
- [VERIFICADO] Estudio con PPG comercial (3 hombres sanos, 124 h; datos NO publicos): solo 0,6 % de las ventanas de 60 s sin perdida de datos; FC media con 3,2 % de error mediano, HRV de corto plazo con 64 % de error (potencia HF) y 25 % (LF); filtrando ventanas sin perdidas los errores bajan a 0,0 %, 27 % y 6,4 %. https://pmc.ncbi.nlm.nih.gov/articles/PMC8400129/ (abierta)
- [VERIFICADO] Un SQI evita deteccion de latidos sobre senal defectuosa (resultado de busqueda; https://marcoaltini.substack.com/p/data-quality-for-heart-rate-variability, blog, no primario).
- [HUECO] Cuantificacion especifica de artefactos en microgravedad no localizada en esta busqueda.

**Demo 48 h.** Calcular el indice de perdida (L) sobre Sleep-Accel (FC irregular) y mostrar la caida de fiabilidad de HRV con la perdida; a continuacion, desactivar HRV y mantener solo FC media cuando L es alto. Incluye un control de "corromper senal" para el jurado.

**Riesgos.** Es un angulo tecnico poco vistoso; hay que contarlo como "el sistema sabe cuando no puede saber" [SUPOSICION]. Sinergia natural con 1: la abstencion se alimenta del indice de calidad.

**Etiqueta.** Magnitudes de error [VERIFICADO] (n=3, terrestre, otro dispositivo); transferencia a Sleep-Accel y microgravedad [SUPOSICION].

---

## 6. Radiacion e indicadores inmunes indirectos; bucles de contramedidas

**Que es.** Alinear contexto de radiacion/clima espacial con tendencias fisiologicas, y buscar signos tempranos de enfermedad en temperatura/FC/respiracion nocturnas; cerrar el bucle con luz, ejercicio y horarios.

**Evidencia.**
- [VERIFICADO] RadLab (OSDR): telemetria de radiacion de ISS y mas alla de LEO desde varias agencias; API con salida CSV/TSV/JSON/HTML. https://visualization.osdr.nasa.gov/radlab/ (abierta). Instrumentos (DORELI: DOSTEL, Lidal, REM; Liulin-5; RAD/REM/TEPC de SRAG). https://astrobiology.com/2024/03/03/nasa-open-science-for-life-in-space-the-radlab-portal-radlab-data-api/ (busqueda). [HUECO] la documentacion de ejemplos de peticion no se leyo (la pagina de tutoriales no la trae); abrir https://visualization.osdr.nasa.gov/radlab/gui/data-api/ antes de comprometerse.
- [VERIFICADO] DONKI (NASA): CME, flares, SEP, tormentas geomagneticas, via https://api.nasa.gov (DEMO_KEY para pruebas; limites exactos [HUECO]). NOAA SWPC: JSON publico sin clave en https://services.swpc.noaa.gov, flujos de protones GOES >=10 MeV alineados con escala S (busqueda).
- [VERIFICADO] Deteccion de fiebre/enfermedad con wearables: TemPredict, >65.000 participantes con anillo Oura, deteccion en 93 % de casos ~3 dias antes (segun nota; AUROC 0,85 y 0,8 % falsos positivos a sensibilidad 0,50, segun resumen). https://pmc.ncbi.nlm.nih.gov/articles/PMC10975930 (busqueda; cifras de prensa, contrastar con el articulo).
- [VERIFICADO] Luz como contramedida circadiana: Solid-State Lighting Assemblies instalados en 2016 en ISS con horarios dinamicos de luz blanca enriquecida en azul (6500 K, 420 lux) tras el sueno/turno; astronautas reportaron mejor descanso. https://ntrs.nasa.gov/api/citations/20160006727/downloads/20160006727.pdf y https://earthsky.org/human-world/blue-light-helps-astronauts-regulate-body-clock/ (busqueda; sin medida cuantitativa leida).
- [HUECO] Un wearable no mide radiacion biologica ni valida reactivacion viral (01-fisiologia). [HUECO] No se verifico correlacion entre eventos solares y HRV/sueno de astronautas.

**Demo 48 h.** Linea de tiempo "contexto ambiental + estado personal": consulta de DONKI/SWPC (JSON) y RadLab, superpuestos a la serie fisiologica de un sujeto analogo; recomendador de luz/horario con reglas simples y rotulado como heuristica. Cumple el requisito de usar datos NASA con APIs sin acceso restringido.

**Riesgos.** Tentacion de sugerir causalidad radiacion-fisiologia sin base [SUPOSICION]; en LEO la dosis es baja comparada con espacio profundo [SUPOSICION, no contrastado]. Mantener formato "contexto", no "inferencia".

**Etiqueta.** APIs [VERIFICADO]; relacion con salud [SUPOSICION/HUECO].

---

## 7. APIs y herramientas abiertas utilizables el dia 1

- [VERIFICADO] OSDR Biological Data API v2, sin autenticacion (JSON/CSV/TSV); tambien API de busqueda `https://osdr.nasa.gov/osdr/data/search`. https://visualization.osdr.nasa.gov/biodata/api/ y https://osdr-tutorials.readthedocs.io/en/latest/pages/guides/biological_data_api.html (busqueda; 03 ya la listaba).
- [VERIFICADO, nuevo] OSDR en AWS Open Data: bucket `nasa-osdr` (us-west-2), acceso sin cuenta (`aws s3 ls --no-sign-request s3://nasa-osdr/`), "no hay restricciones de uso" segun la ficha; contenido ALSDA y GeneLab (ómicas, organismos modelo, algunos datos de astronautas comerciales). https://registry.opendata.aws/nasa-osdr/ (abierta). Cierra parcialmente el [HUECO] de licencia de 03 para el repositorio (no necesariamente para cada estudio).
- [VERIFICADO] RadLab Data API (arriba), DONKI via api.nasa.gov, NOAA SWPC JSON (arriba).
- [VERIFICADO] Pagina Resources de Space Apps: devolvio 522 en un intento y en el otro solo FAQs/Guides, sin datasets ni referencias a ISS o salud (misma conclusion que 03). https://www.spaceappschallenge.org/resources/. [HUECO] no hay "pagina de recursos ISS" verificable; el enunciado del 28 oct es la fuente.
- [HUECO] No se encontro un proyecto NASA open-source de software medico utilizable (p. ej. la Medical Data Architecture) con repositorio publico; solo menciones en NTRS (https://ntrs.nasa.gov/citations/20220017869 no abierto). Verificar el 28 oct si el reto enlaza alguno.
- [HUECO] LSDA/LSAH siguen requiriendo solicitud e IRB (03).

---

## Shortlist priorizada (diferenciacion x factibilidad 48 h x ajuste a criterios)

Puntuacion 1-5 por eje, estimaciones propias [SUPOSICION]. Criterios de jurado: Impact, Creativity, Validity, Relevance, Presentation (escala real [HUECO]).

| # | Angulo | Dif. | Fact. | Ajuste | Nota |
|---|---|---|---|---|---|
| 1 | 1+5: linea base personal con intervalos calibrados y abstencion guiada por calidad de datos | 4 | 4 | 4 | Maximo Validity; narrativa "sabe cuando no sabe"; datos ya disponibles (Sleep-Accel) |
| 2 | 3: tarjeta de decision explicable para el CMO (que hacer, por que, confianza) | 4 | 4 | 5 | Requisito literal del paper CDSS/EIMO; sube Impact y Presentation |
| 3 | 4: PVT-B de 3 min propio + sueno como modulo de cognicion/conducta | 3 | 4 | 4 | Medida validada con historia en ISS; genera datos propios en demo |
| 4 | 2: autonomia offline con simulador de retardo y presupuesto de recursos | 2 | 3 | 5 | Relevance maxima pero idea esperable; solo lo suficiente para la demo de 30 s |
| 5 | 6: linea de tiempo de contexto ambiental (RadLab/DONKI/SWPC) + luz/horario como contramedida | 3 | 3 | 4 | Cumple dato NASA con APIs abiertas; riesgo de sobreafirmar causalidad |

Combinacion sugerida: 1 como motor, 2 como interfaz, 4 como modulo de entrada, 2/offline como marco narrativo minimo, 6 como panel de contexto solo si sobra tiempo. Todo sujeto a revalidacion el 28 oct.

Descartado como eje: voz/habla (sin dataset abierto verificado), imagen (CMO-DA multimodal exige modelos y evaluaciones fuera de 48 h).
