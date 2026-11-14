# Registro de uso de IA

**Requisito oficial 2026:** cada envío debe describir cómo se usaron las herramientas de IA (que en 2026 la organización llama "Super Intelligence") durante el desarrollo. Fuente: https://www.spaceappschallenge.org/resources/participant-faqs/ (ver [research/08](../research/08-enunciado-oficial.md)).

Cada persona agrega una fila cuando la IA aporta algo que llega al repositorio o al pitch. Antes del envío, la persona de producto resume esta tabla en inglés para la página del proyecto.

| Fecha | Persona | Herramienta | Para qué | Qué revisó o cambió el humano |
|---|---|---|---|---|
| 2026-10-28 | Josue Morales | Claude Code | Lectura del enunciado oficial, reanálisis de ideas y estructura del repositorio | Pendiente de revisión del equipo |
| 2026-10-28 | Josue Morales | Claude Code (4 subagentes de investigación) | Búsqueda de literatura sobre humanos en el espacio ([research/09](../research/09-humanos-en-el-espacio.md)) | Pendiente: contrastar las fuentes con artículos descargados (NotebookLM) |
| 2026-10-28 | Josue Morales | NotebookLM (Gemini Notebook) | Recopilación de 189 fuentes e informes de Deep Research sobre salud de astronautas | Pendiente: los 8 informes generados se tratan como [SUPOSICION] hasta verificarlos contra papers |
| 2026-10-30 | Josue Morales | Claude Code (Playwright, skill pdf-to-markdown) | Extracción del inventario de fuentes del cuaderno de NotebookLM, descarga de PDF de acceso abierto y conversión a Markdown ([research/fuentes-notebooklm.md](../research/fuentes-notebooklm.md)) | El humano inició sesión en Google manualmente y eligió la estrategia del corpus. Pendiente: revisar el índice; 17 fuentes de NCBI estaban guardadas en NotebookLM como captcha |
| 2026-11-14 | Josue Morales | Claude Code (Playwright) | Spike A1: app mínima de Flet y prueba del modo offline bloqueando hosts externos ([spike-offline-flet.md](spike-offline-flet.md)) | Pendiente: repetir la prueba con la red realmente desconectada |
