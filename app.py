import os
from flask import Flask, request, redirect, render_template_string, send_from_directory

from src.sensor_simulado import generar_lecturas_sensor, seleccionar_escenario_automatico
from src.diferencias_centradas import (
    calcular_diferencias_centradas,
    calcular_diferencias_adelante,
)
from src.alertas import generar_alertas
from src.notificaciones import enviar_email_alerta
from src.graficos import generar_graficos


app = Flask(__name__)

ARCHIVO_DESTINATARIOS = "datos/destinatarios.txt"
CAMARAS = [
    {
        "id": "CAM-01",
        "nombre": "Cámara 1",
        "producto": "Carne vacuna",
        "ubicacion": "Sector carnes rojas",
    },
    {
        "id": "CAM-02",
        "nombre": "Cámara 2",
        "producto": "Pollo",
        "ubicacion": "Sector aves",
    },
    {
        "id": "CAM-03",
        "nombre": "Cámara 3",
        "producto": "Embutidos",
        "ubicacion": "Sector fiambres",
    },
]


def obtener_camara(camara_id):
    for camara in CAMARAS:
        if camara["id"] == camara_id:
            return camara

    return CAMARAS[0]

def leer_destinatarios():
    if not os.path.exists(ARCHIVO_DESTINATARIOS):
        return []

    with open(ARCHIVO_DESTINATARIOS, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def guardar_destinatario(email):
    os.makedirs("datos", exist_ok=True)

    destinatarios = leer_destinatarios()

    if email not in destinatarios:
        with open(ARCHIVO_DESTINATARIOS, "a", encoding="utf-8") as archivo:
            archivo.write(email + "\n")


def eliminar_destinatario(email):
    destinatarios = leer_destinatarios()
    destinatarios = [destinatario for destinatario in destinatarios if destinatario != email]

    with open(ARCHIVO_DESTINATARIOS, "w", encoding="utf-8") as archivo:
        for destinatario in destinatarios:
            archivo.write(destinatario + "\n")


def analizar_camara(modo, escenario, camara_id="CAM-01"):
    camara = obtener_camara(camara_id)

    if modo == "automatico":
        escenario = seleccionar_escenario_automatico()

    datos = generar_lecturas_sensor(escenario=escenario)

    datos = calcular_diferencias_centradas(datos)
    datos = calcular_diferencias_adelante(datos)
    datos = generar_alertas(datos)

    datos["camara_id"] = camara["id"]
    datos["camara_nombre"] = camara["nombre"]
    datos["producto"] = camara["producto"]
    datos["ubicacion"] = camara["ubicacion"]

    os.makedirs("resultados/reportes", exist_ok=True)

    nombre_archivo = f"{camara['id']}_{escenario}"
    datos.to_csv(f"resultados/reportes/reporte_{nombre_archivo}.csv", index=False)

    ruta_temperatura, ruta_derivada = generar_graficos(datos, nombre_archivo)

    return datos, escenario, camara, ruta_temperatura, ruta_derivada

def analizar_todas_las_camaras():
    resultados = []

    for camara in CAMARAS:
        datos, escenario_real, camara_info, grafico_temp, grafico_derivada = analizar_camara(
            modo="automatico",
            escenario="normal",
            camara_id=camara["id"]
        )

        resumen = construir_resumen(datos, escenario_real)

        resultados.append({
            "camara": camara_info,
            "escenario": escenario_real,
            "estado": resumen["estado_general"],
            "temp_actual": round(datos["temperatura"].iloc[-1], 2),
            "temp_max": round(datos["temperatura"].max(), 2),
            "temp_min": round(datos["temperatura"].min(), 2),
        })

    return resultados

def obtener_estado_general(datos):
    """
    Devuelve el estado actual de la cámara, tomando como referencia
    la última medición disponible.
    """

    ultima_fila = datos.iloc[-1]
    return ultima_fila["estado"]


def construir_resumen(datos, escenario):
    return {
        "camara": datos["camara_id"].iloc[0],
        "producto": datos["producto"].iloc[0],
        "ubicacion": datos["ubicacion"].iloc[0],
        "escenario": escenario,
        "temp_min": round(datos["temperatura"].min(), 2),
        "temp_max": round(datos["temperatura"].max(), 2),
        "temp_prom": round(datos["temperatura"].mean(), 2),
        "estado_general": obtener_estado_general(datos),
    }


def construir_reporte(datos, escenario):
    return (
        "REPORTE GENERAL - CÁMARA DE FRÍO PARA CONSERVACIÓN DE CARNE\n\n"
        f"Escenario analizado: {escenario}\n\n"
        f"Temperatura mínima registrada: {datos['temperatura'].min():.2f} °C\n"
        f"Temperatura máxima registrada: {datos['temperatura'].max():.2f} °C\n"
        f"Temperatura promedio: {datos['temperatura'].mean():.2f} °C\n\n"
        f"Mayor velocidad de calentamiento: {datos['derivada_centrada'].max():.4f} °C/min\n"
        f"Mayor velocidad de enfriamiento: {datos['derivada_centrada'].min():.4f} °C/min\n\n"
        f"Estados normales: {(datos['estado'] == 'Estado normal').sum()}\n"
        f"Advertencias: {(datos['estado'] == 'Advertencia').sum()}\n"
        f"Alertas críticas: {(datos['estado'] == 'Alerta crítica').sum()}\n"
        f"Emergencias: {(datos['estado'] == 'Emergencia').sum()}\n\n"
        "El análisis fue realizado mediante el método de Diferencias Centradas.\n"
    )


def construir_mensaje_alertas(datos):
    eventos = datos[
        (datos["estado"] != "Estado normal")
        & (datos["estado"] != "Inicializando")
    ]

    def formatear_derivada(valor):
        if valor is None or str(valor) == "nan":
            return "No calculable por extremo"

        return f"{float(valor):.3f} °C/min"

    if eventos.empty:
        return (
            "AVISO DEL SISTEMA DE MONITOREO DE CÁMARA DE FRÍO\n\n"
            "No se detectaron advertencias, alertas críticas ni emergencias.\n\n"
            "La cámara se encuentra funcionando dentro de los parámetros esperados.\n\n"
            f"Temperatura mínima registrada: {datos['temperatura'].min():.2f} °C\n"
            f"Temperatura máxima registrada: {datos['temperatura'].max():.2f} °C\n"
            f"Temperatura promedio: {datos['temperatura'].mean():.2f} °C\n\n"
            "Mensaje generado automáticamente mediante el método de Diferencias Centradas.\n"
        )

    cantidad_eventos = len(eventos)
    cantidad_advertencias = (eventos["estado"] == "Advertencia").sum()
    cantidad_criticas = (eventos["estado"] == "Alerta crítica").sum()
    cantidad_emergencias = (eventos["estado"] == "Emergencia").sum()

    primer_evento = eventos.iloc[0]
    ultimo_evento = eventos.iloc[-1]

    mensaje = (
        "AVISO DEL SISTEMA DE MONITOREO DE CÁMARA DE FRÍO\n\n"
        "Se detectaron advertencias, alertas críticas o emergencias.\n\n"
        "Rango esperado para carne refrigerada: 0 °C a 4 °C\n"
        "Temperatura objetivo aproximada: 2 °C\n\n"
        "RESUMEN DEL EVENTO\n"
        "==================\n"
        f"Eventos detectados: {cantidad_eventos}\n"
        f"Advertencias: {cantidad_advertencias}\n"
        f"Alertas críticas: {cantidad_criticas}\n"
        f"Emergencias: {cantidad_emergencias}\n\n"
        f"Temperatura mínima registrada: {datos['temperatura'].min():.2f} °C\n"
        f"Temperatura máxima registrada: {datos['temperatura'].max():.2f} °C\n"
        f"Temperatura promedio: {datos['temperatura'].mean():.2f} °C\n\n"
        "PRIMER EVENTO DETECTADO\n"
        "=======================\n"
        f"Tiempo: {primer_evento['tiempo']} min\n"
        f"Temperatura: {primer_evento['temperatura']} °C\n"
        f"Derivada centrada: {formatear_derivada(primer_evento['derivada_centrada'])}\n"
        f"Estado: {primer_evento['estado']}\n"
        f"Detalle: {primer_evento['alerta']}\n\n"
        "ÚLTIMO EVENTO DETECTADO\n"
        "=======================\n"
        f"Tiempo: {ultimo_evento['tiempo']} min\n"
        f"Temperatura: {ultimo_evento['temperatura']} °C\n"
        f"Derivada centrada: {formatear_derivada(ultimo_evento['derivada_centrada'])}\n"
        f"Estado: {ultimo_evento['estado']}\n"
        f"Detalle: {ultimo_evento['alerta']}\n\n"
        "Recomendación: revisar puerta, equipo de refrigeración, energía eléctrica y sensor.\n\n"
        "Mensaje generado automáticamente mediante el método de Diferencias Centradas.\n"
    )

    return mensaje

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cámara de Frío</title>

    <link rel="icon" type="image/png"
      href="{{ url_for('static', filename='87-879949_copo-de-nieve-png-copo-de-nieve-png.png') }}">

    <style>
        :root {
            --azul-oscuro: #003049;
            --azul-medio: #0077b6;
            --gris-texto: #263238;
            --sombra: 0 10px 28px rgba(0, 48, 73, 0.14);
        }

        * { box-sizing: border-box; }

        body {
            font-family: Arial, sans-serif;
            margin: 0;
            color: var(--gris-texto);
            min-height: 100vh;
            background-image: url('/static/copos.jpg');
            background-repeat: repeat;
            background-size: 800px;
            background-attachment: fixed;
            background-color: #f8fcff;
        }

        header {
            background: linear-gradient(135deg, #002f4b, #005f8f, #0096c7);
            color: white;
            padding: 42px 20px;
            text-align: center;
            box-shadow: 0 4px 18px rgba(0,0,0,0.22);
        }

        header h1 {
            margin: 0;
            font-size: 36px;
        }

        header p {
            margin-top: 12px;
            font-size: 16px;
            opacity: 0.95;
        }

        main {
            max-width: 1120px;
            margin: 34px auto;
            padding: 0 22px;
        }

        .card {
            background: rgba(255,255,255,0.96);
            padding: 28px;
            margin-bottom: 26px;
            border-radius: 22px;
            box-shadow: var(--sombra);
            border: 1px solid rgba(0,119,182,0.16);
        }

        h2 {
            margin-top: 0;
            color: var(--azul-oscuro);
            border-bottom: 2px solid #d8eef8;
            padding-bottom: 10px;
        }

        label {
            font-weight: bold;
            color: #315466;
        }

        input, select {
            padding: 12px;
            margin: 8px 6px;
            border-radius: 10px;
            border: 1px solid #9bbccc;
            min-width: 240px;
            background: #fbfdff;
            outline: none;
        }

        button {
            padding: 12px 18px;
            margin: 8px 6px;
            border-radius: 10px;
            border: none;
            background: linear-gradient(135deg, #0077b6, #0096c7);
            color: white;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,119,182,0.24);
        }

        button:hover {
            background: linear-gradient(135deg, #005f8a, #0077b6);
        }

        .btn-eliminar {
            background: linear-gradient(135deg, #c1121f, #e63946);
            padding: 7px 12px;
            font-size: 12px;
        }

        .mail-item {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 8px 8px 0 0;
            padding: 9px 12px;
            background: #f1f8ff;
            border-radius: 12px;
            border: 1px solid #cde8f7;
        }

        .check-camara {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 8px 12px 8px 0;
            padding: 10px 14px;
            background: #f1f8ff;
            border-radius: 12px;
            border: 1px solid #cde8f7;
        }

        .check-camara input {
            min-width: unset;
            margin: 0;
        }

        .resumen {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }

        .metric {
            padding: 22px;
            border-radius: 18px;
            background: linear-gradient(135deg, #f8fdff, #e0f3ff);
            text-align: center;
            border: 1px solid #b8dff2;
        }

        .metric strong {
            display: block;
            margin-top: 8px;
            font-size: 21px;
            color: var(--azul-oscuro);
        }

        table {
            border-collapse: collapse;
            width: 100%;
            font-size: 14px;
            background: white;
        }

        th, td {
            border: 1px solid #d0d7de;
            padding: 9px;
            text-align: center;
        }

        th {
            background: linear-gradient(135deg, #006494, #0077b6);
            color: white;
        }

        tr:nth-child(even) {
            background: #f4faff;
        }

        img {
            display: block;
            max-width: 100%;
            border-radius: 18px;
            margin: 14px auto 0;
            border: 1px solid #d0d7de;
            box-shadow: 0 6px 16px rgba(0,0,0,0.10);
        }

        .footer-note {
            text-align: center;
            color: #49616f;
            margin: 34px 0;
            font-size: 13px;
        }

        @media (max-width: 900px) {
            .resumen {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 600px) {
            main { padding: 0 12px; }

            .resumen {
                grid-template-columns: 1fr;
            }

            input, select, button {
                width: 100%;
                min-width: unset;
            }

            .mail-item {
                display: flex;
                width: 100%;
                justify-content: space-between;
            }

            header h1 {
                font-size: 25px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>❄ Sistema de Monitoreo de Cámara de Frío ❄</h1>
    <p>Aplicación del Método de Diferencias Centradas para análisis de temperatura</p>
</header>

<main>

<div class="card">
    <h2>📧 Destinatarios de notificaciones</h2>

    <form action="/agregar-mail" method="post">
        <input type="email" name="email" placeholder="Ingrese correo destinatario" required>
        <button type="submit">Agregar mail</button>
    </form>

    {% if destinatarios %}
        {% for mail in destinatarios %}
            <div class="mail-item">
                <span>{{ mail }}</span>
                <form action="/eliminar-mail" method="post">
                    <input type="hidden" name="email" value="{{ mail }}">
                    <button class="btn-eliminar" type="submit">Eliminar</button>
                </form>
            </div>
        {% endfor %}
    {% else %}
        <p>No hay destinatarios cargados.</p>
    {% endif %}
</div>

<div class="card">
    <h2>🧊 Tablero general de cámaras</h2>
    <p>Vista general del estado actual de todas las cámaras simuladas.</p>

    <form action="/tablero" method="get">
        <button type="submit">Actualizar datos de todas las cámaras</button>
    </form>

    {% if resultados_camaras %}
        <table>
            <thead>
                <tr>
                    <th>Cámara</th>
                    <th>Producto</th>
                    <th>Ubicación</th>
                    <th>Escenario</th>
                    <th>Temp. actual</th>
                    <th>Temp. mínima</th>
                    <th>Temp. máxima</th>
                    <th>Estado actual</th>
                    <th>Detalle</th>
                </tr>
            </thead>
            <tbody>
                {% for item in resultados_camaras %}
                    <tr>
                        <td>{{ item.camara.id }}</td>
                        <td>{{ item.camara.producto }}</td>
                        <td>{{ item.camara.ubicacion }}</td>
                        <td>{{ item.escenario }}</td>
                        <td>{{ item.temp_actual }} °C</td>
                        <td>{{ item.temp_min }} °C</td>
                        <td>{{ item.temp_max }} °C</td>
                        <td><strong>{{ item.estado }}</strong></td>
                        <td>
                            <a href="/camara/{{ item.camara.id }}">
                                Ver detalle
                            </a>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}
</div>

<div class="card">
    <h2>🌡️ Ejecutar monitoreo de una cámara</h2>

    <form action="/monitorear" method="post">

        <label>Cámara:</label>
        <select name="camara_id">
            {% for camara in camaras %}
                <option value="{{ camara.id }}">
                    {{ camara.id }} - {{ camara.producto }} - {{ camara.ubicacion }}
                </option>
            {% endfor %}
        </select>

        <label>Modo:</label>
        <select name="modo" class="selector-modo">
            <option value="demo">Demo: elegir escenario</option>
            <option value="automatico">Automático: sensor simulado</option>
        </select>

        <span class="bloque-escenario">
            <label>Escenario:</label>
            <select name="escenario">
                <option value="normal">Funcionamiento normal</option>
                <option value="puerta_abierta">Puerta abierta</option>
                <option value="falla_compresor">Falla del compresor</option>
                <option value="recuperacion">Recuperación luego de falla</option>
                <option value="camara_apagada">Cámara apagada / corte de energía</option>
            </select>
        </span>

        <button type="submit">Monitorear cámara</button>
    </form>
</div>

<div class="card">
    <h2>📄 Solicitar reporte por email</h2>
    <p>Seleccioná las cámaras que querés incluir en el reporte.</p>

    <form action="/reporte" method="post">

        <div>
            {% for camara in camaras %}
                <label class="check-camara">
                    <input type="checkbox" name="camaras_reporte" value="{{ camara.id }}" checked>
                    {{ camara.id }} - {{ camara.producto }}
                </label>
            {% endfor %}
        </div>

        <label>Modo:</label>
        <select name="modo" class="selector-modo">
            <option value="demo">Demo: elegir escenario</option>
            <option value="automatico">Automático: sensor simulado</option>
        </select>

        <span class="bloque-escenario">
            <label>Escenario:</label>
            <select name="escenario">
                <option value="normal">Funcionamiento normal</option>
                <option value="puerta_abierta">Puerta abierta</option>
                <option value="falla_compresor">Falla del compresor</option>
                <option value="recuperacion">Recuperación luego de falla</option>
                <option value="camara_apagada">Cámara apagada / corte de energía</option>
            </select>
        </span>

        <button type="submit">Enviar reporte</button>
    </form>
</div>

{% if mensaje %}
<div class="card">
    <h2>✅ Resultado</h2>
    <p>{{ mensaje }}</p>
</div>
{% endif %}

{% if resumen %}
<div class="card">
    <h2>📊 Resumen del monitoreo</h2>

    <form method="get" action="/camara/{{ resumen.camara }}">
        <button type="submit">
            🔄 Actualizar datos
        </button>
    </form>

    <div class="resumen">
        <div class="metric">Escenario<br><strong>{{ resumen.escenario }}</strong></div>
        <div class="metric">Temperatura mínima<br><strong>{{ resumen.temp_min }} °C</strong></div>
        <div class="metric">Temperatura máxima<br><strong>{{ resumen.temp_max }} °C</strong></div>
        <div class="metric">Estado general<br><strong>{{ resumen.estado_general }}</strong></div>
    </div>
</div>
{% endif %}

{% if grafico_temperatura %}
<div class="card">
    <h2>📈 Gráfico de Temperatura</h2>
    <img src="/{{ grafico_temperatura }}">
</div>
{% endif %}

{% if grafico_derivada %}
<div class="card">
    <h2>📉 Gráfico de Diferencias Centradas</h2>
    <img src="/{{ grafico_derivada }}">
</div>
{% endif %}

{% if tabla %}
<div class="card">
    <h2>🧮 Datos procesados</h2>
    {{ tabla|safe }}
</div>
{% endif %}

<div class="footer-note">
    Proyecto de Análisis Numérico — Método de Diferencias Centradas
</div>

</main>

<script>
function actualizarEscenarios() {
    const selectores = document.querySelectorAll(".selector-modo");

    selectores.forEach(function(selector) {
        const formulario = selector.closest("form");
        const bloqueEscenario = formulario.querySelector(".bloque-escenario");

        if (selector.value === "automatico") {
            bloqueEscenario.style.display = "none";
        } else {
            bloqueEscenario.style.display = "inline-block";
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const selectores = document.querySelectorAll(".selector-modo");

    selectores.forEach(function(selector) {
        selector.addEventListener("change", actualizarEscenarios);
    });

    actualizarEscenarios();
});
</script>

</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(
        HTML,
        camaras=CAMARAS,
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=None,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )

@app.route("/agregar-mail", methods=["POST"])
def agregar_mail():
    guardar_destinatario(request.form["email"])
    return redirect("/")

@app.route("/tablero")
def tablero():
    resultados_camaras = analizar_todas_las_camaras()

    return render_template_string(
        HTML,
        camaras=CAMARAS,
        resultados_camaras=resultados_camaras,
        destinatarios=leer_destinatarios(),
        mensaje="Tablero actualizado con datos simulados automáticos.",
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )

@app.route("/camara/<camara_id>")
def detalle_camara(camara_id):
    camara = obtener_camara(camara_id)

    datos, escenario_real, camara_info, grafico_temp, grafico_derivada = analizar_camara(
        modo="automatico",
        escenario="normal",
        camara_id=camara["id"]
    )

    return render_template_string(
        HTML,
        camaras=CAMARAS,
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=f"Detalle actualizado para {camara['id']} - {camara['producto']}.",
        tabla=datos.fillna("No calculable").to_html(index=False),
        resumen=construir_resumen(datos, escenario_real),
        grafico_temperatura=grafico_temp,
        grafico_derivada=grafico_derivada,
    )

@app.route("/eliminar-mail", methods=["POST"])
def eliminar_mail():
    eliminar_destinatario(request.form["email"])
    return redirect("/")


@app.route("/monitorear", methods=["POST"])
def monitorear():
    modo = request.form["modo"]
    escenario = request.form.get("escenario", "normal")
    camara_id = request.form.get("camara_id", "CAM-01")

    datos, escenario_real, camara, grafico_temp, grafico_derivada = analizar_camara(
        modo,
        escenario,
        camara_id
    )

    destinatarios = leer_destinatarios()
    eventos = datos[
        (datos["estado"] != "Estado normal")
        & (datos["estado"] != "Inicializando")
    ]

    if not eventos.empty:
        enviado = enviar_email_alerta(
            asunto=f"Advertencia/Alerta Cámara de Frío - {camara['id']}",
            mensaje=construir_mensaje_alertas(datos),
            destinatarios=destinatarios,
        )

        if enviado:
            mensaje = f"Se detectaron eventos en {camara['id']} - {camara['producto']}. Se envió notificación por email."
        else:
            mensaje = "Se detectaron eventos, pero no se pudo enviar el email. Verifique destinatarios y configuración."
    else:
        mensaje = f"{camara['id']} - {camara['producto']}: funcionamiento normal. No se enviaron alertas."

    return render_template_string(
        HTML,
        camaras=CAMARAS,
        resultados_camaras=None,
        destinatarios=destinatarios,
        mensaje=mensaje,
        tabla=datos.fillna("No calculable").to_html(index=False),
        resumen=construir_resumen(datos, escenario_real),
        grafico_temperatura=grafico_temp,
        grafico_derivada=grafico_derivada,
    )


@app.route("/reporte", methods=["POST"])
def reporte():
    modo = request.form["modo"]
    escenario = request.form.get("escenario", "normal")
    camaras_seleccionadas = request.form.getlist("camaras_reporte")

    if not camaras_seleccionadas:
        return render_template_string(
            HTML,
            camaras=CAMARAS,
            resultados_camaras=None,
            destinatarios=leer_destinatarios(),
            mensaje="Debe seleccionar al menos una cámara para generar el reporte.",
            tabla=None,
            resumen=None,
            grafico_temperatura=None,
            grafico_derivada=None,
        )

    destinatarios = leer_destinatarios()

    reporte_general = (
        "REPORTE GENERAL - SISTEMA DE CÁMARAS DE FRÍO\n\n"
        "Análisis realizado mediante el método de Diferencias Centradas.\n\n"
    )

    tablas = []

    ultimo_datos = None
    ultimo_escenario = None
    ultimo_grafico_temp = None
    ultimo_grafico_derivada = None

    for camara_id in camaras_seleccionadas:
        datos, escenario_real, camara, grafico_temp, grafico_derivada = analizar_camara(
            modo,
            escenario,
            camara_id
        )

        ultimo_datos = datos
        ultimo_escenario = escenario_real
        ultimo_grafico_temp = grafico_temp
        ultimo_grafico_derivada = grafico_derivada

        estado_actual = obtener_estado_general(datos)

        reporte_general += (
            f"----------------------------------------\n"
            f"Cámara: {camara['id']} - {camara['producto']}\n"
            f"Ubicación: {camara['ubicacion']}\n"
            f"Escenario analizado: {escenario_real}\n\n"
            f"Temperatura mínima: {datos['temperatura'].min():.2f} °C\n"
            f"Temperatura máxima: {datos['temperatura'].max():.2f} °C\n"
            f"Temperatura promedio: {datos['temperatura'].mean():.2f} °C\n"
            f"Estado actual: {estado_actual}\n\n"
            f"Estados normales: {(datos['estado'] == 'Estado normal').sum()}\n"
            f"Inicializando: {(datos['estado'] == 'Inicializando').sum()}\n"
            f"Advertencias: {(datos['estado'] == 'Advertencia').sum()}\n"
            f"Alertas críticas: {(datos['estado'] == 'Alerta crítica').sum()}\n"
            f"Emergencias: {(datos['estado'] == 'Emergencia').sum()}\n\n"
        )

        tablas.append(
            f"<h3>{camara['id']} - {camara['producto']}</h3>"
            + datos.fillna("No calculable").to_html(index=False)
        )

    enviado = enviar_email_alerta(
        asunto="Reporte General Cámaras de Frío",
        mensaje=reporte_general,
        destinatarios=destinatarios,
    )

    mensaje = (
        "Reporte enviado correctamente para las cámaras seleccionadas."
        if enviado
        else "No se pudo enviar el reporte."
    )

    tabla_html = "<br>".join(tablas)

    return render_template_string(
        HTML,
        camaras=CAMARAS,
        resultados_camaras=None,
        destinatarios=destinatarios,
        mensaje=mensaje,
        tabla=tabla_html,
        resumen=construir_resumen(ultimo_datos, ultimo_escenario),
        grafico_temperatura=ultimo_grafico_temp,
        grafico_derivada=ultimo_grafico_derivada,
    )


@app.route("/resultados/graficos/<path:filename>")
def mostrar_grafico(filename):
    return send_from_directory("resultados/graficos", filename)


if __name__ == "__main__":
    app.run(debug=True)
