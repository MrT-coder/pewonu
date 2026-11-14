# 03 - Datos abiertos para un MVP de 48 h

Reto: "Create Health Monitoring Software for Astronauts on Space Missions" (NASA Space Apps 2026, hackathon 14-15 nov 2026).
Fecha de la investigación: 2026-10-02.
Etiquetas: [VERIFICADO] = visto en la página citada; [SUPOSICION] = inferencia mía; [HUECO] = no se pudo confirmar.

## 1. Qué publica hoy spaceappschallenge.org/2026 para este reto

- [VERIFICADO] La página principal indica que los "Challenge Summaries" están publicados y que hay 14 retos. No menciona datasets. Fuente: https://www.spaceappschallenge.org/2026/
- [VERIFICADO] La página de Resources solo muestra Participant FAQs y Participant Guides, y avisa que se actualizará periódicamente. No hay datasets específicos de 2026. Fuente: https://www.spaceappschallenge.org/resources/
- [VERIFICADO] Fechas: registro desde el 26 ago; formación de equipos 17 sep; hackathon 14-15 nov; entrega 15 nov 23:59 hora local. Fuente: https://www.spaceappschallenge.org/2026/
- [VERIFICADO] Los enunciados completos y los datasets NASA se liberan el 28 oct. Fuente: https://astrobiology.com/2026/09/04/registration-is-now-open-for-the-2026-nasa-space-apps-challenge/
- [VERIFICADO] Un medio rumano confirma que el reto de "aplicación para monitorizar la salud de astronautas" es uno de los 14. Fuente: https://zilesinopti.ro/?p=892787
- [HUECO] No pude leer el texto del reto: las páginas /challenges/ y la del reto cargan contenido dinámico y la lectura devolvió solo la navegación. Por tanto no se puede afirmar qué recursos o datasets lista el reto hoy. Fuente intentada: https://www.spaceappschallenge.org/2026/challenges/
- [SUPOSICION] Lo habitual es que el enunciado enlace datasets de NASA y agencias socias el 28 oct. Hay que revisar la página del reto ese día.

Conclusión: hoy no hay datasets oficiales verificables para este reto. El plan debe funcionar con datos públicos ya disponibles y dejar un hueco para adaptar a lo que publiquen el 28 oct.

## 2. Fuentes NASA

### 2.1 NASA OSDR / GeneLab (Open Science Data Repository)
- URL: https://science.nasa.gov/biological-physical/data/ (portal); API: https://visualization.osdr.nasa.gov/biodata/api/ ; tutoriales: https://osdr-tutorials.readthedocs.io/
- Acceso: [VERIFICADO] búsqueda web y API REST. La especificación de la API no documenta autenticación. Endpoints: `GET /v2/datasets/`, `/v2/dataset/{accession}/`, `/v2/query/datasets|assays|samples/`. Formatos de salida: csv (por defecto), tsv, json.records, json.table, json.split. Fuente: https://visualization.osdr.nasa.gov/biodata/api/
- Existe además RadLab (radiación a bordo de ISS y misiones más allá de LEO; CSV/TSV/JSON y API). Fuente: https://visualization.osdr.nasa.gov/radlab/
- Datos humanos: [VERIFICADO] los datos procesados e inmunes a la identificación de Inspiration4 (10 estudios, OSD-569 a 575, 630, 656, 687) son públicos; los datos crudos individuales (secuencias genéticas) requieren solicitud con aprobación IRB. Contenido: ómicas, hemograma, paneles metabólicos y de citoquinas. El artículo no menciona wearables. Formatos: ISA-Tab, CSV, FASTQ. Fuente: https://pmc.ncbi.nlm.nih.gov/articles/PMC11094041
- Controlado: [VERIFICADO] requiere formulario DAR, documento IRB, afiliación institucional y comité; el acceso caduca al año. Inviable en 48 h. Fuente: https://osdr-tutorials.readthedocs.io/en/latest/pages/guides/request_controlled_access_datasets.html
- Licencia: [HUECO] los tutoriales indican que los términos están en cada estudio; no encontré una licencia global. Cuenta Login.gov mencionada en los tutoriales para algunas funciones. Fuente: https://osdr-tutorials.readthedocs.io/
- Tamaño: [HUECO] no confirmado (varía por estudio).
- Mars-500: [VERIFICADO] solo hay en OSDR el estudio de microbiota intestinal (GLDS-191), según el buscador; no confirmé el contenido de la página porque no cargó. Fuente: https://osdr.nasa.gov/genelab/accession/GLDS-191
- Uso en demo 48 h: **parcial**. La API es muy cómoda (sin clave, CSV/JSON) pero los datos son ómicas de organismos, no series fisiológicas en tiempo real. Útil como "capa de contexto biomédico" (por ejemplo, enlazar un riesgo con estudios de vuelo), no como señal de monitorización. Datos humanos públicos: solo tablas procesadas y laboratorios clínicos de 4 tripulantes.

### 2.2 NASA Life Sciences Data Archive (LSDA) y Lifetime Surveillance of Astronaut Health (LSAH)
- URL: https://nlsp.nasa.gov/ (portal NLSP); descripción: https://www.nasa.gov/directorates/esdmd/hhp/life-sciences-data-archive-lsda/
- [VERIFICADO] LSDA guarda datos humanos desidentificados de vuelo y análogos desde 1961; LSAH guarda datos médicos de vigilancia de astronautas. Hay un flujo de "Request Data" con formularios. Fuente: la página de nasa.gov anterior.
- [VERIFICADO] Las solicitudes pasan por un grupo de revisión (EBWG) y las de datos atribuibles van al LSAH Policy Board. Existe helpdesk. Condición de uso: todo resumen, presentación o manuscrito se revisa por atribuibilidad. Fuentes: https://ntrs.nasa.gov/citations/20150021210 y resumen de búsqueda sobre https://nlsp.nasa.gov/explore/lsdahome/lsahhome
- [VERIFICADO] Colección de acceso abierto: estudios de reposo en cama con inclinación de cabeza (UTMB), que imitan los desplazamientos de fluidos en microgravedad. Fuente: https://www.nasa.gov/directorates/esdmd/hhp/life-sciences-data-archive-lsda/
- Formato, tamaño y licencia de esa colección: [HUECO]. Las páginas de nlsp.nasa.gov cargan dinámicamente y no pude leer el catálogo.
- Uso en demo 48 h: **no** para LSAH (datos atribuibles, proceso de solicitud, tiempos no confirmados). **Posible, a verificar** para la colección abierta de bedrest, solo si se confirma qué variables trae. [SUPOSICION] la descarga abierta podría servir como ejemplo de cambios fisiológicos de microgravedad simulada.

### 2.3 Mars-500 y análogos
- [VERIFICADO] ESA documenta que Mars-500 recogió actigrafía, ECG Holter de 24 h, HRV, presión, etc. Fuentes: https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Mars500/Mars500_Scientific_protocols10 y la búsqueda sobre publicaciones.
- [HUECO] No encontré descarga pública de las series de actigrafía/ECG de Mars-500. Solo hay publicaciones con resultados agregados y el estudio de microbiota (GLDS-191) en OSDR/data.gov: https://catalog.data.gov/dataset/temporal-dynamics-of-the-gut-microbiota-in-people-sharing-a-confined-environment-a-520-day
- Uso en demo: **no** (sin datos crudos abiertos verificados). Se puede citar como inspiración de los parámetros a monitorizar.

## 3. Datos públicos de fisiología, sueño, HRV y wearables

| Dataset | URL | Licencia | Formato | Tamaño | Acceso | ¿Demo 48 h? |
|---|---|---|---|---|---|---|
| Sleep-EDF Expanded (PhysioNet) | https://physionet.org/content/sleep-edfx/1.0.0/ | ODC Attribution 1.0 [VERIFICADO] | EDF/EDF+ | 8,1 GB (197 registros) | Descarga libre: ZIP, wget, AWS S3 | Sí: etapas de sueño con EEG; pesado, usar un subconjunto |
| Motion and heart rate from a wrist-worn wearable (Sleep-Accel, PhysioNet) | https://physionet.org/content/sleep-accel/1.0.0/ | ODC Attribution 1.0 [VERIFICADO] | TXT por sujeto (aceleración, FC, pasos, etapas PSG) | 2,2 GB (550 MB comprimido), 31 sujetos | Descarga libre | Sí: es el más ligero y cercano a un smartwatch |
| WESAD (UCI) | https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection | [HUECO] la página UCI remite a la web de origen (Univ. Siegen) | Series multivariantes: Empatica E4 y RespiBAN (ECG, EDA, EMG, respiración, temperatura, acelerómetro) | [HUECO]; 63 M de instancias, 15 sujetos | Descarga libre vía paquete Python `ucimlrepo` o web de origen | Sí: estrés/afecto, ideal para un indicador de carga fisiológica |
| MIMIC-IV Waveform v0.1.0 (PhysioNet) | https://physionet.org/content/mimic4wdb/0.1.0/ | ODC Open Database 1.0 [VERIFICADO] | WFDB (FLAC) + CSV | 12,8 GB, 200 registros / 198 pacientes | Descarga libre | Parcial: señales de UCI (ECG, PPG, respiración, presión), útil para un demo de alarmas |
| MIMIC-III Waveform Matched Subset (PhysioNet) | https://physionet.org/content/mimic3wdb-matched/1.0/ | ODC Open Database 1.0 [VERIFICADO] | WFDB (.hea/.dat) | 2,4 TB, 10.282 pacientes | Descarga libre | No completo: demasiado grande; solo registros sueltos |
| DREAMT (PhysioNet) | https://physionet.org/content/dreamt/ | PhysioNet Restricted Health Data License 1.5.0 [VERIFICADO] | CSV (E4 + PSG) | [HUECO] | Restringido: exige firmar acuerdo de uso | No: la firma/aprobación no cabe en 48 h |
| eICU, MIMIC-III clínica | https://physionet.org/about/database/ | Credenciada [VERIFICADO] | - | - | Requiere credenciales PhysioNet | No |

Otras bases abiertas listadas por PhysioNet y no inspeccionadas en detalle (licencia y tamaño [HUECO]): MIT-BIH Arrhythmia (47 sujetos), Normal Sinus Rhythm RR Interval (54 registros), CAP Sleep, PTB-XL (21.801 ECG de 12 derivaciones), "A Multi-Night Instantaneous Heart Rate and Accelerometry Dataset". Fuente: https://physionet.org/about/database/

## 4. Lagunas generales

- No hay datos abiertos verificados de telemetría real de astronautas en misión. [SUPOSICION] El MVP debe usar datos análogos terrestres y simular el flujo de a bordo.
- No pude leer el texto del reto ni confirmar sus recursos. Revisar el 28 oct.
- No confirmé licencias de WESAD ni de varias bases menores de PhysioNet.
- Los catálogos dinámicos (nlsp.nasa.gov, osdr.nasa.gov) devolvieron solo cabeceras; la información de OSDR/NLSP viene de páginas informativas de nasa.gov, science.nasa.gov, ReadTheDocs y un artículo PMC.

## 5. Shortlist recomendada (3-4)

1. **Sleep-Accel (PhysioNet)**: ligero (2,2 GB; usable por sujetos), licencia abierta, FC + movimiento + etapas de sueño. Base para el panel de sueño y recuperación de la tripulación.
2. **WESAD**: estrés y afecto con wearable de muñeca y pecho; da una "carga fisiológica" demostrable. Comprobar licencia antes de redistribuir.
3. **OSDR Biological Data API**: sin clave, JSON/CSV, permite una capa de "contexto científico NASA" (estudios de vuelo y análogos) y da credibilidad al enlace con NASA. No sirve como señal en vivo.
4. **MIMIC-IV Waveform v0.1.0** (opcional): pocos registros de ECG/PPG con licencia abierta, para probar detección de anomalías y alarmas; 12,8 GB, usar 2-3 registros.

Descartados para 48 h: LSAH y datos controlados de OSDR (solicitud con IRB/comité), DREAMT (acuerdo de uso), MIMIC-III completo (2,4 TB), Mars-500 crudo (sin descarga pública verificada).

## 6. Exploración de Sleep-Accel (2026-10-22)

Muestra: 3 de 31 sujetos (1066528, 1360686, 1449548) en `data/sleep-accel/`, SHA256 verificado contra `SHA256SUMS.txt`. Script: solo librería estándar de Python (pandas no está instalado).

- [VERIFICADO] Descarga: `physionet.org/files/...` limita a ~6 KB/s; el espejo `https://physionet-open.s3.amazonaws.com/sleep-accel/1.0.0/` bajó 5 MB en 2,4 s. Usar S3.
- [VERIFICADO] Formatos: `heart_rate` = `t,bpm` (CSV); `labels` = `t etapa` cada 30 s (-1 sin puntuar, 0 vigilia, 1-3 N1-N3, 5 REM); `motion` = `t x y z` en g (espacios); `steps` = `t,pasos` (CSV). `t` en segundos relativo al inicio de la PSG; negativo = días previos.
- [VERIFICADO] Cada sujeto trae ~8 h de PSG etiquetada y de 4 a 7 días previos de FC y pasos, lo que sirve para construir una línea base personal antes de la noche evaluada (ángulo 1 de 07).
- [VERIFICADO] FC nocturna cada ~5 s; mediana nocturna 59, 70 y 68 lpm; ningún valor fuera de 30-200 lpm.
- [VERIFICADO] Huecos reales: el sujeto 1066528 tiene un hueco nocturno de FC de 5.224 s (~87 min) y 36 huecos de más de 60 s; 1449548 tiene uno de 851 s. Son casos naturales para demostrar la abstención por calidad de datos.
- [VERIFICADO] La aceleración (~25-28 Hz) cubre solo de ~6-7 h antes a ~8 h después del inicio de la PSG, salvo 1449548, que llega a -135 h con muestreo disperso (promedio ~4 Hz). Los pasos de 1066528 terminan 35 h antes de la PSG.
- Tamaño: ~200 MB para 3 sujetos, casi todo aceleración.

## 7. Verificación de datos humanos de NASA (2026-11-06)

Objetivo: cerrar los [HUECO] de las secciones 2.1 y 2.2 sobre si hay series fisiológicas humanas de NASA descargables sin trámite.

### 7.1 LSDA: colección de reposo en cama (UTMB)
- [VERIFICADO] El portal https://www.nasa.gov/hrp/nlsp lista tres misiones de análogo: UTMB Campaign 1, Campaign 3 y Campaign 11 (70 días de ejercicio y desempeño). Detalle de la Campaña 1: https://nlsp.nasa.gov/explore/data/details/6eaf1654-72d4-5d71-a9dd-a02e674c6473?dataType=MISSIONS
- [VERIFICADO] Campaña 1: 3 sujetos hombres, 84 días (10 ambulatorios, 60 de inclinación de cabeza a -6° y 14 de rehabilitación), 25 experimentos, entre ellos "Neuroendocrine and Cardiovascular Response to Tilt" (MR001G) y las "Standard Measures". La página solo tiene las secciones General, Descripción, Experimentos e Imágenes, sin enlaces de descarga.
- [VERIFICADO] Política de acceso (https://nlsp.nasa.gov/data-request-guidelines): solo los datos **agrupados** (medias y rangos) son públicos. Los datos individuales desidentificados exigen revisión de NASA, IRB, consentimiento y acuerdo de uso, con ~13 meses de plazo. Los atribuibles, ~25 meses.
- [SUPOSICION] Las Campañas 3 y 11 siguen la misma política, porque es global del portal. No se abrieron sus páginas de detalle.
- **Conclusión:** no sirve como entrada de la PoC. Queda como contexto citable.

### 7.2 OSDR y otras fuentes
- [VERIFICADO] La API https://visualization.osdr.nasa.gov/biodata/api/ responde sin autenticación. La consulta de *Homo sapiens* devolvió 116-117 accesiones (la cifra varió entre dos consultas). No apareció OSD-630 en ninguna.
- [VERIFICADO] OSD-569 (Inspiration4): sangre total con RNA-seq, WGS, hematopoyesis clonal y hemograma; no declara licencia. OSD-575: 9 archivos de paneles de suero, CMP y metadatos ISA en CSV/XLSX, sin FC ni sueño. Fuente: https://visualization.osdr.nasa.gov/biodata/api/v2/dataset/OSD-575/files/
- [HUECO] No se revisaron los archivos de los demás OSD humanos; no hay evidencia de series temporales.
- [VERIFICADO] Mendeley Data "Blood Pressures In Spaceflight" (CC BY 4.0, DOI 10.17632/pz6nt4cpxs.1): presión arterial agregada por misión, sexo, IMC, edad y contramedida; no es serie por persona. Fuente: https://data.mendeley.com/datasets/pz6nt4cpxs
- [HUECO] No se encontraron datos de astronautas ni de reposo en cama en PhysioNet, Zenodo ni figshare, ni datasets abiertos de ESA, JAXA o CSA con señales fisiológicas. AGBRESA (60 días, ECG y presión) no muestra depósito público [SUPOSICION: revisar su declaración de disponibilidad de datos].
- `data.nasa.gov/dataset/nasa-life-sciences-portal-nlsp` marca "License not specified" y solo apunta al portal. Fuente: https://data.nasa.gov/dataset/nasa-life-sciences-portal-nlsp

### 7.3 Conclusión para la PoC
- No hay serie temporal fisiológica humana de NASA descargable sin trámite. **Sleep-Accel sigue siendo la base de la PoC**, rotulada como dato análogo terrestre.
- Lo "NASA" de la demo es **contenido**: riesgos y contramedidas del HRP, NTRS, OSDR como contexto y el corpus de `data/papers`. Que eso cumpla el requisito de usar datos NASA sigue en [HUECO] hasta la guía 2026.

### 7.4 Hallazgos del corpus local (`data/papers`, índice en `fuentes-notebooklm.md`)
- #125 "Physiological Adaptation Dynamics in Partial Gravity Environments and Autonomous Assessment Protocols" describe una **prueba de pie autoadministrada** (5 min acostado, 5 min de pie, FC y presión continuas con wearables). [HUECO] Es un informe generado en NotebookLM, no una fuente primaria: hay que rastrear sus citas hasta el protocolo de NASA antes de usarlo.
- #41 tesis sobre maniobras de contrapresión para síncope: material didáctico sin fármacos. Solo se leyó su índice.
- #87 *Gravity Well* (NASA), #109/#110 tareas críticas vestibulares y sensoriomotoras: respaldan el escenario de llegada (D-007).
- #67 evitación de atención médica en pilotos militares: respalda D-006.
- #74/#75 respuestas cardiopulmonares en gravedad parcial: contexto para Luna y Marte.
