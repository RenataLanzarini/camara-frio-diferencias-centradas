# Validacion del metodo numerico

## Metodo principal

El proyecto utiliza el Metodo de Diferencias Centradas para aproximar la derivada de la temperatura respecto del tiempo.

La derivada representa la velocidad de cambio de la temperatura:

```text
dT/dt ~= (T(i+1) - T(i-1)) / (t(i+1) - t(i-1))
```

Si las mediciones estan tomadas con un intervalo constante `h`, la expresion equivalente es:

```text
dT/dt ~= (T(i+1) - T(i-1)) / (2h)
```

## Interpretacion fisica

- Derivada positiva: la temperatura aumenta.
- Derivada negativa: la temperatura disminuye.
- Derivada cercana a cero: la temperatura permanece estable.

En el contexto de una camara frigorifica, esta informacion permite detectar tendencias antes de que la temperatura llegue a valores peligrosos.

## Tratamiento de extremos

El primer y ultimo punto de la serie no tienen derivada centrada porque el metodo necesita una medicion anterior y una posterior al punto analizado.

Por este motivo:

- En el primer punto no existe `T(i-1)`.
- En el ultimo punto no existe `T(i+1)`.
- Ambos valores se marcan como no calculables.

## Comparacion con Diferencias Hacia Adelante

El proyecto tambien calcula Diferencias Hacia Adelante:

```text
dT/dt ~= (T(i+1) - T(i)) / (t(i+1) - t(i))
```

Este metodo es mas simple, pero usa solo el punto actual y el punto siguiente. Diferencias Centradas utiliza informacion de ambos lados del punto analizado y por eso ofrece una mejor representacion de la tendencia local.

## Validaciones incorporadas

- El calculo usa posiciones reales de la tabla, por lo que no depende de que el indice del DataFrame empiece en cero.
- El sistema valida que no existan intervalos de tiempo iguales antes de dividir.
- Si dos mediciones tienen el mismo tiempo, se informa un error porque la derivada no puede calcularse con denominador cero.
