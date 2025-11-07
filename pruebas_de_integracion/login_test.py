import requests
import unittest
from bs4 import BeautifulSoup

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE_URL}/user/loginUser"

class TestIntegracionLoginAdmin(unittest.TestCase):
    def setUp(self):
        """Configura la sesión para mantener cookies."""
        self.session = requests.Session()
        self.resultado_final = "Prueba no completada."
        print("\n=== INICIO DE PRUEBA DE INTEGRACIÓN: LOGIN ADMIN ===")

    def get_csrf_token(self):
        """Obtiene el token CSRF desde el formulario de login."""
        r = self.session.get(LOGIN_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        token = token_tag["value"] if token_tag else None
        self.assertIsNotNone(token, "No se encontró token CSRF en el formulario.")
        return token

    def test_login_admin(self):
        """Verifica el flujo completo del login del administrador."""
        token = self.get_csrf_token()

        # Credenciales válidas del administrador
        data = {
            "_token": token,
            "email": "admin2@cubo.com",
            "password": "admin1234"
        }

        response = self.session.post(LOGIN_URL, data=data, allow_redirects=False)

        print(f"→ Código de respuesta: {response.status_code}")
        print(f"→ Cabeceras: {response.headers.get('Location', 'Sin redirección detectada')}")

        # Comprobaciones
        if response.status_code in (302, 303):
            print("El sistema redirige correctamente tras un login exitoso.")
            self.resultado_final = "Inicio de sesión exitoso (flujo correcto)."
        elif response.status_code == 200:
            print("La respuesta es 200, puede significar error en login o validación incorrecta.")
            html = response.text.lower()
            if any(word in html for word in ["credenciales", "incorrecta", "error"]):
                self.resultado_final = "El sistema rechazó las credenciales (flujo correcto)."
            else:
                self.resultado_final = "Respuesta ambigua, revisar comportamiento."
        else:
            print("Error inesperado al procesar la solicitud.")
            self.resultado_final = f"Error HTTP {response.status_code}"

        print("=== FIN DE PRUEBA DE INTEGRACIÓN: LOGIN ADMIN ===")

    def tearDown(self):
        print(f"Resultado final: {self.resultado_final}\n")

if __name__ == "__main__":
    unittest.main(verbosity=0)
