# 04 - Conceptos de solucion

> Nota (2026-10-28): reanalizado frente al enunciado oficial en [docs/idea-base.md](../docs/idea-base.md). La recomendacion de abajo (usuario CMO) queda reemplazada por la idea base (usuario astronauta).

Reto: "Create Health Monitoring Software for Astronauts on Space Missions" (NASA Space Apps 2026, 14-15 nov; nivel Intermediate).
Etiquetas: [VERIFICADO] respaldado por fuente en 01/02/03/05; [SUPOSICION] inferencia propia; [HUECO] no confirmado.
Los conceptos son solo inspiracion conceptual; no se reutiliza codigo de ningun proyecto previo.

## Restricciones comunes (heredadas de los otros archivos)

- [VERIFICADO] No hay datos abiertos de telemetria real de astronautas en mision; el MVP usa datos analogos terrestres y simula el flujo de a bordo (03-datos.md, secc. 4).
- [VERIFICADO] Datasets utilizables en 48 h segun 03-datos.md: Sleep-Accel (PhysioNet, ODC-BY, FC + aceleracion + etapas PSG, 31 sujetos), WESAD (estres; licencia [HUECO], comprobar antes de redistribuir), OSDR Biological Data API (sin clave; omicas, no senal fisiologica), MIMIC-IV Waveform v0.1.0 (opcional, 2-3 registros).
- [VERIFICADO] Enunciado completo y datasets oficiales se liberan el 28 oct (03-datos.md, 05-ganadores.md). Todo lo de abajo debe revalidarse ese dia.
- [VERIFICADO] Para Global Judging hay que usar al menos algunos datos abiertos de NASA o agencias socias (guia 2022, 05-ganadores.md). OSDR es el unico dataset NASA verificado accesible; por eso aparece como "capa de contexto" en los conceptos.
- [VERIFICADO] Criterios (guia 2020/2022): Impact, Creativity, Validity, Relevance, Presentation. La escala 1-5 no esta confirmada [HUECO]; las puntuaciones de abajo son ESTIMACIONES propias, no medidas.
- [SUPOSICION] Cifras clinicas y umbrales: no hay umbrales de alerta validados para astronautas en orbita [HUECO] (01-fisiologia.md, secc. 5). Se usan linea base personal y rangos terrestres solo como placeholder.

---

## Concepto A - "Baseline": linea base personal e incertidumbre explicita (honesto con la incertidumbre)

- **Problema.** Con 3-6 tripulantes y grandes diferencias individuales (Mars-500, 01-fisiologia.md), los umbrales poblacionales fallan y un veredicto con falsa precision puede danar la confianza del CMO. [VERIFICADO] diferencias individuales; [SUPOSICION] el riesgo de falsa precision.
- **Usuario.** Crew Medical Officer (normalmente no medico; 02-estado-del-arte.md) y, de forma secundaria, el equipo de tierra.
- **Indicadores.** FC en reposo, sueno (duracion, regularidad), actividad; HRV si el dataset lo permite. Cada indicador se expresa como desviacion respecto a la propia linea base con banda de error.
- **Reglas de honestidad (obligatorias).**
  1. Toda salida numerica lleva banda de incertidumbre (p. ej. intervalo bootstrap) visible en la UI.
  2. Estado `insufficient_data` con prioridad sobre cualquier veredicto: si faltan dias de linea base, hay huecos de sensor o la calidad de senal es baja, no se emite "normal" ni "alerta", solo `insufficient_data` y el motivo.
  3. Nunca mostrar mas digitos de los que justifica la banda; sin puntuaciones de "riesgo %" inventadas.
  4. Pantalla "Limites": que datos son analogos y que no se valido en orbita.
- **Demostrable en un fin de semana.** Sleep-Accel por sujeto: construir linea base de las primeras noches, marcar desviaciones en noches posteriores, y mostrar casos en que el sistema se abstiene (sujeto con pocas noches o FC ausente). Se puede inyectar ruido/huecos para demostrar la abstencion. Limite: Sleep-Accel son voluntarios en tierra, no astronautas; no valida deteccion clinica. [VERIFICADO] ficha de dataset en 03-datos.md.
- **Estimacion (1-5, [SUPOSICION]).**
  - Impact 3: ayuda a un CMO sin formacion clinica, pero sin validacion en orbita.
  - Creativity 3: linea base individual no es nueva; la abstencion como caracteristica de primer nivel es poco habitual.
  - Validity 4: lo mas defendible cientificamente; no afirma mas de lo que los datos permiten.
  - Relevance 4: encaja con EIMO y n pequeno (02-estado-del-arte.md, secc. 4).
  - Presentation 3: concepto sutil; requiere buen storytelling para que "no decir nada" se vea como valor.

## Concepto B - "Edge-CMO": monitor offline-first con sincronizacion diferida (offline/edge)

- **Problema.** El retraso unidireccional a Marte es de ~3 a 22 min segun geometria [VERIFICADO con reservas, citar el rango; 02-estado-del-arte.md secc. 5], sin posibilidad de evacuacion; EIMO propone mover el cuidado a sistemas a bordo [VERIFICADO].
- **Usuario.** Astronauta/CMO a bordo; el equipo de tierra recibe un resumen cuando llega el enlace.
- **Indicadores.** Los de Sleep-Accel (FC, movimiento, sueno) y estres (WESAD) calculados localmente.
- **Diseno.**
  - Todo el analisis corre en el dispositivo (PWA o app local): sin LLM ni servicio en la nube; reglas y estadistica ligera, explicables.
  - Cola local de eventos con marca de tiempo y deduplicacion; sincronizacion diferida y reanudable hacia "Tierra".
  - Simulador de enlace con retardo configurable (3-22 min) y cortes, para demostrar que las alertas locales no dependen del enlace.
  - Registro de auditoria local (trazabilidad de cada alerta: dato de entrada, regla, version).
- **Demostrable en un fin de semana.** Reproducir un registro de Sleep-Accel/WESAD como "flujo de sensor", activar modo avion y mostrar que las alertas siguen; luego restaurar el enlace con retraso simulado y mostrar la sincronizacion. Limite: el retardo es simulado, no hay hardware de mision ni datos reales de nave [SUPOSICION: es consecuencia de diseno, no requisito oficial NASA; 02-estado-del-arte.md].
- **Estimacion (1-5, [SUPOSICION]).**
  - Impact 4: aborda directamente una restriccion real de misiones a Marte.
  - Creativity 3: offline-first es ingenieria solida pero predecible; el simulador de retardo ayuda a la narrativa.
  - Validity 3: arquitectura verificable en demo; la parte clinica depende de datos analogos.
  - Relevance 5: coincide con EIMO y con el nucleo del reto.
  - Presentation 4: demo visual clara (cortar enlace, seguir funcionando) en 30 s.

## Concepto C - "Cross-Domain Early Warning": tendencias multidominio y contexto NASA

- **Problema.** Los riesgos del HRP (inmune, cardio, conductual, sueno) se vigilan por separado; las tendencias combinadas podrian dar alerta temprana, pero eso no esta validado en orbita [HUECO] (01-fisiologia.md, secc. 3).
- **Usuario.** CMO y equipo de tierra.
- **Indicadores.** Sueno + FC + actividad (Sleep-Accel), carga de estres (WESAD); capa de contexto con estudios OSDR relacionados con cada riesgo (consulta via API).
- **Demostrable.** Panel que fusiona dos fuentes en una "linea de tiempo de carga fisiologica" y enlaza cada alerta con estudios de vuelo OSDR relevantes. Limite: Sleep-Accel y WESAD son sujetos distintos; la fusion es una demostracion de integracion, no de inferencia clinica; hay que decirlo en pantalla. OSDR no aporta senal en vivo [VERIFICADO 03-datos.md].
- **Estimacion (1-5, [SUPOSICION]).**
  - Impact 3: util conceptualmente, sin evidencia de eficacia.
  - Creativity 4: la union salud-en-tiempo-real + contexto de estudios NASA es atractiva.
  - Validity 2: la fusion de sujetos distintos es debil; el riesgo de sobreafirmar es alto.
  - Relevance 4: responde al reto y usa datos NASA (cumple requisito de datos abiertos NASA).
  - Presentation 4: visualmente vistoso.

## Concepto D - "Crew Dashboard + Contramedidas": monitoreo con recomendaciones de ejercicio y sueno

- **Problema.** Los proyectos de salud nominados suelen mezclar monitoreo con contramedidas (ejercicio, psicologia) [VERIFICADO: ExoBox, Astro State; 05-ganadores.md]. La perdida osea de ~1-2 %/mes [VERIFICADO con reservas, cifras a contrastar con el original; 01-fisiologia.md] motiva medir carga mecanica.
- **Usuario.** Astronauta (autoseguimiento) y CMO.
- **Indicadores.** Minutos de actividad y sueno (Sleep-Accel); estres (WESAD). Proxy de carga osea desde aceleracion es [SUPOSICION], sin validar.
- **Demostrable.** App movil/web que muestra el estado diario y sugiere ajustes (hora de dormir, bloque de ejercicio) con reglas simples. Limite: no hay datos de ejercicio resistivo en orbita; las recomendaciones son heuristicas, no clinicas.
- **Estimacion (1-5, [SUPOSICION]).**
  - Impact 3, Creativity 2 (patron ya visto en proyectos previos), Validity 2 (recomendaciones sin respaldo clinico), Relevance 3, Presentation 4.

## Concepto E (opcional) - "Insight Lab": dashboard de investigacion sobre OSDR

- **Problema.** SpaceGenes+ gano Best Use of Science con un dashboard para investigadores sobre radiacion/microgravedad [VERIFICADO; 05-ganadores.md]. Se desplaza el foco de monitoreo clinico a exploracion de datos.
- **Usuario.** Investigador del HRP, no el astronauta.
- **Demostrable.** Explorador de estudios OSDR (API sin clave) por riesgo del HRP y por tipo de ensayo. Limite: se aleja del texto del reto ("software de monitoreo de salud para astronautas") [SUPOSICION], pudiendo perder Relevance.
- **Estimacion (1-5, [SUPOSICION]).** Impact 3, Creativity 3, Validity 4 (datos reales NASA), Relevance 2, Presentation 3.

---

## Tabla comparativa (estimaciones propias, no verificadas)

| Concepto | Impact | Creativity | Validity | Relevance | Presentation | Total (de 25) |
|---|---|---|---|---|---|---|
| A Baseline (honesto) | 3 | 3 | 4 | 4 | 3 | 17 |
| B Edge-CMO (offline) | 4 | 3 | 3 | 5 | 4 | 19 |
| C Cross-Domain | 3 | 4 | 2 | 4 | 4 | 17 |
| D Contramedidas | 3 | 2 | 2 | 3 | 4 | 14 |
| E Insight Lab | 3 | 3 | 4 | 2 | 3 | 15 |

## Recomendacion

Combinar B y A: una app offline-first (B) cuyo motor de alertas sea el de linea base con bandas de error y `insufficient_data` (A). Cubre Relevance (EIMO, retraso de comunicaciones), Validity (no sobreafirma) y da una demo de 30 s clara (cortar enlace, seguir alertando, abstenerse cuando faltan datos). Usar OSDR (de C/E) solo como panel de contexto con enlaces, para cumplir el requisito de datos NASA sin sobrecargar el alcance.

Tradeoffs:
- Honestidad vs. espectacularidad: abstenerse y mostrar bandas luce menos que un "score" con colores; hay que contarlo en el relato (Presentation).
- Offline-first agrega trabajo de ingenieria (cola, sync, simulador) que compite con el tiempo de pulido; recortar a un simulador de enlace minimo.
- Datos analogos: ninguna afirmacion clinica; presentar como prototipo de arquitectura y de metodo.
- Todo depende del enunciado del 28 oct [HUECO]; si el reto trae datasets o un enfoque distinto, reevaluar antes de comprometerse.

---

## Actualizacion con 07-angulos-de-idea.md y adendas de 05

Fecha: 2026-10-02. Etiquetas: [VERIFICADO] respaldado por 05/07; [SUPOSICION] inferencia propia; [HUECO] no confirmado. Todo lo anterior de este archivo se conserva; esta seccion lo reconcilia, no lo reemplaza. Las puntuaciones son ESTIMACIONES propias [SUPOSICION], no medidas.

### 1. Correspondencia entre los cinco conceptos y los angulos priorizados de 07

| Angulo 07 (rango) | Concepto 04 | Relacion | Que aporta de nuevo |
|---|---|---|---|
| 1. Linea base personal + intervalos calibrados + abstencion | A (Baseline) | Es A con mas rigor; absorbe el angulo 5 de 07 (indice de calidad de datos) | Detector CUSUM/EWMA con referencia publicada (Mishra 2020, Scripps DETECT), intervalo conformal split, cobertura empirica visible, abstencion guiada por calidad de senal [VERIFICADO en 07; aplicabilidad a astronautas SUPOSICION] |
| 2. Tarjeta de decision explicable para el CMO | Sin equivalente directo (04 solo menciona "alerta"); toca A y B | Nuevo, pasa a ser la capa de interfaz | Requisito literal del paper CDSS/EIMO: que hacer, por que, como se decidio [VERIFICADO en 07]; mini prueba de usabilidad con n pequeno declarada como tal |
| 3. PVT-B de 3 min + modulo de sueno/conducta | Sin equivalente (01 lo dejaba como SUPOSICION de cognicion breve); parcialmente D | Nuevo, modulo de entrada | Medida con historia en ISS [VERIFICADO en 07]; genera datos propios del jurado sin datos NASA; riesgo de jitter del navegador [SUPOSICION] |
| 4. Autonomia offline con simulador de retardo | B (Edge-CMO) | Igual a B; 07 la califica de idea esperable | Presupuesto de recursos visible (latencia, KB, bytes sincronizados) [SUPOSICION: diseno propio] |
| 5. Linea de tiempo de contexto ambiental (RadLab/DONKI/SWPC) | C (Cross-Domain), reducido | C sin la fusion de sujetos distintos; solo contexto | APIs abiertas que cumplen el requisito de dato NASA [VERIFICADO en 07]; relacion con salud [SUPOSICION/HUECO], formato "contexto", no inferencia |

Conceptos sin angulo propio en 07: D (Contramedidas) queda reducido a la heuristica de luz/horario dentro del angulo 5; E (Insight Lab) sigue como opcion fuera de foco por Relevance baja (04) y por el patron de premios por categoria (ver 3).

### 2. Recomendacion revisada

La recomendacion previa (B + A) se mantiene en espiritu pero cambia el reparto de peso. Motivo: 07 indica que el offline es lo mas predecible (varios equipos lo propondran, novedad baja [SUPOSICION]) y que la tarjeta de decision responde a un requisito literal de EIMO/CDSS que 04 no habia explotado.

- **Motor:** angulo 1 (A + calidad de datos). Maximiza Validity y la narrativa "sabe cuando no sabe".
- **Interfaz:** angulo 2, tarjeta de decision para el CMO (estado, razon, banda de incertidumbre, accion de protocolo ficticio, enlace a datos). Reglas deterministas y texto plantillado; sin LLM en la ruta critica.
- **Marco minimo:** angulo 4 (B), recortado al conmutador de enlace con retardo configurable y a una demo de 30 s; no un proyecto de ingenieria completo.
- **Modulo opcional:** angulo 3 (PVT-B) solo si el equipo tiene perfil web; da "datos de usuario" propios.
- **Panel de contexto:** angulo 5 solo si sobra tiempo; OSDR/RadLab/DONKI/SWPC como contexto con enlaces, para cumplir el requisito de dato NASA.

Estimacion de la combinacion "1 + 2 con marco 4" (1-5, [SUPOSICION], no verificado): Impact 4, Creativity 3, Validity 4, Relevance 5, Presentation 4, total estimado 20 de 25. Es una estimacion propia comparable con la tabla anterior (B 19, A 17), no una medida. La escala real de la guia 2026 sigue en [HUECO].

Tradeoffs nuevos:
- La tarjeta de decision aumenta el riesgo de sugerir acciones medicas sin validacion; mitigar con protocolo ficticio rotulado y la pantalla "Limites".
- Sumar PVT-B y panel ambiental compite con el pulido de Presentation; recortar primero esos dos.
- Sin eventos clinicos etiquetados en Sleep-Accel, solo se valida cobertura estadistica, no deteccion de enfermedad [SUPOSICION, 07]. No usar "detecta enfermedad".

### 3. Leccion de los premios 2025 y el precedente de 42 QuakeHeroes

- [VERIFICADO, 05 Adenda 2026-10-03] En 2025 los 10 Global Winners se repartieron por categoria (Best Use of Science, Data, Technology, Galactic Impact, Best Mission Concept, Most Inspirational, Best Storytelling, Global Connection, Art & Technology, Local Impact). Leccion [SUPOSICION]: apuntar a una categoria clara, no a todas. Candidata natural para esta combinacion: Best Use of Technology (edge + modelo explicable) [SUPOSICION]; el relato de abstencion tambien podria sostener Best Use of Science, pero eso no esta verificado.
- [VERIFICADO, 05 Adenda 2] Los ganadores combinan tecnologia con un usuario o decision concreta (agricultor, persona ciega, estudiante). Aqui el usuario es el CMO y la decision es "que hacer ahora"; por eso la tarjeta de decision (angulo 2) debe ser el centro de la demo, no un grafico.
- [VERIFICADO, 05 Adenda 2] Precedente 42 QuakeHeroes (2024, Best Use of Technology): el reto pedia decidir a bordo que datos enviar por limite de energia de transmision, es decir, razonamiento edge, y entregaron cuaderno en GitHub, video y web explicativa. [SUPOSICION] Un monitor que decide a bordo que alertar y que transmitir con el enlace degradado encaja con un criterio ya premiado; no hay evidencia de que sea suficiente.
- [VERIFICADO] Discrepancia resuelta 2026-10-03: SpaceGenes+ gano Best Use of Science. La tabla previa de la adenda de 05 estaba corrida una fila porque en la pagina oficial la insignia va antes del nombre; ya esta corregida. Fuente: https://www.spaceappschallenge.org/2025/awards/global-winners/
- [SUPOSICION, 05] La incertidumbre explicita no aparece como diferenciador en ninguno de los 20 ganadores 2023-2024; puede diferenciar, pero no hay evidencia de que los jueces la valoren. Contarla como valor para el usuario ("el CMO sabe cuanto fiarse"), no como virtud tecnica abstracta.

### 4. Pendiente de revalidar el 28 oct

Enunciado completo, datasets oficiales y guia de jueces 2026 pueden cambiar el foco (monitoreo, prediccion, apoyo al CMO, interfaz de tierra). Si el reto lista datasets propios, priorizarlos sobre Sleep-Accel/WESAD y reevaluar esta recomendacion [DEPENDE-28OCT].
