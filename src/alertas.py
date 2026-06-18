def generar_alertas(
    datos,
    temp_min=0,
    temp_max=4,
    variacion_advertencia=0.15,
    variacion_critica=0.30,
    variacion_emergencia=0.60,
    tiempo_estabilizacion=15
):
    datos = datos.copy()

    estados = []
    mensajes = []

    for _, fila in datos.iterrows():
        tiempo = fila["tiempo"]
        temperatura = fila["temperatura"]
        derivada = fila["derivada_centrada"]

        estado = "Estado normal"
        mensaje = "Funcionamiento normal"

        en_estabilizacion = tiempo <= tiempo_estabilizacion

        if en_estabilizacion:
            estado = "Inicializando"
            mensaje = "Cámara alcanzando temperatura objetivo"

        elif derivada is not None and temperatura > 8 and derivada > variacion_emergencia:
            estado = "Emergencia"
            mensaje = "Posible cámara apagada o corte de energía"

        elif temperatura > temp_max:
            estado = "Alerta crítica"
            mensaje = "Temperatura por encima del límite permitido"

        elif temperatura < temp_min:
            estado = "Alerta crítica"
            mensaje = "Temperatura por debajo del límite permitido"

        elif derivada is not None and derivada > variacion_critica:
            estado = "Alerta crítica"
            mensaje = "Aumento brusco de temperatura"

        elif derivada is not None and derivada > variacion_advertencia:
            estado = "Advertencia"
            mensaje = "Temperatura en aumento, se recomienda revisar la cámara"

        elif derivada is not None and derivada < -variacion_critica:
            estado = "Advertencia"
            mensaje = "Descenso brusco de temperatura"

        estados.append(estado)
        mensajes.append(mensaje)

    datos["estado"] = estados
    datos["alerta"] = mensajes

    return datos