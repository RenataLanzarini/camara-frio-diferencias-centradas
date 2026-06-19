import os
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(tempfile.gettempdir(), "camara-frio-matplotlib"),
)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def generar_graficos(datos, escenario):
    os.makedirs("resultados/graficos", exist_ok=True)

    ruta_temperatura = f"resultados/graficos/temperatura_{escenario}.png"
    ruta_derivada = f"resultados/graficos/derivada_{escenario}.png"

    plt.figure()
    plt.plot(datos["tiempo"], datos["temperatura"], marker="o")
    plt.axhline(0, linestyle="--", label="Límite mínimo 0 °C")
    plt.axhline(4, linestyle="--", label="Límite máximo 4 °C")
    plt.axhline(2, linestyle=":", label="Objetivo 2 °C")
    plt.xlabel("Tiempo (min)")
    plt.ylabel("Temperatura (°C)")
    plt.title(f"Temperatura - {escenario}")
    plt.legend()
    plt.grid(True)
    plt.savefig(ruta_temperatura)
    plt.close()

    plt.figure()
    plt.plot(
        datos["tiempo"],
        datos["derivada_centrada"],
        marker="o",
        label="Diferencias centradas"
    )

    plt.plot(
        datos["tiempo"],
        datos["derivada_adelante"],
        marker="x",
        label="Diferencias hacia adelante"
    )

    plt.axhline(0, linestyle="--", label="Estabilidad")
    plt.xlabel("Tiempo (min)")
    plt.ylabel("dT/dt (°C/min)")
    plt.title(f"Velocidad de cambio - {escenario}")
    plt.legend()
    plt.grid(True)
    plt.savefig(ruta_derivada)
    plt.close()

    return ruta_temperatura, ruta_derivada
