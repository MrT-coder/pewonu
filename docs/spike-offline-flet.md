# Spike A1: modo offline de Flet

Fecha: 2026-11-14. Tarea: A1 de [tareas.md](tareas.md). Cierra el [HUECO] "modo offline real" de D-017.

## Resultado

**Pasa.** Con `ft.run(..., no_cdn=True)` la app del astronauta abre y responde sin acceso a internet. La salida a TypeScript de D-017 no se activa por este motivo.

## Qué se probó

- Flet 1.1.2 (Flutter 3.47.9), servidor dinámico en la misma máquina, vista `WEB_BROWSER`, Chromium headless con Playwright.
- App mínima: dos zonas clicables, un texto de estado y un `Dropdown` de idioma (`on_select`).
- Sin internet = todo pedido a un host distinto de `127.0.0.1` se aborta y se registra (Playwright `page.route`). No se desconectó el adaptador de red. [SUPOSICION] equivale a estar sin red para este fin.

| Configuración | Pedidos externos | Resultado |
|---|---|---|
| `ft.run(main)` (por defecto) | `www.gstatic.com/flutter-canvaskit/.../skwasm.js` y `.wasm` | **No renderiza** sin internet |
| `ft.run(main, no_cdn=True)` | `cdn.jsdelivr.net/npm/@rive-app/flutter-native-wasm@44.0.0/wasm/rive_native.js` | Renderiza |

Con `no_cdn=True`, y sin red:

- [VERIFICADO] La pantalla se dibuja (texto, `Dropdown`, zonas).
- [VERIFICADO] El clic en una zona llega al servidor Python y actualiza el texto (`Clic en: brain`).
- [VERIFICADO] El cambio de idioma español/inglés actualiza todos los textos.

## Residual y límites

- Queda **un** pedido externo (runtime de Rive, a jsdelivr). La app funciona igual cuando falla. No usamos Rive: no agregar controles de animación Rive. [SUPOSICION] no afecta a ningún control que planeamos usar; confirmar si A3 incorpora animación.
- No se probó `flet build web --no-cdn` (compilación estática con Pyodide). No aplica a la arquitectura de D-017, que usa servidor dinámico local.
- [HUECO] Siguen sin verificar: figura con arte SVG y zonas encima (A3), micrófono (`AudioRecorder`, A6) y SQLite dentro de la app (A2).
- [HUECO] El enlace público de la demo sigue pendiente de la guía de envío (P1).

## Cómo repetirlo

1. `uv sync --group dev --extra astronaut`
2. Servidor: `ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550, no_cdn=True)`.
3. Abrir `http://127.0.0.1:8550` con un navegador que bloquee todo host externo y revisar los pedidos bloqueados.
