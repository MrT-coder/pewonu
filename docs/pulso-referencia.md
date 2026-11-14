# Referencia poblacional del pulso en reposo

Tarea C2 de [tareas.md](tareas.md). Aplica D-014 de [decisiones.md](decisiones.md). Código y datos: `src/crew_self_check/core/pulse_reference.py`.

## Fuente

- [VERIFICADO 2026-11-14] Ostchega Y, Porter KS, Hughes J, Dillon CF, Nwankwo T. *Resting pulse rate reference data for children, adolescents, and adults: United States, 1999-2008.* National Health Statistics Reports nº 41, NCHS, 2011. https://www.cdc.gov/nchs/data/nhsr/nhsr041.pdf
- [VERIFICADO] Se abrió el PDF y se copiaron los valores de las filas adultas de la Tabla 2 (hombres) y la Tabla 3 (mujeres, páginas 13 y 14), contrastando el texto extraído con la imagen de cada página. Los tests fijan cada fila.
- [VERIFICADO] Los datos excluyen a personas con una condición médica o un medicamento que afecte el pulso en reposo (nota al pie de las tablas).

## Qué cubre

Seis filas: hombres y mujeres de 20-39, 40-59 y 60-79 años, con n, media y los percentiles 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5 y 99.

No cubre, a propósito: menores de 20 (no son la tripulación) y 80 años o más (el PDF deja celdas sin calcular, marcadas con †). Para esas edades `reference_row` devuelve `None` y el estado no puede salir de la tabla: sigue `insufficient_data`.

## Criterio de color (propuesta, D-014 pide definirlo)

El pulso en reposo de la persona se compara con la fila de su edad y sexo:

| Estado | Condición |
|---|---|
| `ok` (verde) | del percentil 5 al 95, ambos incluidos |
| `watch` (ámbar) | del percentil 1 hasta debajo del 5, o por encima del 95 hasta el 99 |
| `act` (rojo) | por debajo del percentil 1 o por encima del 99 |

Ejemplo, hombre de 30 años (percentiles 1, 5, 95, 99 = 47, 52, 89, 101 lpm): 51 lpm es ámbar, 70 es verde, 95 es ámbar, 102 es rojo.

Qué significa: "inusual frente a adultos sanos de la misma edad y sexo". No es un umbral clínico ni un diagnóstico. Los cortes son estadísticos y es una decisión del equipo; si se quiere otro (por ejemplo, no usar rojo con solo la tabla), se cambia aquí y en la función `population_status`.

## Límites

- [SUPOSICION] La población general de EE. UU. de 1999-2008, medida sentada y en reposo, es una referencia razonable mientras no hay línea base personal. No son datos de astronautas ni de microgravedad (D-013).
- La app debe rotular siempre este estado como `reference: population` (contrato, sección 2). Cuando la línea base personal madura, esa pasa a mandar (D-014).
- Los mismos valores valen en los tres espacios; la tabla de ajustes por entorno empieza vacía (D-014).
