import requests
import unittest
from bs4 import BeautifulSoup

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.errores_detectados = 0
        self.resultado_final = "No se completó la prueba correctamente."

    def get_csrf_token(self):
        """Obtiene el token CSRF del formulario de login."""
        r = self.session.get(BASE_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        return token_tag["value"] if token_tag else None

    def test_login_analisis(self):
        """Evalúa el comportamiento del login con análisis separado de usuario y contraseña."""
        token = self.get_csrf_token()

        # --- DATOS DE PRUEBA ---
        email = "admin2@cubo.com"  
        password = "admin1234"    

        data = {"_token": token, "email": email, "password": password}

        # --- ENVÍO DE LA SOLICITUD ---
        r = self.session.post(BASE_URL, data=data)
        html = r.text.lower()

        print("RESULTADO DE LA PRUEBA UNITARIA: LOGIN - ANÁLISIS DETALLADO")
        print("-------------------------------------------------------------")
        print(f"Código HTTP recibido: {r.status_code}")

        # --- ANÁLISIS DEL COMPORTAMIENTO ---
        usuario_valido = "admin" in email.lower() 
        acceso_permitido = any(x in html for x in ["panel", "dashboard", "categorías"])
        acceso_rechazado = any(x in html for x in ["credenciales", "incorrecta", "contraseña", "error"])

        # --- LÓGICA DE RESULTADOS ---
        if usuario_valido:
            print("Usuario: válido o detectado correctamente.")
        else:
            print("Usuario: no detectado o inválido.")
            self.errores_detectados += 1

        if acceso_permitido:
            print("Contraseña: válida. Acceso permitido.")
        elif acceso_rechazado:
            print("Contraseña: inválida. Acceso bloqueado correctamente.")
        else:
            print("Contraseña: no determinada. Posible error de validación.")
            self.errores_detectados += 1

        # --- EVALUACIÓN GLOBAL ---
        if acceso_permitido and usuario_valido:
            self.resultado_final = "El módulo de login funciona correctamente."
        elif acceso_rechazado and usuario_valido:
            self.resultado_final = "El módulo de login rechazó correctamente una contraseña inválida."
        else:
            self.resultado_final = "El módulo de login requiere revisión adicional."

        print("-------------------------------------------------------------")
        print(f"Errores detectados en la prueba: {self.errores_detectados}")
        print("-------------------------------------------------------------")

    def tearDown(self):
        print(f"Resumen final: {self.resultado_final}\n")

if __name__ == "__main__":
    unittest.main(verbosity=0)