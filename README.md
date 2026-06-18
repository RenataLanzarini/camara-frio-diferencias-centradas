# Sistema de Monitoreo Inteligente de Cámaras de Frío mediante Diferencias Centradas

## Integrantes

* María Renata Lanzarini
* Franco Maldonado

## Materia

Análisis Numérico

## Carrera

Ingeniería en Informática

## Tema Asignado

Método de Diferencias Centradas

---

# Descripción General

Las cámaras de frío destinadas a la conservación de carne requieren un monitoreo permanente de la temperatura para garantizar la calidad e inocuidad de los productos almacenados. Variaciones fuera de los rangos recomendados pueden comprometer la conservación de los alimentos y generar pérdidas económicas.

El presente proyecto consiste en el desarrollo de un sistema inteligente de monitoreo para cámaras frigoríficas de conservación de carne refrigerada. El sistema analiza mediciones de temperatura obtenidas mediante sensores simulados y aplica el método de Diferencias Centradas para estimar la velocidad de variación de la temperatura a partir de datos discretos.

A partir de dicho análisis, la aplicación puede detectar comportamientos anormales, identificar tendencias de calentamiento o enfriamiento, generar alertas automáticas y enviar notificaciones por correo electrónico.

La temperatura objetivo de funcionamiento es aproximadamente de 2 °C, considerando como rango operativo recomendado valores comprendidos entre 0 °C y 4 °C.

---

# Problema a Resolver

En una cámara frigorífica no resulta suficiente conocer únicamente la temperatura actual.

También es necesario determinar:

* Si la temperatura está aumentando o disminuyendo.
* La velocidad con la que cambia la temperatura.
* Si existe una tendencia que pueda derivar en una falla.
* Si la cámara se encuentra estabilizada.
* Si es necesario emitir alertas preventivas.

Por ejemplo:

* Una temperatura dentro del rango permitido puede estar aumentando rápidamente.
* Una falla del sistema de refrigeración puede detectarse antes de alcanzar valores críticos.
* Una puerta mal cerrada puede provocar una tendencia sostenida de calentamiento.
* Un corte de energía puede detectarse mediante un aumento brusco de temperatura.

Para analizar estos comportamientos se utilizan técnicas de diferenciación numérica basadas en Diferencias Centradas.

---

# Objetivo General

Desarrollar una herramienta informática que permita monitorear y analizar la evolución de la temperatura de cámaras frigoríficas destinadas a la conservación de carne utilizando el método de Diferencias Centradas.

---

# Objetivos Específicos

* Implementar el cálculo de derivadas mediante Diferencias Centradas.
* Implementar el cálculo de derivadas mediante Diferencias Hacia Adelante para comparación.
* Simular mediciones de temperatura obtenidas por sensores.
* Analizar la evolución temporal de la temperatura.
* Determinar la velocidad de calentamiento o enfriamiento.
* Detectar situaciones fuera de los rangos establecidos.
* Generar alertas automáticas.
* Representar gráficamente los resultados obtenidos.
* Generar reportes automáticos.
* Enviar notificaciones por correo electrónico.
* Aplicar conceptos de Análisis Numérico a un problema de ingeniería.

---

# Alcance del Proyecto

La aplicación trabaja con datos generados mediante sensores simulados.

A partir de dichas mediciones se calculan derivadas numéricas utilizando el método de Diferencias Centradas para estudiar la evolución de la temperatura dentro de las cámaras.

El sistema está orientado al monitoreo, análisis y asistencia al usuario, sin realizar acciones automáticas de control sobre los equipos de refrigeración.

---

# Metodología Matemática

Para aproximar la derivada de la temperatura respecto del tiempo se utiliza el método de Diferencias Centradas.

La aproximación empleada es:

dT/dt ≈ (T(i+1) - T(i-1)) / (2h)

donde:

* T(i+1): temperatura posterior.
* T(i-1): temperatura anterior.
* h: intervalo de tiempo entre mediciones.

También se implementa el método de Diferencias Hacia Adelante:

dT/dt ≈ (T(i+1) - T(i)) / h

La utilización de Diferencias Centradas permite obtener una aproximación más precisa de la derivada, ya que utiliza información de ambos lados del punto analizado.

---

# Funcionalidades Implementadas

Actualmente el sistema permite:

* Simulación de lecturas de temperatura mediante sensores virtuales.
* Simulación de múltiples cámaras frigoríficas.
* Monitoreo individual de cámaras.
* Monitoreo automático.
* Aplicación del método de Diferencias Centradas.
* Aplicación del método de Diferencias Hacia Adelante.
* Generación automática de alertas.
* Clasificación de estados operativos.
* Visualización gráfica de temperatura versus tiempo.
* Visualización gráfica de derivadas numéricas.
* Gestión de destinatarios de correo electrónico.
* Envío automático de alertas.
* Generación de reportes.
* Selección de múltiples cámaras para reportes.
* Tablero general de monitoreo.
* Interfaz web desarrollada con Flask.

---

# Escenarios Simulados

El sistema contempla distintos escenarios de funcionamiento:

## Funcionamiento Normal

La temperatura converge gradualmente hacia la temperatura objetivo.

## Puerta Abierta

La temperatura aumenta debido al ingreso de aire exterior.

## Falla del Compresor

La capacidad de refrigeración disminuye y la temperatura aumenta progresivamente.

## Recuperación

Luego de una falla temporal la cámara vuelve gradualmente a la temperatura deseada.

## Cámara Apagada

Se produce un aumento importante de temperatura debido a la ausencia de refrigeración.

---

# Sistema de Alertas

El sistema clasifica automáticamente los eventos en los siguientes estados:

* Inicializando.
* Estado normal.
* Advertencia.
* Alerta crítica.
* Emergencia.

La clasificación se realiza considerando:

* Temperatura actual.
* Velocidad de variación calculada mediante Diferencias Centradas.
* Límites operativos establecidos.

Cuando se detectan condiciones anormales se genera automáticamente una notificación por correo electrónico.

---

# Rangos de Operación Considerados

Para este proyecto se consideran los siguientes límites:

* Temperatura mínima recomendada: 0 °C
* Temperatura máxima recomendada: 4 °C
* Temperatura objetivo: 2 °C

Posibles alertas:

* Temperatura superior a 4 °C.
* Temperatura inferior a 0 °C.
* Variación brusca de temperatura.
* Tendencia sostenida de calentamiento.
* Posible falla del sistema de refrigeración.
* Posible corte de energía.

---

# Tecnologías Utilizadas

* Python
* Flask
* Pandas
* Matplotlib
* HTML
* CSS
* Git
* GitHub

---

# Estructura del Proyecto

```text
camara-frio-diferencias-centradas

├── app.py
├── main.py
├── README.md
├── requirements.txt
│
├── datos/
│   └── destinatarios.txt
│
├── informe/
│   └── marco_teorico.md
│
├── resultados/
│   ├── graficos/
│   └── reportes/
│
├── src/
│   ├── alertas.py
│   ├── diferencias_centradas.py
│   ├── graficos.py
│   ├── lectura_datos.py
│   ├── notificaciones.py
│   └── sensor_simulado.py
│
└── static/
    ├── copos.jpg
    └── favicon.png
```

---

# Instalación

## Crear entorno virtual

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecución del Proyecto

Iniciar la aplicación:

```bash
python app.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

---

# Uso del Sistema

1. Agregar destinatarios de correo electrónico.
2. Seleccionar una cámara.
3. Elegir el modo de ejecución.
4. Ejecutar el monitoreo.
5. Analizar gráficos y resultados.
6. Consultar el tablero general de cámaras.
7. Generar reportes.
8. Recibir alertas por correo electrónico.

---

# Resultados Generados

El sistema genera automáticamente:

* Reportes CSV.
* Gráficos de temperatura.
* Gráficos de derivadas.
* Alertas automáticas por correo electrónico.

Los archivos generados se almacenan en:

```text
resultados/
```

---

# Estado Actual

Proyecto completamente funcional.

Actualmente se encuentran implementadas todas las funcionalidades principales de simulación, monitoreo, análisis numérico, generación de reportes y envío de alertas.

---

# Posibles Mejoras Futuras

* Lectura de datos desde sensores físicos.
* Integración con dispositivos IoT.
* Base de datos para almacenamiento histórico.
* Monitoreo remoto en tiempo real.
* Panel administrativo avanzado.
* Dashboard con actualización automática.
* Integración con aplicaciones móviles.
* Control automático de temperatura.

---

# Conclusión

El proyecto demuestra una aplicación práctica del método de Diferencias Centradas a un problema real de ingeniería.

La combinación de simulación de sensores, análisis numérico, generación de alertas, visualización gráfica y monitoreo web permite implementar una solución integral para el seguimiento de cámaras frigoríficas destinadas a la conservación de alimentos.

Además, el desarrollo evidencia cómo los conceptos estudiados en Análisis Numérico pueden utilizarse para resolver problemas reales de monitoreo industrial mediante herramientas modernas de software.
