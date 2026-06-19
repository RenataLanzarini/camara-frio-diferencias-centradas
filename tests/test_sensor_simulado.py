import unittest

from src.sensor_simulado import generar_lecturas_sensor


class TestSensorSimulado(unittest.TestCase):
    def test_misma_semilla_repite_resultados(self):
        primera = generar_lecturas_sensor(escenario="puerta_abierta", semilla=123)
        segunda = generar_lecturas_sensor(escenario="puerta_abierta", semilla=123)

        self.assertTrue(primera.equals(segunda))

    def test_distinta_semilla_cambia_resultados(self):
        primera = generar_lecturas_sensor(escenario="puerta_abierta", semilla=123)
        segunda = generar_lecturas_sensor(escenario="puerta_abierta", semilla=456)

        self.assertFalse(primera.equals(segunda))


if __name__ == "__main__":
    unittest.main()
