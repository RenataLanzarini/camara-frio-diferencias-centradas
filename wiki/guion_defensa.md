# Defensa completa del proyecto

# Sistema de Monitoreo Inteligente de Camaras de Frio mediante Diferencias Centradas

## 1. Presentacion inicial

Buenos dias. Nuestro proyecto se titula **Sistema de Monitoreo Inteligente de Camaras de Frio mediante el Metodo de Diferencias Centradas**.

El trabajo fue desarrollado para la materia **Analisis Numerico** y tiene como objetivo aplicar el tema asignado por la catedra, el **Metodo de Diferencias Centradas**, a un problema concreto vinculado con la ingenieria y el monitoreo de sistemas.

La idea central del proyecto es construir una herramienta informatica capaz de simular mediciones de temperatura en camaras frigorificas, analizar la evolucion de esas temperaturas y detectar posibles situaciones de riesgo a partir de la velocidad de cambio calculada mediante diferenciacion numerica.

## 2. Problema que se busca resolver

Las camaras de frio se utilizan para conservar alimentos perecederos, como carnes, pollos o embutidos. En este tipo de almacenamiento, la temperatura debe mantenerse dentro de un rango seguro para evitar deterioro del producto, perdida de calidad y riesgos sanitarios.

Para este proyecto se toma como referencia el rango de **0 °C a 4 °C**, con una temperatura objetivo cercana a **2 °C**.

El problema es que observar solamente la temperatura actual no siempre alcanza para tomar una buena decision. Por ejemplo:

- Una camara puede estar todavia dentro del rango seguro, pero calentandose rapidamente.
- Una temperatura elevada puede ser menos grave si la camara ya esta recuperandose y enfriando.
- Una falla de compresor, una puerta abierta o un corte de energia pueden detectarse antes si se analiza la tendencia.

Por eso, ademas de medir temperatura, el sistema calcula la **velocidad de cambio de la temperatura**. Esa velocidad se obtiene mediante el Metodo de Diferencias Centradas.

## 3. Relacion con Analisis Numerico

El proyecto se relaciona directamente con Analisis Numerico porque trabaja con datos discretos, no con una funcion matematica exacta.

En un caso ideal, podriamos tener una funcion continua:

```text
T(t)
```

donde `T` representa la temperatura y `t` representa el tiempo.

Si conocieramos esa funcion, podriamos derivarla analiticamente para saber como cambia la temperatura:

```text
dT/dt
```

Pero en una aplicacion real normalmente no se conoce la expresion exacta de `T(t)`. Lo que se tiene son mediciones tomadas por sensores en distintos instantes:

```text
t0, t1, t2, t3, ...
T0, T1, T2, T3, ...
```

Por ese motivo se usa **diferenciacion numerica**, que permite aproximar derivadas a partir de valores discretos.

## 4. Base teorica: derivada como velocidad de cambio

La derivada mide cuanto cambia una variable respecto de otra.

En este proyecto, la derivada de la temperatura respecto del tiempo indica la velocidad con la que la camara se calienta o se enfria.

La interpretacion fisica es:

- Si la derivada es positiva, la temperatura esta aumentando.
- Si la derivada es negativa, la temperatura esta disminuyendo.
- Si la derivada es cercana a cero, la temperatura se encuentra estable.

Esto permite complementar el analisis de temperatura actual con informacion de tendencia.

## 5. Metodo de Diferencias Centradas

El metodo numerico principal del proyecto es el **Metodo de Diferencias Centradas**.

La formula teorica para paso constante es:

```text
dT/dt ~= (T(i+1) - T(i-1)) / (2h)
```

donde:

- `T(i+1)` es la temperatura posterior al punto analizado.
- `T(i-1)` es la temperatura anterior al punto analizado.
- `h` es el intervalo de tiempo entre mediciones.

En el codigo se implementa una version equivalente que admite tiempos no necesariamente uniformes:

```text
dT/dt ~= (T(i+1) - T(i-1)) / (t(i+1) - t(i-1))
```

Esta forma es mas general porque calcula el intervalo real entre la medicion anterior y la posterior.

## 6. Justificacion del metodo elegido

Se eligio Diferencias Centradas porque ofrece una mejor aproximacion local que una diferencia hacia adelante o hacia atras.

La diferencia hacia adelante calcula:

```text
dT/dt ~= (T(i+1) - T(i)) / h
```

Ese metodo usa el punto actual y el siguiente.

En cambio, Diferencias Centradas usa informacion de ambos lados del punto:

```text
anterior -> punto analizado -> posterior
```

Esto permite representar mejor la tendencia alrededor del punto analizado y reduce el error de truncamiento en comparacion con aproximaciones de primer orden.

En el proyecto tambien se calcula Diferencias Hacia Adelante, pero como comparacion. El metodo central utilizado para interpretar el estado del sistema es Diferencias Centradas.

## 7. Tratamiento de los extremos

Una caracteristica importante del metodo es que no puede calcularse en el primer ni en el ultimo punto de la serie.

Esto ocurre porque:

- En el primer punto no existe una medicion anterior `T(i-1)`.
- En el ultimo punto no existe una medicion posterior `T(i+1)`.

Por eso, el sistema marca esos valores como **no calculables**. Esta decision es correcta desde el punto de vista numerico, porque evita inventar datos que no existen.

## 8. Descripcion general del sistema

El sistema desarrollado permite monitorear camaras frigorificas simuladas desde una interfaz web.

El flujo general es:

1. El usuario selecciona una camara.
2. El usuario elige un modo de ejecucion.
3. El sistema genera mediciones simuladas de temperatura.
4. Se calcula la derivada mediante Diferencias Centradas.
5. Se calcula tambien Diferencias Hacia Adelante para comparacion.
6. Se clasifica el estado de la camara.
7. Se generan graficos, tablas y reportes.
8. Si corresponde, se intenta enviar una alerta por correo.

## 9. Escenarios simulados

Para evaluar el sistema se definieron distintos escenarios:

### Funcionamiento normal

La temperatura comienza por encima del objetivo y desciende gradualmente hasta acercarse al rango seguro.

En este caso, la derivada tiende a acercarse a cero, lo que indica estabilizacion.

### Puerta abierta

Luego de una etapa inicial, la temperatura empieza a aumentar por ingreso de aire exterior.

La derivada positiva permite identificar la tendencia de calentamiento.

### Falla del compresor

La camara pierde capacidad de enfriamiento. La temperatura se mantiene elevada o aumenta de forma progresiva.

Este caso representa una situacion sostenida de riesgo.

### Recuperacion

La camara atraviesa una etapa anormal y luego vuelve gradualmente hacia el rango esperado.

Este escenario permite ver cambios de signo en la derivada: primero calentamiento y luego enfriamiento.

### Camara apagada o corte de energia

La temperatura aumenta rapidamente porque desaparece la refrigeracion.

Este escenario permite observar una condicion critica donde las alertas son necesarias.

## 10. Sistema de alertas

El sistema clasifica el comportamiento de la camara en distintos estados:

- Inicializando.
- Estado normal.
- Advertencia.
- Alerta critica.
- Emergencia.

La clasificacion considera:

- Temperatura actual.
- Rango seguro de operacion.
- Derivada calculada por Diferencias Centradas.
- Tendencia de calentamiento o enfriamiento.

De esta forma, el sistema no depende solo de un valor aislado de temperatura, sino que interpreta el comportamiento temporal.

## 11. Implementacion del proyecto

El proyecto fue desarrollado en Python y organizado en modulos.

Los archivos principales son:

- `app.py`: contiene la aplicacion web en Flask.
- `main.py`: permite ejecutar el flujo desde consola.
- `src/sensor_simulado.py`: genera datos de temperatura.
- `src/diferencias_centradas.py`: implementa el calculo numerico.
- `src/alertas.py`: clasifica los estados de la camara.
- `src/graficos.py`: genera graficos de temperatura y derivada.
- `src/notificaciones.py`: gestiona el envio de alertas por correo.

Esta separacion permite que cada parte tenga una responsabilidad clara.

## 12. Visualizacion web

La aplicacion web permite interactuar con el sistema de manera simple.

Desde la interfaz se puede:

- Agregar destinatarios de correo.
- Seleccionar camaras.
- Ejecutar monitoreos.
- Ver un tablero general.
- Consultar tablas de datos procesados.
- Visualizar graficos de temperatura.
- Visualizar graficos de derivadas.
- Generar reportes.

La interfaz ayuda a demostrar el proyecto durante la defensa porque permite mostrar el flujo completo sin ejecutar comandos manuales.

## 13. Persistencia de destinatarios

Los destinatarios de correo se almacenan en:

```text
datos/destinatarios.txt
```

Esto significa que los correos cargados no dependen solamente de memoria temporal. Si la aplicacion se cierra y se vuelve a abrir, los destinatarios siguen disponibles.

Ademas, el sistema esta preparado para no interrumpir la ejecucion si faltan credenciales de correo. En ese caso informa que no pudo enviar el email, pero sigue mostrando los resultados en pantalla.

## 14. Reproducibilidad de simulaciones

El sistema simula datos con cierta aleatoriedad para representar ruido de sensores y variaciones reales.

Para una defensa, tambien se agrego la posibilidad de fijar una semilla con:

```text
SIMULACION_SEMILLA
```

Esto permite repetir una misma simulacion y obtener los mismos resultados, lo cual es util para demostrar el proyecto de forma controlada.

## 15. Validacion y pruebas

Se agregaron pruebas unitarias para validar el calculo numerico.

Las pruebas verifican:

- Que una serie lineal produzca una derivada constante.
- Que el primer y ultimo punto no tengan derivada centrada.
- Que los tiempos repetidos generen error para evitar division por cero.
- Que una misma semilla produzca la misma simulacion.

Esto refuerza que el nucleo numerico del proyecto funciona correctamente.

## 16. Resultados obtenidos

El sistema genera resultados en:

```text
resultados/
```

Los resultados incluyen:

- Reportes CSV.
- Graficos de temperatura.
- Graficos de derivadas.
- Clasificacion de estados.

En funcionamiento normal se observa una tendencia hacia la estabilizacion. En escenarios como puerta abierta, falla del compresor o camara apagada, se observa que la temperatura sale del rango seguro y que la derivada permite detectar la tendencia de calentamiento.

## 17. Justificacion de decisiones de diseno

Se uso Python porque es claro para calculo numerico, procesamiento de datos y generacion de graficos.

Se uso Flask porque permite crear una aplicacion web sencilla y suficiente para demostrar el sistema.

Se uso Pandas para manipular datos tabulares de temperatura y tiempo.

Se uso Matplotlib para generar graficos de temperatura y derivadas.

Se separo el proyecto en modulos para facilitar la comprension durante la defensa y para que cada parte del sistema sea explicable.

## 18. Relacion entre teoria y aplicacion

La teoria indica que Diferencias Centradas permite aproximar la derivada usando valores discretos alrededor del punto de interes.

La aplicacion usa esa idea para transformar mediciones de temperatura en informacion sobre velocidad de cambio.

Esa velocidad de cambio permite responder preguntas practicas:

- La camara se esta calentando?
- La camara se esta enfriando?
- La temperatura esta estable?
- Hay una tendencia peligrosa aunque el valor actual parezca aceptable?

Por eso, el proyecto muestra una aplicacion directa de Analisis Numerico a un problema real.

## 19. Posibles preguntas durante la defensa

### Por que no se usa solo la temperatura actual?

Porque la temperatura actual no muestra la tendencia. Una camara puede estar dentro del rango seguro pero calentandose rapidamente. La derivada permite detectar esa evolucion.

### Por que se eligio Diferencias Centradas?

Porque utiliza informacion anterior y posterior al punto analizado, lo que mejora la aproximacion de la derivada local frente a metodos mas simples como Diferencias Hacia Adelante.

### Por que no se calcula la derivada centrada en los extremos?

Porque el metodo necesita un punto anterior y uno posterior. En el primer punto falta el anterior y en el ultimo falta el posterior.

### Que representa una derivada positiva?

Representa que la temperatura esta aumentando. En una camara frigorifica puede indicar calentamiento o posible falla.

### Que representa una derivada negativa?

Representa que la temperatura esta disminuyendo. Puede indicar enfriamiento o recuperacion.

### Que pasa si no se configuran los correos?

El sistema no se detiene. Muestra el resultado en pantalla y avisa que no pudo enviar el email.

### Que aporta la interfaz web?

Permite ejecutar el monitoreo, visualizar resultados y demostrar el proyecto de forma clara durante la presentacion.

## 20. Cierre de la defensa

Como conclusion, el proyecto cumple con el objetivo de aplicar un metodo numerico a un problema concreto de ingenieria.

El Metodo de Diferencias Centradas se utiliza como nucleo matematico para calcular la velocidad de cambio de la temperatura a partir de mediciones discretas.

La combinacion de simulacion, calculo numerico, alertas, graficos, reportes y visualizacion web permite construir una herramienta completa de monitoreo.

El aporte principal del proyecto es que no se limita a observar si la temperatura esta dentro o fuera de rango, sino que analiza la tendencia del sistema. Esa informacion permite detectar comportamientos anormales con mayor anticipacion y justificar tecnicamente el uso del metodo asignado.
