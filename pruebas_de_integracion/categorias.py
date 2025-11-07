import requests
import unittest
import time
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# CONFIGURACIÓN BASE DEL SISTEMA
# ------------------------------------------------------------
BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE_URL}/user/loginUser"
CATEGORIAS_URL = f"{BASE_URL}/admin/gestion/categorias"

ADMIN_EMAIL = "admin2@cubo.com"
ADMIN_PASSWORD = "admin1234"

# ------------------------------------------------------------
class TestIntegracionGestionCategorias(unittest.TestCase):
    def setUp(self):
        """Inicia sesión de prueba y mantiene cookies activas."""
        self.session = requests.Session()
        self.resultado_final = "Prueba no completada."
        print("\n=== INICIO DE PRUEBA DE INTEGRACIÓN: GESTIÓN DE CATEGORÍAS ===")

    # ------------------------------------------------------------
    def obtener_csrf(self, url):
        """Obtiene el token CSRF del formulario de login."""
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {"name": "_token"})
        return token["value"] if token else None

    # ------------------------------------------------------------
    def login_admin(self):
        """Inicia sesión como administrador y confirma autenticación."""
        token = self.obtener_csrf(LOGIN_URL)
        if not token:
            print("No se encontró token CSRF en el formulario de login.")
            return False

        data = {"_token": token, "email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        r = self.session.post(LOGIN_URL, data=data, allow_redirects=False)

        if r.status_code in (302, 303):
            print("Sesión iniciada correctamente (HTTP 302/303).")
            return True
        else:
            print(f"Error al iniciar sesión. Código HTTP: {r.status_code}")
            return False

    # ------------------------------------------------------------
    def test_integracion_gestion_categorias(self):
        """Verifica la carga y respuesta del módulo Gestión de Categorías."""
        login_ok = self.login_admin()
        self.assertTrue(login_ok, "No se pudo iniciar sesión correctamente.")

        # Primer acceso al módulo
        print("\n→ Accediendo al módulo de Gestión de Categorías...")
        response = self.session.get(CATEGORIAS_URL)
        html = response.text.lower()
        codigo = response.status_code

        print(f"→ Código de respuesta: {codigo}")

        # Validación principal
        if codigo == 200 and any(palabra in html for palabra in ["categorías", "agregar", "editar"]):
            print("El módulo cargó correctamente (vista renderizada sin errores).")
            self.resultado_final = "Acceso exitoso al módulo de Gestión de Categorías."
        elif codigo == 403:
            print("Acceso denegado. Posible error de permisos o middleware.")
            self.resultado_final = "Error: Acceso prohibido (403)."
        elif codigo == 500:
            print("Error interno del servidor al cargar el módulo.")
            self.resultado_final = "Error: Fallo interno del servidor (500)."
        else:
            print("Comportamiento inesperado o contenido no detectado en la vista.")
            self.resultado_final = "Revisión requerida: posible fallo de integración."

        # Segunda verificación (estabilidad del módulo)
        print("\n→ Verificación de estabilidad del módulo...")
        time.sleep(2)
        response2 = self.session.get(CATEGORIAS_URL)
        if response2.status_code == 200:
            print("El módulo responde de forma estable en una segunda solicitud.")
        else:
            print(f"Código inesperado en segunda carga: {response2.status_code}")

        print("\n=== FIN DE PRUEBA DE INTEGRACIÓN: GESTIÓN DE CATEGORÍAS ===")

    # ------------------------------------------------------------
    def tearDown(self):
        print(f"Resultado final: {self.resultado_final}\n")

# ------------------------------------------------------------
if __name__ == "__main__":
    unittest.main(verbosity=0)
