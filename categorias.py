import requests
import time
import random
import string
from bs4 import BeautifulSoup
from colorama import Fore, init

# Inicializar color en consola
init(autoreset=True)

# ------------------------------------------------------------
BASE = "https://www.biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE}/user/loginUser"
CATEGORIAS_URL = f"{BASE}/admin/gestion/categorias"

# Credenciales del admin real
ADMIN_EMAIL = "admin2@cubo.com"
ADMIN_PASSWORD = "admin1234"

# Crear sesión persistente
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

# ------------------------------------------------------------
def obtener_csrf(url):
    """Extrae el token CSRF del formulario HTML."""
    r = session.get(url, allow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "_token"})
    return token["value"] if token else None

def generar_categoria():
    """Crea un nombre de categoría único para prueba."""
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"categoria_test_{sufijo}"

# ------------------------------------------------------------
def login_admin():
    print(Fore.CYAN + " Iniciando sesión como administrador...")
    token = obtener_csrf(LOGIN_URL)
    if not token:
        print(Fore.RED + "  No se encontró token CSRF en el formulario.")
        return False

    data = {"_token": token, "email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    r = session.post(LOGIN_URL, data=data, allow_redirects=True)

    if ("admin" in r.text.lower()) or ("/admin" in r.url):
        print(Fore.GREEN + "  Autenticación exitosa.")
        return True
    else:
        print(Fore.RED + f" Falló el login (HTTP {r.status_code}).")
        return False

# ------------------------------------------------------------
def crear_categoria(nombre):
    print(Fore.CYAN + f"\n Creando categoría: {nombre} ...")
    token = obtener_csrf(CATEGORIAS_URL)
    if not token:
        print(Fore.RED + "  No se pudo obtener token CSRF.")
        return False

    data = {
        "_token": token,
        "nombre": nombre,
        "estado": "habilitado"
    }

    r = session.post(CATEGORIAS_URL, data=data, allow_redirects=True)
    print(f"   -> HTTP {r.status_code} | URL final: {r.url}")

    if "Categoría agregada exitosamente" in r.text or r.status_code in [200, 302]:
        print(Fore.GREEN + "  Categoría creada exitosamente.")
        return True
    else:
        print(Fore.RED + "  Error al crear categoría.")
        return False

# ------------------------------------------------------------
def verificar_categoria(nombre):
    print(Fore.CYAN + "\n Verificando existencia en el listado...")

    for intento in range(5):
        time.sleep(2)
        for page in range(1, 6):
            url = f"{CATEGORIAS_URL}?page={page}"
            r = session.get(url)
            if nombre.lower() in r.text.lower():
                print(Fore.GREEN + f"  Categoría encontrada ({nombre}) en página {page}.")
                return True
        print(Fore.YELLOW + f"   ... intento {intento+1}: aún no aparece.")

    print(Fore.RED + "  Categoría no visible en el listado.")
    return False

# ------------------------------------------------------------
def main():
    print("------------------------------------------------------------")
    print("PRUEBA FUNCIONAL: GESTIÓN DE CATEGORÍAS (CUBO ADMIN)")
    print("------------------------------------------------------------")

    errores = 0

    if not login_admin():
        print(Fore.RED + " Abortando prueba.")
        return

    nombre_categoria = generar_categoria()

    if not crear_categoria(nombre_categoria):
        errores += 1
    elif not verificar_categoria(nombre_categoria):
        errores += 1

    print("\n------------------------------------------------------------")
    print(Fore.CYAN + f"ERRORES DETECTADOS: {errores}")
    if errores == 0:
        print(Fore.GREEN + "RESULTADO FINAL:  TODO CORRECTO – CREACIÓN FUNCIONAL.")
    else:
        print(Fore.YELLOW + "RESULTADO FINAL:  Se detectaron fallas en el flujo.")
    print("------------------------------------------------------------")

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
