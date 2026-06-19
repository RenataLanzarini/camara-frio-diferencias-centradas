# Informe final del proyecto

# Sistema de Monitoreo Inteligente de Camaras de Frio mediante Diferencias Centradas

## 1. Datos generales

Materia: Analisis Numerico

Tema asignado: Metodo de Diferencias Centradas

Carrera: Ingenieria en Informatica

Integrantes:

- Maria Renata Lanzarini
- Franco Maldonado

## 2. Problema abordado

Las camaras frigorificas utilizadas para conservar alimentos perecederos deben mantener la temperatura dentro de rangos seguros. En el caso de carnes refrigeradas, el rango operativo considerado en este proyecto es de 0 °C a 4 °C, con una temperatura objetivo aproximada de 2 °C.

Controlar solamente la temperatura actual no siempre es suficiente. Una camara puede encontrarse dentro del rango permitido y, al mismo tiempo, presentar una tendencia de calentamiento que anticipe una falla. Por esta razon, el proyecto analiza tambien la velocidad de cambio de la temperatura mediante diferenciacion numerica.

## 3. Objetivo general

Desarrollar una herramienta informatica capaz de simular, monitorear y analizar la evolucion de la temperatura de camaras frigorificas aplicando el Metodo de Diferencias Centradas.

## 4. Objetivos especificos

- Simular mediciones discretas de temperatura.
- Calcular la derivada de la temperatura respecto del tiempo.
- Aplicar Diferencias Centradas como metodo numerico principal.
- Comparar el resultado con Diferencias Hacia Adelante.
- Clasificar estados de funcionamiento de la camara.
- Generar alertas, graficos y reportes.
- Relacionar los resultados obtenidos con el marco teorico de Analisis Numerico.

## 5. Fundamentacion matematica

En problemas reales no siempre se conoce una funcion continua `T(t)` que describa la temperatura. En cambio, se dispone de mediciones discretas tomadas en distintos instantes. Para estimar la velocidad de cambio se utiliza diferenciacion numerica.

El metodo principal aplicado es Diferencias Centradas:

```text
dT/dt ~= (T(i+1) - T(i-1)) / (t(i+1) - t(i-1))
```

Cuando las mediciones se toman con paso constante `h`, la expresion se escribe como:

```text
dT/dt ~= (T(i+1) - T(i-1)) / (2h)
```

Este metodo usa informacion anterior y posterior al punto evaluado, por lo que representa mejor la tendencia local que una diferencia hacia adelante simple.

Como metodo comparativo se implementa:

```text
dT/dt ~= (T(i+1) - T(i)) / (t(i+1) - t(i))
```

La derivada calculada permite interpretar el comportamiento termico:

- Valor positivo: la temperatura esta aumentando.
- Valor negativo: la temperatura esta disminuyendo.
- Valor cercano a cero: la temperatura se mantiene estable.

## 6. Implementacion

El proyecto fue desarrollado en Python con una interfaz web en Flask. La estructura principal separa responsabilidades:

- `src/sensor_simulado.py`: genera mediciones de temperatura para distintos escenarios.
- `src/diferencias_centradas.py`: calcula derivadas numericas.
- `src/alertas.py`: clasifica el estado de la camara.
- `src/graficos.py`: genera graficos de temperatura y derivadas.
- `src/notificaciones.py`: gestiona el envio de correos.
- `app.py`: integra la interfaz web, monitoreo, reportes y destinatarios.
- `main.py`: permite ejecutar el flujo desde consola.

La aplicacion permite seleccionar camaras, ejecutar monitoreos, visualizar tablas y graficos, generar reportes y enviar alertas cuando se detectan eventos relevantes.

## 7. Escenarios simulados

El sistema contempla cinco escenarios principales:

- Funcionamiento normal: la temperatura converge hacia el valor objetivo.
- Puerta abierta: la temperatura aumenta por ingreso de aire exterior.
- Falla del compresor: la refrigeracion pierde eficiencia y la temperatura sube progresivamente.
- Recuperacion: la camara vuelve gradualmente al rango esperado despues de una falla.
- Camara apagada o corte de energia: la temperatura aumenta rapidamente.

## 8. Resultados obtenidos

Los resultados se generan automaticamente en la carpeta `resultados/`.

La aplicacion produce:

- Reportes CSV en `resultados/reportes/`.
- Graficos de temperatura en `resultados/graficos/`.
- Graficos de derivadas numericas en `resultados/graficos/`.
- Mensajes de alerta para advertencias, alertas criticas y emergencias.

En los escenarios normales, la derivada tiende a acercarse a cero a medida que la temperatura se estabiliza. En escenarios anormales, como puerta abierta, falla del compresor o camara apagada, la derivada positiva permite detectar una tendencia de calentamiento antes de que la situacion sea mas grave.

## 9. Validacion

Se incorporaron pruebas unitarias para validar el comportamiento numerico del sistema. Las pruebas verifican:

- Una serie lineal con derivada conocida.
- El tratamiento del primer y ultimo punto en Diferencias Centradas.
- La deteccion de tiempos repetidos, que producirian division por cero.

Las pruebas se ejecutan con:

```bash
python -m unittest discover -s tests
```

## 10. Relacion con Analisis Numerico

El nucleo del proyecto es la aplicacion practica del Metodo de Diferencias Centradas. El sistema transforma datos discretos de temperatura en informacion sobre la velocidad de cambio, permitiendo tomar decisiones a partir de la tendencia del sistema.

De esta manera, el proyecto vincula un contenido teorico de Analisis Numerico con un problema real de monitoreo industrial.

## 11. Conclusiones

El proyecto cumple con el objetivo de construir una herramienta informatica relacionada con la carrera y basada en el tema asignado por la catedra. La aplicacion permite simular mediciones, calcular derivadas mediante Diferencias Centradas, detectar comportamientos anormales y generar informacion util para el monitoreo de camaras frigorificas.

La principal ventaja del enfoque utilizado es que no se limita a observar la temperatura actual, sino que analiza su evolucion. Esto permite anticipar fallas y justificar el uso de metodos numericos como herramienta aplicada a problemas de ingenieria.
