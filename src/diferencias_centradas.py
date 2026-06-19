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
            temp_siguiente = datos.iloc[i + 1][columna_temperatura]
            temp_anterior = datos.iloc[i - 1][columna_temperatura]

            tiempo_siguiente = datos.iloc[i + 1][columna_tiempo]
            tiempo_anterior = datos.iloc[i - 1][columna_tiempo]
            intervalo = tiempo_siguiente - tiempo_anterior

            if intervalo == 0:
                raise ValueError("No se puede calcular la derivada con tiempos repetidos.")

            derivada = (temp_siguiente - temp_anterior) / intervalo

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
            temp_actual = datos.iloc[i][columna_temperatura]
            temp_siguiente = datos.iloc[i + 1][columna_temperatura]

            tiempo_actual = datos.iloc[i][columna_tiempo]
            tiempo_siguiente = datos.iloc[i + 1][columna_tiempo]
            intervalo = tiempo_siguiente - tiempo_actual

            if intervalo == 0:
                raise ValueError("No se puede calcular la derivada con tiempos repetidos.")

            derivada = (temp_siguiente - temp_actual) / intervalo

            derivadas.append(round(derivada, 4))

    datos["derivada_adelante"] = derivadas
    return datos
