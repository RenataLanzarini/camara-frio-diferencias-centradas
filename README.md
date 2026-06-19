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

|-- app.py
|-- main.py
|-- README.md
|-- requirements.txt
|
|-- datos/
|   |-- camaras.json
|   |-- destinatarios.txt
|
|-- informe/
|   |-- Lineamiento.md
|   |-- informe_final.md
|   |-- marco_teorico.md
|
|-- resultados/
|   |-- graficos/
|   |-- reportes/
|
|-- src/
|   |-- alertas.py
|   |-- diferencias_centradas.py
|   |-- graficos.py
|   |-- lectura_datos.py
|   |-- notificaciones.py
|   |-- sensor_simulado.py
|
|-- static/
|   |-- 87-879949_copo-de-nieve-png-copo-de-nieve-png.png
|   |-- copos.jpg
|
|-- tests/
|   |-- test_camaras.py
|   |-- test_diferencias.py
|   |-- test_sensor_simulado.py
|
|-- wiki/
|   |-- flujo_ejecucion_checklist.md
|   |-- flujo_modificaciones_web.md
|   |-- guion_defensa.md
|   |-- resultados_por_escenario.md
|   |-- validacion_metodo_numerico.md
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
python -m venv venv
venv\Scripts\activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Pruebas

El proyecto incluye pruebas básicas para validar el cálculo de Diferencias Centradas y Diferencias Hacia Adelante.

Ejecutar:

```bash
python -m unittest discover -s tests
```

Estas pruebas verifican una serie lineal con derivada conocida, los extremos no calculables del método centrado y el rechazo de mediciones con tiempos repetidos.

---

# Reproducibilidad de Simulaciones

Por defecto, las simulaciones incluyen variaciones aleatorias para representar ruido de sensores y condiciones variables.

Para una demostración o defensa, se puede fijar una semilla y obtener resultados repetibles:

```bash
set SIMULACION_SEMILLA=defensa
python app.py
```

En Linux:

```bash
export SIMULACION_SEMILLA=defensa
python app.py
```

Si `SIMULACION_SEMILLA` no está definida, el sistema funciona en modo aleatorio normal.

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

1. Agregar o eliminar cámaras desde la sección de administración.
2. Cargar cada destinatario una sola vez y seleccionar qué cámaras le corresponden.
3. Seleccionar una cámara.
4. Elegir el modo de ejecución.
5. Ejecutar el monitoreo.
6. Analizar gráficos y resultados.
7. Consultar el tablero general de cámaras.
8. Abrir el detalle de una cámara sin perder la tabla general.
9. Generar reportes y seleccionar desde un desplegable a qué mails cargados enviarlos.
10. Recibir alertas por correo electrónico según la cámara afectada.

---

# Configuración de Cámaras y Notificaciones

La aplicación permite administrar cámaras desde la interfaz web. Las cámaras se guardan de forma persistente en:

```text
datos/camaras.json
```

Cada cámara contiene:

* ID.
* Nombre.
* Producto.
* Ubicación.
* Lista de destinatarios.

Los correos se cargan una sola vez desde la interfaz. Para cada correo se seleccionan las cámaras que le corresponden mediante casillas de selección. Esto evita escribir varias veces el mismo mail y permite que una misma persona reciba alertas de una o varias cámaras.

Para enviar correos reales, el sistema utiliza las siguientes variables de entorno:

```text
EMAIL_REMITENTE
EMAIL_PASSWORD
```

`EMAIL_REMITENTE` corresponde a la cuenta desde la cual se enviarán las alertas y `EMAIL_PASSWORD` corresponde a la contraseña o clave de aplicación configurada para esa cuenta.

Estas credenciales pueden guardarse en un archivo local `.env` en la raíz del proyecto. Ese archivo está ignorado por Git para evitar subir datos sensibles al repositorio.

Si una cámara no tiene destinatarios asignados, o si faltan las credenciales de envío, el sistema no interrumpe la ejecución. En ese caso, muestra el resultado del monitoreo en pantalla y deja constancia de que no se pudo enviar el correo.

Las notificaciones se intentan enviar cuando el monitoreo detecta advertencias, alertas críticas o emergencias. El envío se realiza a los destinatarios asociados a la cámara que generó el evento. En funcionamiento normal, el sistema muestra el estado en pantalla y no envía alertas innecesarias.

Para reportes, la sección correspondiente permite desplegar los mails ya cargados y seleccionar manualmente cuáles recibirán el reporte generado.

La interfaz está adaptada para PC y dispositivos móviles. En pantallas pequeñas, las tablas se desplazan horizontalmente y los formularios se acomodan en una sola columna.

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
