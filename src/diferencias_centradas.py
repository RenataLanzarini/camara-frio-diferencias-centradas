def calcular_diferencias_centradas(
    datos,
    columna_tiempo="tiempo",
    columna_temperatura="temperatura"
):
    """
    Calcula dT/dt usando diferencias centradas:

    dT/dt ≈ (T(i+1) - T(i-1)) / (t(i+1) - t(i-1))
    """

    datos = datos.copy()
    derivadas = []

    for i in range(len(datos)):
        if i == 0 or i == len(datos) - 1:
            derivadas.append(None)
        else:
            temp_siguiente = datos.loc[i + 1, columna_temperatura]
            temp_anterior = datos.loc[i - 1, columna_temperatura]

            tiempo_siguiente = datos.loc[i + 1, columna_tiempo]
            tiempo_anterior = datos.loc[i - 1, columna_tiempo]

            derivada = (temp_siguiente - temp_anterior) / (
                tiempo_siguiente - tiempo_anterior
            )

            derivadas.append(round(derivada, 4))

    datos["derivada_centrada"] = derivadas
    return datos


def calcular_diferencias_adelante(
    datos,
    columna_tiempo="tiempo",
    columna_temperatura="temperatura"
):
    """
    Calcula dT/dt usando diferencias hacia adelante:

    dT/dt ≈ (T(i+1) - T(i)) / (t(i+1) - t(i))
    """

    datos = datos.copy()
    derivadas = []

    for i in range(len(datos)):
        if i == len(datos) - 1:
            derivadas.append(None)
        else:
            temp_actual = datos.loc[i, columna_temperatura]
            temp_siguiente = datos.loc[i + 1, columna_temperatura]

            tiempo_actual = datos.loc[i, columna_tiempo]
            tiempo_siguiente = datos.loc[i + 1, columna_tiempo]

            derivada = (temp_siguiente - temp_actual) / (
                tiempo_siguiente - tiempo_actual
            )

            derivadas.append(round(derivada, 4))

    datos["derivada_adelante"] = derivadas
    return datos