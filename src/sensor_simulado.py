import random
import pandas as pd


def generar_lecturas_sensor(
    escenario="normal",
    intervalo_minutos=5,
    cantidad_mediciones=20,
    temperatura_inicial=8.0,
    temperatura_objetivo=2.0,
):
    tiempos = []
    temperaturas = []
    temperatura_actual = temperatura_inicial

    for i in range(cantidad_mediciones):
        tiempo = i * intervalo_minutos
        tiempos.append(tiempo)

        ruido = random.uniform(-0.15, 0.15)

        if escenario == "normal":
            diferencia = temperatura_actual - temperatura_objetivo
            temperatura_actual -= diferencia * 0.25

        elif escenario == "puerta_abierta":
            if i < 8:
                diferencia = temperatura_actual - temperatura_objetivo
                temperatura_actual -= diferencia * 0.25
            else:
                temperatura_actual += random.uniform(0.30, 0.55)

        elif escenario == "falla_compresor":
            if i < 5:
                diferencia = temperatura_actual - temperatura_objetivo
                temperatura_actual -= diferencia * 0.20
            else:
                temperatura_actual += random.uniform(0.12, 0.30)

        elif escenario == "recuperacion":
            if i < 6:
                diferencia = temperatura_actual - temperatura_objetivo
                temperatura_actual -= diferencia * 0.25
            elif i < 12:
                temperatura_actual += random.uniform(0.35, 0.60)
            else:
                diferencia = temperatura_actual - temperatura_objetivo
                temperatura_actual -= diferencia * 0.30

        elif escenario == "camara_apagada":
            if i < 5:
                diferencia = temperatura_actual - temperatura_objetivo
                temperatura_actual -= diferencia * 0.25
            else:
                temperatura_actual += random.uniform(0.70, 1.20)

        else:
            raise ValueError("Escenario no válido.")

        temperatura_actual += ruido
        temperaturas.append(round(temperatura_actual, 2))

    return pd.DataFrame({
        "tiempo": tiempos,
        "temperatura": temperaturas
    })


def seleccionar_escenario_automatico():
    return random.choices(
        ["normal", "puerta_abierta", "falla_compresor", "recuperacion", "camara_apagada"],
        weights=[65, 12, 10, 8, 5],
        k=1
    )[0]