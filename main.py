import os

from src.sensor_simulado import generar_lecturas_sensor
from src.diferencias_centradas import (
    calcular_diferencias_centradas,
    calcular_diferencias_adelante,
)
from src.alertas import generar_alertas
from src.notificaciones import enviar_email_alerta
from src.graficos import generar_graficos

def exportar_resultados(datos, escenario):
    """
    Guarda los resultados procesados en un archivo CSV.
    """

    os.makedirs("resultados/reportes", exist_ok=True)
    ruta = f"resultados/reportes/reporte_{escenario}.csv"
    datos.to_csv(ruta, index=False)
    print(f"Reporte exportado en: {ruta}")

def construir_mensaje_alerta(alertas_criticas):
    """
    Construye el contenido del email de alerta.
    """

    mensaje = (
        "ALERTA - CÁMARA DE FRÍO PARA CONSERVACIÓN DE CARNE\n\n"
        "El sistema detectó una o más condiciones anómalas.\n\n"
        "Rango esperado de operación: 0 °C a 4 °C\n"
        "Temperatura objetivo: 2 °C\n\n"
        "DETALLE DE ALERTAS\n"
        "===================\n\n"
    )

    for _, fila in alertas_criticas.iterrows():
        mensaje += (
            f"Tiempo registrado: {fila['tiempo']} min\n"
            f"Temperatura registrada: {fila['temperatura']} °C\n"
            f"Derivada por diferencias centradas: "
            f"{fila['derivada_centrada']} °C/min\n"
            f"Derivada por diferencias hacia adelante: "
            f"{fila['derivada_adelante']} °C/min\n"
            f"Alerta detectada: {fila['alerta']}\n"
            "Recomendación: verificar el cierre de la puerta, "
            "el funcionamiento del sistema de refrigeración "
            "y el estado del sensor.\n\n"
        )

    mensaje += (
        "----------------------------------------\n"
        "Mensaje generado automáticamente por el\n"
        "Sistema de Monitoreo de Cámara de Frío\n"
        "Proyecto de Análisis Numérico\n"
        "Tema: Método de Diferencias Centradas\n"
        "----------------------------------------\n"
    )

    return mensaje

def ejecutar_monitoreo(escenario):
    """
    Ejecuta el flujo completo del sistema.
    """

    print("\n========================================")
    print(" SISTEMA DE MONITOREO DE CÁMARA DE FRÍO")
    print("========================================")
    print(f"Escenario seleccionado: {escenario}\n")

    semilla = os.getenv("SIMULACION_SEMILLA")
    datos = generar_lecturas_sensor(escenario=escenario, semilla=semilla)

    datos = calcular_diferencias_centradas(datos)
    datos = calcular_diferencias_adelante(datos)
    datos = generar_alertas(datos)

    print("Lecturas procesadas:\n")
    print(datos)

    exportar_resultados(datos, escenario)
    generar_graficos(datos, escenario)

    alertas_criticas = datos[datos["alerta"] != "Estado normal"]

    if not alertas_criticas.empty:
        mensaje = construir_mensaje_alerta(alertas_criticas)

        print("\n⚠ ALERTAS DETECTADAS\n")
        print(mensaje)

        enviar_email_alerta(
            asunto="Alerta Cámara de Frío - Temperatura fuera de rango",
            mensaje=mensaje
        )
    else:
        print("\n✅ No se detectaron alertas.\n")

def mostrar_menu():
    """
    Menú principal del sistema.
    """

    print("\nSeleccione un escenario:")
    print("1. Funcionamiento normal")
    print("2. Puerta abierta")
    print("3. Falla del compresor")
    print("4. Recuperación luego de falla")

    opcion = input("\nIngrese una opción: ")

    escenarios = {
        "1": "normal",
        "2": "puerta_abierta",
        "3": "falla_compresor",
        "4": "recuperacion",
    }

    return escenarios.get(opcion, "normal")

def main():
    escenario = mostrar_menu()
    ejecutar_monitoreo(escenario)

if __name__ == "__main__":
    main()
