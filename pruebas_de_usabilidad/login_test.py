import unittest
import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE_URL}/user/loginUser"

class TestUsabilidadLoginAdmin(unittest.TestCase):

    def setUp(self):
        self.session = requests.Session()
        self.resultado_final = "Prueba no completada."
        print("\n=== INICIO DE PRUEBA DE USABILIDAD: LOGIN ADMINISTRADOR ===")

    def test_usabilidad_login(self):
        """Evalúa la accesibilidad, tiempos de carga y claridad de la interfaz de inicio de sesión."""
        inicio = time.time()
        response = self.session.get(LOGIN_URL)
        fin = time.time()

        tiempo_carga = round(fin - inicio, 2)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        print(f"→ Código HTTP: {response.status_code}")
        print(f"→ Tiempo de carga: {tiempo_carga} segundos")

        campos = {
            "email": soup.find("input", {"name": "email"}),
            "password": soup.find("input", {"name": "password"}),
            "boton": soup.find("button")
        }

        # Evaluación de visibilidad y accesibilidad
        if response.status_code == 200:
            print("Página accesible: Sí (HTTP 200)")
        else:
            print("Página accesible: No (error de carga)")

        if all(campos.values()):
            print("Campos esenciales visibles: Sí (correo, contraseña, botón).")
        else:
            print("Campos esenciales visibles: No (falta un elemento).")

        # Evaluación de tiempos de carga
        if tiempo_carga <= 5:
            print("Rendimiento: Aceptable (≤ 5s).")
        else:
            print("Rendimiento: Lento (> 5s).")

        # Evaluación del contenido visual
        elementos_texto = ["correo", "contraseña", "iniciar sesión", "admin"]
        contenido_legible = sum(1 for palabra in elementos_texto if palabra in html.lower())
        if contenido_legible >= 3:
            print("Textos y etiquetas comprensibles: Sí.")
        else:
            print("Textos y etiquetas comprensibles: Poca claridad.")

        # Resultado general
        if response.status_code == 200 and all(campos.values()) and tiempo_carga <= 5:
            self.resultado_final = "Interfaz de login funcional y accesible."
        else:
            self.resultado_final = "La interfaz presenta deficiencias de usabilidad."

        print("=== FIN DE PRUEBA DE USABILIDAD: LOGIN ADMINISTRADOR ===")

    def tearDown(self):
        print(f"Resultado final: {self.resultado_final}\n")

if __name__ == "__main__":
    unittest.main(verbosity=0)
