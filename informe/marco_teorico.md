# MARCO TEÓRICO

# Sistema de Monitoreo Inteligente de Cámaras de Frío mediante el Método de Diferencias Centradas

## 1. Introducción

La conservación adecuada de alimentos constituye un aspecto fundamental dentro de la industria alimentaria. Los productos perecederos, especialmente las carnes refrigeradas, requieren mantenerse dentro de rangos específicos de temperatura para garantizar su calidad, inocuidad y vida útil.

Las cámaras frigoríficas son equipos diseñados para mantener temperaturas controladas durante el almacenamiento. Sin embargo, diversas situaciones pueden provocar variaciones térmicas no deseadas, tales como aperturas prolongadas de puertas, fallas mecánicas, cortes de energía eléctrica o problemas en el sistema de refrigeración.

La detección temprana de estas situaciones permite actuar antes de que los productos sufran deterioros importantes. Por este motivo resulta necesario implementar sistemas de monitoreo capaces de analizar continuamente la evolución de la temperatura y generar alertas automáticas cuando se detecten comportamientos anormales.

En este proyecto se desarrolla una aplicación que simula el funcionamiento de cámaras frigoríficas y utiliza métodos numéricos para analizar el comportamiento térmico mediante el cálculo de derivadas aproximadas.

---

# 2. Conservación de alimentos mediante refrigeración

La refrigeración es uno de los métodos más utilizados para preservar alimentos. Su objetivo principal es disminuir la velocidad de crecimiento de microorganismos y reducir las reacciones químicas que provocan el deterioro de los productos.

En el caso de la carne refrigerada, organismos internacionales y normativas sanitarias recomiendan mantener temperaturas comprendidas entre 0 °C y 4 °C.

Cuando la temperatura supera estos valores durante períodos prolongados pueden producirse:

* Desarrollo acelerado de microorganismos.
* Pérdida de calidad del producto.
* Reducción de la vida útil.
* Riesgos para la salud del consumidor.

Por esta razón resulta fundamental monitorear permanentemente las condiciones de almacenamiento.

---

# 3. Derivada y velocidad de cambio

La derivada es uno de los conceptos fundamentales del cálculo diferencial y permite medir la velocidad de cambio de una variable respecto de otra.

Si la temperatura de una cámara se representa mediante una función T(t), la derivada:

[
\frac{dT}{dt}
]

indica qué tan rápido está aumentando o disminuyendo la temperatura con el transcurso del tiempo.

Interpretación física:

* Si la derivada es positiva, la temperatura aumenta.
* Si la derivada es negativa, la temperatura disminuye.
* Si la derivada es cercana a cero, la temperatura permanece estable.

La velocidad de cambio constituye un indicador muy útil para detectar anomalías antes de que la temperatura alcance niveles peligrosos.

---

# 4. Diferenciación numérica

En problemas reales generalmente no se conoce la expresión matemática exacta de la función analizada.

En cambio, se dispone de mediciones tomadas en instantes discretos de tiempo mediante sensores.

Por esta razón se utilizan métodos de diferenciación numérica, los cuales permiten aproximar derivadas a partir de datos experimentales.

Estos métodos son ampliamente utilizados en:

* Ingeniería.
* Automatización industrial.
* Control de procesos.
* Sistemas de monitoreo.
* Instrumentación electrónica.

---

# 5. Método de Diferencias Hacia Adelante

Una de las aproximaciones más simples para estimar la derivada es el método de diferencias hacia adelante:

[
\frac{dT}{dt}\approx\frac{T_{i+1}-T_i}{h}
]

donde:

* (T_i) es la temperatura actual.
* (T_{i+1}) es la temperatura siguiente.
* (h) es el intervalo temporal entre mediciones.

Este método utiliza únicamente información futura respecto del punto analizado.

Su principal ventaja es la simplicidad computacional, aunque presenta menor precisión que otros métodos.

---

# 6. Método de Diferencias Centradas

El método de Diferencias Centradas constituye una mejora respecto de las diferencias hacia adelante y hacia atrás.

La fórmula utilizada es:

[
\frac{dT}{dt}\approx\frac{T_{i+1}-T_{i-1}}{2h}
]

Este método utiliza simultáneamente la información anterior y posterior al punto de interés.

Ventajas:

* Mayor precisión.
* Menor error de truncamiento.
* Mejor representación de la tendencia real de los datos.

Debido a estas características fue seleccionado como método principal para el desarrollo del sistema.

---

# 7. Aplicación del método al monitoreo térmico

El cálculo de la derivada permite conocer no solamente la temperatura actual de una cámara sino también la tendencia de su comportamiento.

Por ejemplo:

* Una temperatura dentro del rango permitido puede ocultar una falla si está aumentando rápidamente.
* Una temperatura elevada puede no representar un problema grave si se encuentra disminuyendo y acercándose al valor objetivo.

El análisis conjunto de temperatura y derivada permite obtener una interpretación mucho más completa del estado del sistema.

---

# 8. Escenarios simulados

Con el objetivo de evaluar el comportamiento del sistema se desarrollaron diversos escenarios de simulación.

## Funcionamiento normal

La temperatura desciende progresivamente hasta alcanzar la temperatura objetivo cercana a 2 °C.

## Puerta abierta

La apertura prolongada permite el ingreso de aire exterior provocando un aumento gradual de temperatura.

## Falla del compresor

La capacidad de enfriamiento disminuye considerablemente y la temperatura comienza a elevarse de manera sostenida.

## Recuperación

Representa la situación en la que una falla es corregida y la cámara retorna gradualmente a las condiciones normales de funcionamiento.

## Cámara apagada o corte de energía

La refrigeración desaparece completamente y la temperatura aumenta rápidamente, generando una condición de riesgo.

---

# 9. Sistema de alertas automáticas

El sistema desarrollado clasifica el comportamiento de la cámara en distintos niveles:

* Inicializando.
* Estado normal.
* Advertencia.
* Alerta crítica.
* Emergencia.

La clasificación se realiza considerando:

* Temperatura medida.
* Velocidad de cambio calculada mediante diferencias centradas.
* Rango seguro de conservación.

Cuando se detectan condiciones anormales se genera automáticamente una notificación por correo electrónico para informar al responsable del sistema.

---

# 10. Tecnologías utilizadas

Para el desarrollo del proyecto se emplearon las siguientes herramientas:

* Python.
* Flask.
* Pandas.
* Matplotlib.
* HTML.
* CSS.

Estas tecnologías permitieron construir una aplicación web capaz de simular sensores, procesar datos, generar gráficos y emitir alertas automáticas.

---

# 11. Relación entre el proyecto y Análisis Numérico

El núcleo matemático del proyecto está basado en la aplicación práctica del método de Diferencias Centradas.

La utilización de este método permite transformar mediciones discretas de temperatura en información útil sobre la velocidad de cambio del sistema.

De esta manera se demuestra cómo los conceptos estudiados en Análisis Numérico pueden emplearse para resolver problemas reales de monitoreo industrial y control de procesos.

---

# 12. Conclusiones

El desarrollo realizado demuestra la utilidad de los métodos numéricos en aplicaciones de ingeniería y automatización.

La utilización de Diferencias Centradas permitió estimar con precisión la velocidad de cambio de la temperatura, facilitando la detección temprana de anomalías en cámaras frigoríficas.

La combinación de simulación de sensores, análisis numérico, visualización gráfica y notificaciones automáticas permitió construir una solución integral que vincula los contenidos teóricos de la asignatura con una problemática real de interés industrial.



