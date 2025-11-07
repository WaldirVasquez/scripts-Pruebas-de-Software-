import requests
import unittest
from bs4 import BeautifulSoup

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE_URL}/user/loginUser"
USUARIOS_URL = f"{BASE_URL}/admin/gestion/usuarios"

class TestIntegracionGestionUsuarios(unittest.TestCase):
    def setUp(self):
        """Configura sesión persistente para autenticación."""
        self.session = requests.Session()
        self.resultado_final = "Prueba no completada."
        print("\n=== INICIO DE PRUEBA DE INTEGRACIÓN: GESTIÓN DE USUARIOS ===")

    def get_csrf_token(self):
        """Obtiene el token CSRF desde el formulario de login."""
        r = self.session.get(LOGIN_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        return token_tag["value"] if token_tag else None

    def login_admin(self):
        """Inicia sesión como administrador."""
        token = self.get_csrf_token()
        data = {
            "_token": token,
            "email": "admin2@cubo.com",
            "password": "admin1234"
        }
        r = self.session.post(LOGIN_URL, data=data, allow_redirects=False)
        return r.status_code in (302, 303)

    def test_gestion_usuarios(self):
        """Evalúa el acceso y contenido del módulo Gestión de Usuarios."""
        login_exitoso = self.login_admin()
        self.assertTrue(login_exitoso, "No se pudo iniciar sesión correctamente.")

        # Acceder al módulo de Gestión de Usuarios
        response = self.session.get(USUARIOS_URL)
        html = response.text.lower()

        print(f"→ Código de respuesta: {response.status_code}")

        # Verificar que la página se cargue correctamente
        if response.status_code == 200 and any(palabra in html for palabra in ["usuarios", "agregar", "editar"]):
            print("El módulo de Gestión de Usuarios cargó correctamente.")
            self.resultado_final = "Acceso exitoso al módulo de Gestión de Usuarios."
        elif response.status_code == 403:
            print("Acceso denegado. El usuario no tiene permisos.")
            self.resultado_final = "Error: Acceso prohibido (403)."
        elif response.status_code == 500:
            print("Error interno del servidor al cargar el módulo.")
            self.resultado_final = "Error: Fallo interno del servidor (500)."
        else:
            print("Comportamiento inesperado o contenido no detectado.")
            self.resultado_final = "Revisión requerida: posible error de vista o permisos."

        print("=== FIN DE PRUEBA DE INTEGRACIÓN: GESTIÓN DE USUARIOS ===")

    def tearDown(self):
        print(f"Resultado final: {self.resultado_final}\n")

if __name__ == "__main__":
    unittest.main(verbosity=0)
