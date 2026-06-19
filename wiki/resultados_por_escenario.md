# Resultados por escenario

Esta pagina resume los resultados generados por el sistema para los cinco escenarios principales. Los datos provienen de los reportes CSV existentes en `resultados/reportes/` y se complementan con los graficos ubicados en `resultados/graficos/`.

## Resumen numerico

| Escenario | Temp. minima | Temp. maxima | Temp. promedio | Derivada min. | Derivada max. | Estados detectados |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Funcionamiento normal | 1.98 °C | 6.57 °C | 2.95 °C | -0.2010 °C/min | 0.0120 °C/min | Inicializando: 4, Estado normal: 16 |
| Puerta abierta | 2.69 °C | 8.32 °C | 5.12 °C | -0.1950 °C/min | 0.1170 °C/min | Estado normal: 7, Alerta critica: 13 |
| Falla del compresor | 4.21 °C | 7.23 °C | 5.73 °C | -0.1760 °C/min | 0.0750 °C/min | Inicializando: 4, Alerta critica: 16 |
| Recuperacion | 2.04 °C | 6.52 °C | 4.08 °C | -0.2270 °C/min | 0.1280 °C/min | Inicializando: 4, Estado normal: 9, Alerta critica: 7 |
| Camara apagada | 3.53 °C | 18.23 °C | 9.83 °C | -0.1810 °C/min | 0.2340 °C/min | Inicializando: 4, Estado normal: 1, Alerta critica: 15 |

## Interpretacion

### Funcionamiento normal

La temperatura desciende desde un valor inicial elevado hasta acercarse al rango seguro. La derivada centrada tiende a valores cercanos a cero, lo que indica estabilizacion progresiva.

Archivos asociados:

- `resultados/reportes/reporte_normal.csv`
- `resultados/graficos/temperatura_normal.png`
- `resultados/graficos/derivada_normal.png`

### Puerta abierta

Luego de una etapa inicial de enfriamiento, la temperatura comienza a aumentar. El sistema detecta alertas criticas cuando la temperatura supera el limite maximo recomendado.

Archivos asociados:

- `resultados/reportes/reporte_puerta_abierta.csv`
- `resultados/graficos/temperatura_puerta_abierta.png`
- `resultados/graficos/derivada_puerta_abierta.png`

### Falla del compresor

La camara no logra recuperar el rango seguro y la temperatura permanece por encima del limite permitido. Este escenario evidencia una condicion sostenida de riesgo.

Archivos asociados:

- `resultados/reportes/reporte_falla_compresor.csv`
- `resultados/graficos/temperatura_falla_compresor.png`
- `resultados/graficos/derivada_falla_compresor.png`

### Recuperacion

El escenario combina una etapa de falla con una posterior tendencia de retorno hacia el rango esperado. La derivada permite observar el cambio de tendencia entre calentamiento y enfriamiento.

Archivos asociados:

- `resultados/reportes/reporte_recuperacion.csv`
- `resultados/graficos/temperatura_recuperacion.png`
- `resultados/graficos/derivada_recuperacion.png`

### Camara apagada o corte de energia

La temperatura aumenta hasta valores muy superiores al rango recomendado. El sistema clasifica la mayor parte del comportamiento como alerta critica por temperatura elevada.

Archivos asociados:

- `resultados/reportes/reporte_camara_apagada.csv`
- `resultados/graficos/temperatura_camara_apagada.png`
- `resultados/graficos/derivada_camara_apagada.png`

## Lectura para defensa

La comparacion entre escenarios muestra que el Metodo de Diferencias Centradas aporta informacion adicional a la temperatura actual. Permite observar si la camara se esta estabilizando, calentando o recuperando, lo que fortalece la deteccion temprana de fallas.
