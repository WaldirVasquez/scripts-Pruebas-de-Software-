import unittest
import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE_URL}/user/loginUser"
USUARIOS_URL = f"{BASE_URL}/admin/gestion/usuarios"

ADMIN_EMAIL = "admin2@cubo.com"
ADMIN_PASSWORD = "admin1234"

class TestUsabilidadGestionUsuarios(unittest.TestCase):

    def setUp(self):
        self.session = requests.Session()
        self.resultado_final = "Prueba no completada."
        print("\n=== INICIO DE PRUEBA DE USABILIDAD: GESTIÓN DE USUARIOS (ADMIN) ===")

    def obtener_csrf(self):
        """Obtiene el token CSRF del formulario de login."""
        r = self.session.get(LOGIN_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {"name": "_token"})
        return token["value"] if token else None

    def login_admin(self):
        """Inicia sesión como administrador."""
        token = self.obtener_csrf()
        if not token:
            print("No se encontró token CSRF.")
            return False
        data = {"_token": token, "email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        r = self.session.post(LOGIN_URL, data=data, allow_redirects=False)
        return r.status_code in (302, 303)

    def test_usabilidad_gestion_usuarios(self):
        """Evalúa la carga, visibilidad y claridad de la interfaz de Gestión de Usuarios."""
        inicio = time.time()
        login_exitoso = self.login_admin()
        self.assertTrue(login_exitoso, "No se pudo iniciar sesión correctamente.")

        response = self.session.get(USUARIOS_URL)
        fin = time.time()
        tiempo_carga = round(fin - inicio, 2)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        print(f"→ Código HTTP: {response.status_code}")
        print(f"→ Tiempo total de carga (login + vista): {tiempo_carga} segundos")

        # Elementos visuales esperados
        encabezado = soup.find(["h1", "h2", "h3"])
        tabla = soup.find("table")
        botones = soup.find_all("button")
        enlaces = soup.find_all("a")

        # Evaluación de accesibilidad
        if response.status_code == 200:
            print("Página accesible: Sí (HTTP 200)")
        else:
            print("Página accesible: No")

        # Evaluación de visibilidad de componentes principales
        if encabezado and tabla:
            print("Estructura visual: Encabezado y tabla de usuarios visibles.")
        else:
            print("Estructura visual: Elementos principales no encontrados.")

        # Evaluación de botones y acciones visibles
        if any("agregar" in b.text.lower() or "editar" in b.text.lower() for b in botones):
            print("Botones de acción visibles: Sí (Agregar/Editar detectados).")
        else:
            print("Botones de acción visibles: No detectados.")

        # Evaluación de rendimiento
        if tiempo_carga <= 6:
            print("Rendimiento: Aceptable (≤ 6s).")
        else:
            print("Rendimiento: Lento (> 6s).")

        # Evaluación de claridad textual
        etiquetas_clave = ["usuarios", "agregar", "editar", "correo", "rol"]
        legibilidad = sum(1 for palabra in etiquetas_clave if palabra in html.lower())
        if legibilidad >= 3:
            print("Textos y etiquetas comprensibles: Sí.")
        else:
            print("Textos y etiquetas comprensibles: Deficiencia en el contenido textual.")

        # Resultado general
        if response.status_code == 200 and encabezado and tabla and tiempo_carga <= 6:
            self.resultado_final = "Interfaz de gestión de usuarios accesible y funcional."
        else:
            self.resultado_final = "La interfaz presenta deficiencias de usabilidad."

        print("=== FIN DE PRUEBA DE USABILIDAD: GESTIÓN DE USUARIOS (ADMIN) ===")

    def tearDown(self):
        print(f"Resultado final: {self.resultado_final}\n")

if __name__ == "__main__":
    unittest.main(verbosity=0)
