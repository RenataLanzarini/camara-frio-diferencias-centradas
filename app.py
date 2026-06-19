import os
import json
import time
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DESTINATARIOS = os.path.join(BASE_DIR, "datos", "destinatarios.txt")
ARCHIVO_CAMARAS = os.path.join(BASE_DIR, "datos", "camaras.json")
CAMARAS_INICIALES = [
    {
        "id": "CAM-01",
        "nombre": "Cámara 1",
        "producto": "Carne vacuna",
        "ubicacion": "Sector carnes rojas",
        "destinatarios": [],
    },
    {
        "id": "CAM-02",
        "nombre": "Cámara 2",
        "producto": "Pollo",
        "ubicacion": "Sector aves",
        "destinatarios": [],
    },
    {
        "id": "CAM-03",
        "nombre": "Cámara 3",
        "producto": "Embutidos",
        "ubicacion": "Sector fiambres",
        "destinatarios": [],
    },
]


@app.context_processor
def contexto_global():
    return {
        "cache_buster": int(time.time() * 1000),
        "mails_notificacion": obtener_mails_con_camaras(),
    }


def normalizar_camara(camara):
    return {
        "id": camara.get("id", "").strip().upper(),
        "nombre": camara.get("nombre", "").strip(),
        "producto": camara.get("producto", "").strip(),
        "ubicacion": camara.get("ubicacion", "").strip(),
        "destinatarios": sorted({
            email.strip().lower()
            for email in camara.get("destinatarios", [])
            if email.strip()
        }),
    }


def guardar_camaras(camaras):
    os.makedirs(os.path.dirname(ARCHIVO_CAMARAS), exist_ok=True)
    camaras = [normalizar_camara(camara) for camara in camaras]

    with open(ARCHIVO_CAMARAS, "w", encoding="utf-8") as archivo:
        json.dump(camaras, archivo, ensure_ascii=False, indent=2)


def leer_camaras():
    os.makedirs(os.path.dirname(ARCHIVO_CAMARAS), exist_ok=True)

    if not os.path.exists(ARCHIVO_CAMARAS):
        guardar_camaras(CAMARAS_INICIALES)

    with open(ARCHIVO_CAMARAS, "r", encoding="utf-8") as archivo:
        camaras = json.load(archivo)

    camaras = [normalizar_camara(camara) for camara in camaras]

    if not camaras:
        camaras = [normalizar_camara(camara) for camara in CAMARAS_INICIALES]
        guardar_camaras(camaras)

    return camaras


def obtener_camara(camara_id):
    camaras = leer_camaras()

    for camara in camaras:
        if camara["id"] == camara_id:
            return camara

    return camaras[0]


def agregar_camara(camara):
    camaras = leer_camaras()
    nueva_camara = normalizar_camara(camara)

    if not all([
        nueva_camara["id"],
        nueva_camara["nombre"],
        nueva_camara["producto"],
        nueva_camara["ubicacion"],
    ]):
        return False, "Debe completar todos los datos de la cámara."

    if any(camara["id"] == nueva_camara["id"] for camara in camaras):
        return False, f"Ya existe una cámara con el ID {nueva_camara['id']}."

    camaras.append(nueva_camara)
    guardar_camaras(camaras)
    return True, f"Cámara {nueva_camara['id']} agregada correctamente."


def eliminar_camara_por_id(camara_id):
    camaras = leer_camaras()

    if len(camaras) <= 1:
        return False, "Debe quedar al menos una cámara para monitorear."

    camaras_filtradas = [
        camara for camara in camaras
        if camara["id"] != camara_id
    ]

    if len(camaras_filtradas) == len(camaras):
        return False, "No se encontró la cámara seleccionada."

    guardar_camaras(camaras_filtradas)
    return True, f"Cámara {camara_id} eliminada correctamente."


def agregar_destinatario_camara(camara_id, email):
    email = email.strip().lower()

    if not email:
        return False, "Ingrese un correo válido."

    camaras = leer_camaras()

    for camara in camaras:
        if camara["id"] == camara_id:
            if email not in camara["destinatarios"]:
                camara["destinatarios"].append(email)
            guardar_camaras(camaras)
            return True, f"Correo agregado a {camara_id}."

    return False, "No se encontró la cámara seleccionada."


def eliminar_destinatario_camara(camara_id, email):
    email = email.strip().lower()
    camaras = leer_camaras()

    for camara in camaras:
        if camara["id"] == camara_id:
            camara["destinatarios"] = [
                destinatario
                for destinatario in camara["destinatarios"]
                if destinatario != email
            ]
            guardar_camaras(camaras)
            return True, f"Correo eliminado de {camara_id}."

    return False, "No se encontró la cámara seleccionada."


def obtener_semilla_simulacion(*partes):
    semilla_base = os.getenv("SIMULACION_SEMILLA")

    if not semilla_base:
        return None

    return "-".join([semilla_base, *[str(parte) for parte in partes]])

def leer_destinatarios():
    if not os.path.exists(ARCHIVO_DESTINATARIOS):
        return []

    with open(ARCHIVO_DESTINATARIOS, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def guardar_destinatario(email):
    os.makedirs(os.path.dirname(ARCHIVO_DESTINATARIOS), exist_ok=True)

    email = email.strip().lower()
    if not email:
        return

    destinatarios = obtener_destinatarios_camara(camara)

    if email not in destinatarios:
        with open(ARCHIVO_DESTINATARIOS, "a", encoding="utf-8") as archivo:
            archivo.write(email + "\n")


def eliminar_destinatario(email):
    email = email.strip().lower()
    destinatarios = leer_destinatarios()
    destinatarios = [destinatario for destinatario in destinatarios if destinatario != email]

    with open(ARCHIVO_DESTINATARIOS, "w", encoding="utf-8") as archivo:
        for destinatario in destinatarios:
            archivo.write(destinatario + "\n")


def obtener_mails_con_camaras():
    asignaciones = {}

    for camara in leer_camaras():
        for email in camara.get("destinatarios", []):
            asignaciones.setdefault(email, set()).add(camara["id"])

    return [
        {
            "email": email,
            "camaras": sorted(camara_ids),
        }
        for email, camara_ids in sorted(asignaciones.items())
    ]


def asignar_destinatario_a_camaras(email, camara_ids):
    email = email.strip().lower()
    camara_ids = set(camara_ids)

    if not email:
        return False, "Ingrese un correo válido."

    if not camara_ids:
        return False, "Seleccione al menos una cámara para el correo."

    camaras = leer_camaras()

    for camara in camaras:
        camara["destinatarios"] = [
            destinatario
            for destinatario in camara.get("destinatarios", [])
            if destinatario != email
        ]

        if camara["id"] in camara_ids:
            camara["destinatarios"].append(email)

    guardar_camaras(camaras)
    return True, f"Asignaciones actualizadas para {email}."


def eliminar_destinatario_de_todas_las_camaras(email):
    email = email.strip().lower()
    camaras = leer_camaras()

    for camara in camaras:
        camara["destinatarios"] = [
            destinatario
            for destinatario in camara.get("destinatarios", [])
            if destinatario != email
        ]

    guardar_camaras(camaras)
    return True, f"Correo {email} eliminado de todas las cámaras."


def obtener_destinatarios_camara(camara):
    return camara.get("destinatarios", [])


def obtener_destinatarios_camaras(camara_ids):
    destinatarios = []

    for camara_id in camara_ids:
        camara = obtener_camara(camara_id)
        destinatarios.extend(obtener_destinatarios_camara(camara))

    return sorted(set(destinatarios))


def analizar_camara(modo, escenario, camara_id="CAM-01"):
    camara = obtener_camara(camara_id)

    if modo == "automatico":
        escenario = seleccionar_escenario_automatico(
            semilla=obtener_semilla_simulacion(camara_id, "escenario")
        )

    datos = generar_lecturas_sensor(
        escenario=escenario,
        semilla=obtener_semilla_simulacion(camara_id, escenario),
    )

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

    for camara in leer_camaras():
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
        "camara_nombre": datos["camara_nombre"].iloc[0],
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
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cámara de Frío</title>

    <link rel="icon" type="image/png"
      href="{{ url_for('static', filename='87-879949_copo-de-nieve-png-copo-de-nieve-png.png') }}">

    <style>
        :root {
            --azul-oscuro: #003049;
            --azul-medio: #0077b6;
            --azul-panel: #3c5466;
            --azul-panel-oscuro: #314657;
            --azul-panel-claro: #496375;
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
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
            background-color: #f8fcff;
        }

        header {
            background: #001D45;
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
            background: var(--azul-panel);
            color: white;
            padding: 28px;
            margin-bottom: 26px;
            border-radius: 22px;
            box-shadow: var(--sombra);
            border: 1px solid rgba(255,255,255,0.28);
        }

        h2 {
            margin-top: 0;
            color: white;
            border-bottom: 2px solid rgba(255,255,255,0.32);
            padding-bottom: 10px;
        }

        label {
            font-weight: bold;
            color: white;
        }

        input, select {
            padding: 12px;
            margin: 8px 6px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.42);
            min-width: 240px;
            background: var(--azul-panel);
            color: white;
            outline: none;
        }

        form {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
        }

        input::placeholder {
            color: rgba(255,255,255,0.78);
        }

        option {
            color: white;
            background: var(--azul-panel);
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
            background: var(--azul-panel);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.32);
        }

        .check-camara {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 8px 12px 8px 0;
            padding: 10px 14px;
            background: var(--azul-panel);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.32);
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
            background: var(--azul-panel);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.32);
        }

        .metric strong {
            display: block;
            margin-top: 8px;
            font-size: 21px;
            color: white;
        }

        .detalle-camara-destacada {
            border: 1px solid rgba(255,255,255,0.36);
            border-radius: 14px;
            padding: 16px;
            margin: 14px 0 18px;
            background: var(--azul-panel-oscuro);
        }

        .detalle-camara-destacada span {
            display: block;
            font-size: 13px;
            opacity: 0.86;
            margin-bottom: 6px;
        }

        .detalle-camara-destacada strong {
            display: block;
            font-size: 28px;
            line-height: 1.2;
        }

        .detalle-camara-destacada small {
            display: block;
            margin-top: 6px;
            font-size: 15px;
            opacity: 0.95;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            min-width: 760px;
            font-size: 14px;
            background: var(--azul-panel);
            color: white;
        }

        th, td {
            border: 1px solid rgba(255,255,255,0.35);
            padding: 9px;
            text-align: center;
        }

        th {
            background: var(--azul-panel-oscuro);
            color: white;
        }

        tr:nth-child(even) {
            background: var(--azul-panel-claro);
        }

        a {
            color: white;
            font-weight: bold;
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

        main.actualizando {
            opacity: 0.62;
            pointer-events: none;
            transition: opacity 0.18s ease;
        }

        .tabla-scroll {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        .camara-admin {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin-top: 16px;
        }

        .camara-admin-item {
            border: 1px solid rgba(255,255,255,0.32);
            border-radius: 14px;
            padding: 16px;
        }

        .camara-admin-item h3 {
            margin: 0 0 10px;
        }

        .acciones-inline {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
        }

        .mail-admin {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            margin-top: 18px;
        }

        .mail-admin-item {
            border: 1px solid rgba(255,255,255,0.32);
            border-radius: 14px;
            padding: 14px;
        }

        .mail-admin-header {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 10px;
        }

        .selector-camaras {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .selector-camaras label {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 1px solid rgba(255,255,255,0.32);
            border-radius: 12px;
            padding: 8px 10px;
        }

        .selector-camaras input {
            width: auto;
            min-width: unset;
            margin: 0;
        }

        .desplegable-reporte {
            width: 100%;
            border: 1px solid rgba(255,255,255,0.32);
            border-radius: 14px;
            padding: 12px;
            margin: 8px 0;
        }

        .desplegable-reporte summary {
            cursor: pointer;
            font-weight: bold;
        }

        .desplegable-reporte[open] summary {
            margin-bottom: 10px;
        }

        @media (max-width: 900px) {
            .resumen {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 600px) {
            body {
                background-attachment: scroll;
            }

            header {
                padding: 28px 14px;
            }

            main {
                margin: 18px auto;
                padding: 0 10px;
            }

            .card {
                border-radius: 14px;
                padding: 16px;
                margin-bottom: 16px;
            }

            .resumen {
                grid-template-columns: 1fr;
            }

            form,
            .acciones-inline,
            .mail-admin-header,
            .selector-camaras {
                display: block;
            }

            input, select, button {
                width: 100%;
                min-width: unset;
                margin: 7px 0;
            }

            .mail-item {
                display: flex;
                width: 100%;
                justify-content: space-between;
            }

            header h1 {
                font-size: 25px;
            }

            header p {
                font-size: 14px;
            }

            table {
                min-width: 680px;
                font-size: 13px;
            }

            .detalle-camara-destacada strong {
                font-size: 23px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>❄ Sistema de Monitoreo de Cámara de Frío ❄</h1>
    <p>Aplicación del Método de Diferencias Centradas para análisis de temperatura</p>
</header>

<main id="contenido-principal">

<div class="card">
    <h2>⚙️ Cámaras y notificaciones</h2>

    <h3>Agregar destinatario</h3>
    <form action="/agregar-mail" method="post">
        <input type="email" name="email" placeholder="Correo destinatario" required>
        <div class="selector-camaras">
            {% for camara in camaras %}
                <label>
                    <input type="checkbox" name="camaras_mail" value="{{ camara.id }}">
                    {{ camara.id }}
                </label>
            {% endfor %}
        </div>
        <button type="submit">Guardar destinatario</button>
    </form>

    {% if mails_notificacion %}
        <div class="mail-admin">
            {% for item in mails_notificacion %}
                <div class="mail-admin-item">
                    <div class="mail-admin-header">
                        <strong>{{ item.email }}</strong>
                        <form action="/eliminar-mail" method="post">
                            <input type="hidden" name="email" value="{{ item.email }}">
                            <button class="btn-eliminar" type="submit">Eliminar</button>
                        </form>
                    </div>

                    <form action="/actualizar-mail-camaras" method="post">
                        <input type="hidden" name="email" value="{{ item.email }}">
                        <div class="selector-camaras">
                            {% for camara in camaras %}
                                <label>
                                    <input
                                        type="checkbox"
                                        name="camaras_mail"
                                        value="{{ camara.id }}"
                                        {% if camara.id in item.camaras %}checked{% endif %}
                                    >
                                    {{ camara.id }}
                                </label>
                            {% endfor %}
                        </div>
                        <button type="submit">Actualizar cámaras</button>
                    </form>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>No hay destinatarios cargados.</p>
    {% endif %}

    <h3>Administrar cámaras</h3>
    <form action="/agregar-camara" method="post">
        <input type="text" name="id" placeholder="ID. Ej: CAM-04" required>
        <input type="text" name="nombre" placeholder="Nombre de la cámara" required>
        <input type="text" name="producto" placeholder="Producto" required>
        <input type="text" name="ubicacion" placeholder="Ubicación" required>
        <button type="submit">Agregar cámara</button>
    </form>

    <div class="camara-admin">
        {% for camara in camaras %}
            <div class="camara-admin-item">
                <h3>{{ camara.id }} - {{ camara.nombre }}</h3>
                <p>{{ camara.producto }} · {{ camara.ubicacion }}</p>

                <div class="acciones-inline">
                    <form action="/eliminar-camara" method="post">
                        <input type="hidden" name="camara_id" value="{{ camara.id }}">
                        <button class="btn-eliminar" type="submit">Eliminar cámara</button>
                    </form>
                </div>
            </div>
        {% endfor %}
    </div>
</div>

<div class="card">
    <h2>🧊 Tablero general de cámaras</h2>
    <p>Vista general del estado actual de todas las cámaras simuladas.</p>

    <form action="/tablero" method="get">
        <button type="submit">Actualizar datos de todas las cámaras</button>
    </form>

    {% if resultados_camaras %}
        <div class="tabla-scroll">
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
        </div>
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

        <details class="desplegable-reporte">
            <summary>Destinatarios del reporte</summary>
            {% if mails_notificacion %}
                <div class="selector-camaras">
                    {% for item in mails_notificacion %}
                        <label>
                            <input type="checkbox" name="mails_reporte" value="{{ item.email }}">
                            {{ item.email }}
                        </label>
                    {% endfor %}
                </div>
            {% else %}
                <p>No hay mails cargados para seleccionar.</p>
            {% endif %}
        </details>

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

    <div class="detalle-camara-destacada">
        <span>Detalle correspondiente a</span>
        <strong>{{ resumen.camara }} - {{ resumen.camara_nombre }}</strong>
        <small>{{ resumen.producto }} · {{ resumen.ubicacion }}</small>
    </div>

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
    <img src="/{{ grafico_temperatura }}?v={{ cache_buster }}">
</div>
{% endif %}

{% if grafico_derivada %}
<div class="card">
    <h2>📉 Gráfico de Diferencias Centradas</h2>
    <img src="/{{ grafico_derivada }}?v={{ cache_buster }}">
</div>
{% endif %}

{% if tabla %}
<div class="card">
    <h2>🧮 Datos procesados</h2>
    <div class="tabla-scroll">
        {{ tabla|safe }}
    </div>
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

function esAccionParcial(ruta) {
    return (
        ruta === "/tablero"
        || ruta === "/monitorear"
        || ruta === "/reporte"
        || ruta === "/agregar-camara"
        || ruta === "/eliminar-camara"
        || ruta === "/agregar-mail"
        || ruta === "/eliminar-mail"
        || ruta === "/actualizar-mail-camaras"
        || ruta.startsWith("/camara/")
    );
}

async function actualizarContenidoDesdeRespuesta(respuesta) {
    const html = await respuesta.text();
    const documento = new DOMParser().parseFromString(html, "text/html");
    const nuevoContenido = documento.querySelector("#contenido-principal");
    const contenidoActual = document.querySelector("#contenido-principal");

    if (!nuevoContenido || !contenidoActual) {
        window.location.reload();
        return;
    }

    contenidoActual.innerHTML = nuevoContenido.innerHTML;
    inicializarInteracciones();
}

async function enviarFormularioParcial(event) {
    const formulario = event.currentTarget;
    const url = new URL(formulario.action, window.location.origin);

    if (!esAccionParcial(url.pathname)) {
        return;
    }

    event.preventDefault();

    const contenido = document.querySelector("#contenido-principal");
    const metodo = formulario.method.toUpperCase();
    const opciones = { method: metodo };

    if (metodo !== "GET") {
        opciones.body = new FormData(formulario);
    }

    contenido.classList.add("actualizando");

    try {
        const respuesta = await fetch(formulario.action, opciones);
        await actualizarContenidoDesdeRespuesta(respuesta);
    } finally {
        contenido.classList.remove("actualizando");
    }
}

async function abrirEnContenido(event) {
    const enlace = event.currentTarget;
    const url = new URL(enlace.href, window.location.origin);

    if (!esAccionParcial(url.pathname)) {
        return;
    }

    event.preventDefault();

    const contenido = document.querySelector("#contenido-principal");
    contenido.classList.add("actualizando");

    try {
        const respuesta = await fetch(enlace.href);
        await actualizarContenidoDesdeRespuesta(respuesta);
    } finally {
        contenido.classList.remove("actualizando");
    }
}

function inicializarInteracciones() {
    const selectores = document.querySelectorAll(".selector-modo");

    selectores.forEach(function(selector) {
        selector.addEventListener("change", actualizarEscenarios);
    });

    document.querySelectorAll("form").forEach(function(formulario) {
        formulario.addEventListener("submit", enviarFormularioParcial);
    });

    document.querySelectorAll("a").forEach(function(enlace) {
        enlace.addEventListener("click", abrirEnContenido);
    });

    actualizarEscenarios();
}

document.addEventListener("DOMContentLoaded", function() {
    inicializarInteracciones();
});
</script>

</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(
        HTML,
        camaras=leer_camaras(),
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
    _, mensaje = asignar_destinatario_a_camaras(
        request.form.get("email", ""),
        request.form.getlist("camaras_mail"),
    )

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


@app.route("/agregar-camara", methods=["POST"])
def agregar_camara_web():
    _, mensaje = agregar_camara({
        "id": request.form.get("id", ""),
        "nombre": request.form.get("nombre", ""),
        "producto": request.form.get("producto", ""),
        "ubicacion": request.form.get("ubicacion", ""),
        "destinatarios": [],
    })

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


@app.route("/eliminar-camara", methods=["POST"])
def eliminar_camara_web():
    _, mensaje = eliminar_camara_por_id(request.form.get("camara_id", ""))

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


@app.route("/agregar-mail-camara", methods=["POST"])
def agregar_mail_camara_web():
    _, mensaje = agregar_destinatario_camara(
        request.form.get("camara_id", ""),
        request.form.get("email", ""),
    )

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


@app.route("/eliminar-mail-camara", methods=["POST"])
def eliminar_mail_camara_web():
    _, mensaje = eliminar_destinatario_camara(
        request.form.get("camara_id", ""),
        request.form.get("email", ""),
    )

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


@app.route("/tablero")
def tablero():
    resultados_camaras = analizar_todas_las_camaras()

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
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
        camaras=leer_camaras(),
        resultados_camaras=analizar_todas_las_camaras(),
        destinatarios=leer_destinatarios(),
        mensaje=f"Detalle actualizado para {camara['id']} - {camara['producto']}.",
        tabla=datos.fillna("No calculable").to_html(index=False),
        resumen=construir_resumen(datos, escenario_real),
        grafico_temperatura=grafico_temp,
        grafico_derivada=grafico_derivada,
    )

@app.route("/eliminar-mail", methods=["POST"])
def eliminar_mail():
    _, mensaje = eliminar_destinatario_de_todas_las_camaras(
        request.form.get("email", "")
    )

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


@app.route("/actualizar-mail-camaras", methods=["POST"])
def actualizar_mail_camaras():
    _, mensaje = asignar_destinatario_a_camaras(
        request.form.get("email", ""),
        request.form.getlist("camaras_mail"),
    )

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
        resultados_camaras=None,
        destinatarios=leer_destinatarios(),
        mensaje=mensaje,
        tabla=None,
        resumen=None,
        grafico_temperatura=None,
        grafico_derivada=None,
    )


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
            mensaje = (
                f"Se detectaron eventos en {camara['id']}, pero no se pudo enviar el email. "
                "Verifique que la cámara tenga destinatarios y credenciales configuradas."
            )
    else:
        mensaje = f"{camara['id']} - {camara['producto']}: funcionamiento normal. No se enviaron alertas."

    return render_template_string(
        HTML,
        camaras=leer_camaras(),
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
    destinatarios = sorted(set(request.form.getlist("mails_reporte")))

    if not camaras_seleccionadas:
        return render_template_string(
            HTML,
            camaras=leer_camaras(),
            resultados_camaras=None,
            destinatarios=leer_destinatarios(),
            mensaje="Debe seleccionar al menos una cámara para generar el reporte.",
            tabla=None,
            resumen=None,
            grafico_temperatura=None,
            grafico_derivada=None,
        )

    if not destinatarios:
        return render_template_string(
            HTML,
            camaras=leer_camaras(),
            resultados_camaras=None,
            destinatarios=leer_destinatarios(),
            mensaje="Debe seleccionar al menos un mail para enviar el reporte.",
            tabla=None,
            resumen=None,
            grafico_temperatura=None,
            grafico_derivada=None,
        )

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
        camaras=leer_camaras(),
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
