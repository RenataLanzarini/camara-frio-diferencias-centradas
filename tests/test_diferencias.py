import unittest

import pandas as pd

from src.diferencias_centradas import (
    calcular_diferencias_adelante,
    calcular_diferencias_centradas,
)


class TestDiferenciasNumericas(unittest.TestCase):
    def test_diferencias_centradas_en_serie_lineal(self):
        datos = pd.DataFrame({
            "tiempo": [0, 5, 10, 15],
            "temperatura": [2, 4, 6, 8],
        })

        resultado = calcular_diferencias_centradas(datos)

        self.assertTrue(pd.isna(resultado.loc[0, "derivada_centrada"]))
        self.assertEqual(resultado.loc[1, "derivada_centrada"], 0.4)
        self.assertEqual(resultado.loc[2, "derivada_centrada"], 0.4)
        self.assertTrue(pd.isna(resultado.loc[3, "derivada_centrada"]))

    def test_diferencias_adelante_en_serie_lineal(self):
        datos = pd.DataFrame({
            "tiempo": [0, 5, 10, 15],
            "temperatura": [2, 4, 6, 8],
        })

        resultado = calcular_diferencias_adelante(datos)

        self.assertEqual(resultado.loc[0, "derivada_adelante"], 0.4)
        self.assertEqual(resultado.loc[1, "derivada_adelante"], 0.4)
        self.assertEqual(resultado.loc[2, "derivada_adelante"], 0.4)
        self.assertTrue(pd.isna(resultado.loc[3, "derivada_adelante"]))

    def test_tiempos_repetidos_generan_error(self):
        datos = pd.DataFrame({
            "tiempo": [0, 0, 10],
            "temperatura": [2, 3, 4],
        })

        with self.assertRaises(ValueError):
            calcular_diferencias_adelante(datos)


if __name__ == "__main__":
    unittest.main()
