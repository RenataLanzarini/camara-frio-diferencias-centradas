import tempfile
import unittest
from pathlib import Path

import app


class TestPersistenciaCamaras(unittest.TestCase):
    def setUp(self):
        self.archivo_original = app.ARCHIVO_CAMARAS
        self.temporal = tempfile.TemporaryDirectory()
        app.ARCHIVO_CAMARAS = str(Path(self.temporal.name) / "camaras.json")

    def tearDown(self):
        app.ARCHIVO_CAMARAS = self.archivo_original
        self.temporal.cleanup()

    def test_agregar_y_eliminar_camara(self):
        creada, _ = app.agregar_camara({
            "id": "cam-99",
            "nombre": "Camara prueba",
            "producto": "Producto prueba",
            "ubicacion": "Sector prueba",
            "destinatarios": [],
        })

        self.assertTrue(creada)
        self.assertIn("CAM-99", [camara["id"] for camara in app.leer_camaras()])

        eliminada, _ = app.eliminar_camara_por_id("CAM-99")

        self.assertTrue(eliminada)
        self.assertNotIn("CAM-99", [camara["id"] for camara in app.leer_camaras()])

    def test_destinatarios_por_camara(self):
        app.agregar_camara({
            "id": "CAM-88",
            "nombre": "Camara con mail",
            "producto": "Producto",
            "ubicacion": "Sector",
            "destinatarios": [],
        })

        agregado, _ = app.agregar_destinatario_camara("CAM-88", "Responsable@Ejemplo.com")
        camara = app.obtener_camara("CAM-88")

        self.assertTrue(agregado)
        self.assertEqual(camara["destinatarios"], ["responsable@ejemplo.com"])

        eliminado, _ = app.eliminar_destinatario_camara("CAM-88", "responsable@ejemplo.com")
        camara = app.obtener_camara("CAM-88")

        self.assertTrue(eliminado)
        self.assertEqual(camara["destinatarios"], [])

    def test_mail_unico_asignado_a_varias_camaras(self):
        app.agregar_camara({
            "id": "CAM-77",
            "nombre": "Camara A",
            "producto": "Producto A",
            "ubicacion": "Sector A",
            "destinatarios": [],
        })
        app.agregar_camara({
            "id": "CAM-78",
            "nombre": "Camara B",
            "producto": "Producto B",
            "ubicacion": "Sector B",
            "destinatarios": [],
        })

        asignado, _ = app.asignar_destinatario_a_camaras(
            "Responsable@Ejemplo.com",
            ["CAM-77", "CAM-78"],
        )
        mails = app.obtener_mails_con_camaras()

        self.assertTrue(asignado)
        self.assertEqual(len(mails), 1)
        self.assertEqual(mails[0]["email"], "responsable@ejemplo.com")
        self.assertEqual(mails[0]["camaras"], ["CAM-77", "CAM-78"])

    def test_reporte_requiere_mail_seleccionado(self):
        cliente = app.app.test_client()

        respuesta = cliente.post("/reporte", data={
            "modo": "demo",
            "escenario": "normal",
            "camaras_reporte": ["CAM-01"],
        })

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "Debe seleccionar al menos un mail",
            respuesta.data.decode("utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
