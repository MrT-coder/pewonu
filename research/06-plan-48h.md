# 06 - Plan de preparacion y de 48 h

> Nota (2026-10-28): el equipo es de 3 personas y la idea cambio (ver [docs/idea-base.md](../docs/idea-base.md) y [docs/equipo.md](../docs/equipo.md)). Los roles y el plan por horas de abajo estan pendientes de ajuste.

> Nota (2026-10-02): las dependencias del 28 oct (enunciado completo, datasets oficiales, guia de jueces 2026, vigencia de 30 s / 7 slides) se conectan con 07-angulos-de-idea.md: el reparto actual de angulos (motor = linea base + abstencion; interfaz = tarjeta de decision; marco = offline minimo; PVT-B y contexto ambiental opcionales) esta en 04-ideas.md, seccion "Actualizacion con 07...". Revalidar 04, 06 y 07 ese dia antes de congelar alcance. Este plan no se reescribio. [DEPENDE-28OCT]

Etiquetas: [VERIFICADO] respaldado por fuente en 01-05; [SUPOSICION] inferencia propia; [HUECO] no confirmado; [DEPENDE-28OCT] depende del enunciado completo que se publica el 28 oct 2026.
Fechas: hackathon 14-15 nov 2026; envio sab 9:00 a dom 23:59 hora local [VERIFICADO: https://www.spaceappschallenge.org/2026/]. Juicio desde el 16 nov [VERIFICADO: astrobiology.com, ver 05-ganadores.md].
Nota: este documento es solo planificacion; no contiene codigo del proyecto.

## 1. Antes del evento (hoy 2 oct a 13 nov)

### 1.1 Hitos
| Fecha | Accion |
|---|---|
| Ya | Confirmar equipo (1-6 miembros, todos registrados) [VERIFICADO guia 2022] |
| 28 oct | Leer enunciado y datasets oficiales; reevaluar 04-ideas.md [DEPENDE-28OCT] |
| 29 oct - 6 nov | Descargar y explorar datasets; elegir concepto |
| 7-12 nov | Prueba general de demo y video; checklist de envio |
| 13 nov | Congelar herramientas; dormir |

### 1.2 Herramientas (sin codigo de proyecto)
- Familiarizarse con: lectura de EDF/WFDB (p. ej. paquete `wfdb` de PhysioNet [SUPOSICION: confirmar la libreria]), pandas, Jupyter; OSDR API REST (`GET /v2/datasets/`, formatos csv/json) [VERIFICADO: https://visualization.osdr.nasa.gov/biodata/api/].
- Practicar una PWA offline (service worker, almacenamiento local) para el concepto B [SUPOSICION].
- Cuenta de repositorio publico y hosting externo para demo/video (YouTube/Drive/GitHub) [VERIFICADO guia 2022: el portal no admite subir archivos].

### 1.3 Datasets: descarga y familiarizacion
- Sleep-Accel (2,2 GB, ODC-BY): descargar 3-5 sujetos; entender columnas (aceleracion, FC, pasos, etapas PSG) [VERIFICADO 03-datos.md].
- WESAD: descargar via `ucimlrepo` o web de origen; comprobar licencia antes de redistribuir [HUECO licencia].
- OSDR API: 5-10 consultas de ejemplo; guardar respuestas JSON para modo offline.
- MIMIC-IV Waveform (opcional): solo 2-3 registros (12,8 GB total) [VERIFICADO 03-datos.md].
- Revisar el 28 oct si el reto lista datasets propios; priorizarlos [DEPENDE-28OCT].
- No intentar LSAH, controlado OSDR, DREAMT ni Mars-500 crudo [VERIFICADO: inviables en 48 h].

### 1.4 Roles (equipo de 4-6; ajustar)
| Rol | Responsabilidad |
|---|---|
| Datos/ciencia | Pipeline de datos, linea base, bandas de error, redaccion de limites |
| Ingenieria app | Interfaz, modo offline, sincronizacion simulada |
| Diseno/UX | Flujo de CMO, pantallas, identidad visual |
| Narrativa/video | Storyboard, guion en ingles, subtitulos, diapositivas |
| Coordinacion | Cronograma, integracion, checklist de envio y enlaces |
[SUPOSICION] La guia 2020 recomienda dedicar gente a Presentation [VERIFICADO 05-ganadores.md].

### 1.5 Storyboard del demo (modelo "30 Seconds of Glory", guia 2022 [VERIFICADO])
- 0:00-0:05 Quien somos y el reto; nombre + tagline.
- 0:05-0:15 Problema: Marte, retraso de ~3-22 min, CMO no medico [VERIFICADO con reservas].
- 0:15-0:25 Demo: cortar enlace, alertas siguen; estado `insufficient_data` cuando faltan datos.
- 0:25-0:30 Datos usados (NASA OSDR + PhysioNet), futuro e impacto.
Preparar version de 7 diapositivas equivalente; los jueces dejan de ver en 30 s o diapositiva 7 [VERIFICADO].

### 1.6 Checklist de envio (guias 2020/2022; vigencia 2026 por confirmar [HUECO])
- [ ] Pagina de proyecto en ingles; campos obligatorios completos.
- [ ] Demo: video <=30 s (otro idioma permitido con subtitulos en ingles) o <=7 diapositivas en ingles.
- [ ] Un solo enlace de demo, separado del "Final Project"; ambos publicos, sin permiso ni registro; probar en ventana privada.
- [ ] Alojamiento externo (YouTube, Drive, GitHub); el portal no admite archivos.
- [ ] Enlace a repositorio publico si aplica.
- [ ] Uso de al menos algunos datos abiertos de NASA o agencias socias citados en References.
- [ ] Todos los miembros (1-6) registrados; casillas de terminos y trabajo original marcadas; recursos externos listados.
- [ ] Sin lenguaje inapropiado.
- [ ] Enviar antes de dom 23:59 hora local con margen (no subir archivos a ultimo minuto [VERIFICADO fuente secundaria]).
- Confirmar con la guia 2026 todos los limites: https://www.spaceappschallenge.org/resources/judging-awards-guide/ [DEPENDE-28OCT / HUECO].

## 2. Plan hora por hora (48 h)

Referencia: H0 = inicio del evento. Ventana de envio: sab 9:00 a dom 23:59. [SUPOSICION: el evento arranca el sabado por la manana; ajustar si el evento local cambia.]

### Sabado
| Hora | Actividad |
|---|---|
| 09:00-10:00 | Kickoff, releer enunciado, confirmar concepto y alcance (congelar) |
| 10:00-12:00 | Datos: cargar Sleep-Accel/WESAD; esquema comun; maqueta de pantallas |
| 12:00-13:00 | Almuerzo; revision de alcance (recortar) |
| 13:00-17:00 | Motor de linea base + bandas de error + `insufficient_data`; esqueleto de app offline |
| 17:00-18:00 | Integracion 1: flujo de punta a punta con datos reales (aunque feo) |
| 18:00-20:00 | Simulador de enlace/sincronizacion; panel de contexto OSDR |
| 20:00-22:00 | UI funcional; pantalla "Limites" |
| 22:00-24:00 | Guion y storyboard final; congelar funcionalidades (feature freeze al terminar) |
| 00:00-07:00 | Dormir por turnos (minimo 6 h) [SUPOSICION] |

### Domingo
| Hora | Actividad |
|---|---|
| 07:00-09:00 | Correccion de errores; pruebas con casos de abstencion |
| 09:00-12:00 | Pulido UI; README y referencias; datos citados |
| 12:00-14:00 | Grabar video 30 s (varias tomas); subtitulos en ingles |
| 14:00-16:00 | Diapositivas (<=7) de respaldo; pagina de proyecto |
| 16:00-18:00 | Hosting externo, enlaces publicos, prueba en ventana privada |
| 18:00-20:00 | Enviar (primer envio completo) |
| 20:00-22:30 | Mejoras menores solo si hay margen; reenvio si el portal lo permite [HUECO] |
| 22:30-23:30 | Verificar enlaces y envio final |
| 23:59 | Fin de la ventana |

## 3. Stack sugerido (con justificacion; todo [SUPOSICION] salvo indicacion)

- **Datos/analitica: Python (pandas, numpy, scipy)** en Jupyter. Razon: lectura directa de datos de PhysioNet, bootstrap para bandas de error, velocidad de iteracion.
- **App: PWA (TypeScript + framework web ligero) con service worker y almacenamiento local.** Razon: encaja con el concepto offline-first y se aloja de forma publica de modo gratuito; evita instalar apps nativas.
- **Procesamiento en cliente o en un servicio local; sin LLM en la nube.** Razon: coherencia con el retraso de comunicaciones y con EIMO [VERIFICADO 02-estado-del-arte.md]. Si se quisiera un LLM, solo uno local pequeno y opcional, nunca en la ruta critica de alertas.
- **Graficos: libreria de graficos web (p. ej. Chart.js u homologa) con bandas de error visibles.**
- **Control de versiones: repositorio publico en GitHub** (enlace al codigo, guia 2020 [VERIFICADO]).
- **Datos precalculados** guardados como archivos estaticos (JSON) para que la demo no dependa de descargas pesadas.
- Alternativa mas ligera: Streamlit/notebook si el equipo no tiene perfil web; se pierde la demostracion offline real.

## 4. Que NO hacer

- No afirmar capacidad diagnostica ni usar la palabra "detecta enfermedad" [VERIFICADO riesgo en 05-ganadores.md; SUPOSICION].
- No presentar datos terrestres como si fueran de astronautas; indicar siempre "datos analogos".
- No inventar umbrales clinicos ni precision (AUC, % acierto) sin validacion [HUECO umbrales].
- No depender de LLM/API en la nube en la ruta critica.
- No abarcar demasiado: un problema formulable en una frase [VERIFICADO fuente secundaria].
- No usar datos web genericos en lugar de datasets NASA [VERIFICADO fuente secundaria].
- No intentar datos con acceso restringido (LSAH, controlado, DREAMT) ni descargar los 2,4 TB de MIMIC-III.
- No descuidar Presentation: video/diapositivas desde el sabado [VERIFICADO guia 2020].
- No pasar de 30 s / 7 diapositivas; no enlaces privados ni que pidan registro [VERIFICADO].
- No subir archivos ni resolver el hosting a ultima hora.
- No redistribuir datos con licencia no confirmada (WESAD) [HUECO].
- No sacrificar el sueno completamente.

## 5. Elementos que dependen del enunciado del 28 oct

- Datasets o recursos oficiales listados para el reto.
- Foco exacto (monitoreo, prediccion, apoyo al CMO, interfaz de tierra).
- Requisitos de formato o de entregables propios del reto.
- Criterios y escala de la guia de jueces 2026 (1-5 o 10 puntos).
- Vigencia de 30 s / 7 slides, subtitulos en ingles, maximo 6 personas.
- Enlaces a recursos NASA que sustituyan o complementen Sleep-Accel/WESAD/OSDR.
