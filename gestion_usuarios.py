import requests
import time
from bs4 import BeautifulSoup
import random
import string
from colorama import Fore, Style, init

init(autoreset=True)

# ------------------------------------------------------------
BASE = "https://www.biblioteca-cubo.com/Biblioteca-CUBO/public"
LOGIN_URL = f"{BASE}/user/loginUser"
USUARIOS_URL = f"{BASE}/admin/gestion/usuarios"
ADMIN_EMAIL = "admin2@cubo.com"
ADMIN_PASSWORD = "admin1234"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# ------------------------------------------------------------
def obtener_csrf(url):
    """Extrae token CSRF desde un formulario."""
    r = session.get(url, allow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "_token"})
    return token["value"] if token else None

def generar_usuario():
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    nombre = f"usuario_test_{sufijo}"
    correo = f"{nombre}@cubo.com"
    return nombre, correo

# ------------------------------------------------------------
def login_admin():
    print(Fore.CYAN + "1 Iniciando sesión como administrador...")
    token = obtener_csrf(LOGIN_URL)
    if not token:
        print(Fore.RED + "    No se encontró token CSRF en el formulario.")
        return False

    data = {"_token": token, "email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    r = session.post(LOGIN_URL, data=data, allow_redirects=True)

    if ("admin" in r.text.lower()) or ("/admin" in r.url):
        print(Fore.GREEN + "   Autenticación exitosa.")
        return True
    else:
        print(Fore.RED + f"   Falló el login (HTTP {r.status_code}).")
        return False

# ------------------------------------------------------------
def crear_usuario(nombre_usuario, correo):
    print(Fore.CYAN + f"\n Creando usuario: {nombre_usuario} ...")
    token = obtener_csrf(USUARIOS_URL)

    data = {
        "_token": token,
        "nombre_completo": "Usuario Temporal",
        "edad": "22",
        "sexo": "masculino",
        "nombre_usuario": nombre_usuario,
        "correo": correo,
        "rol": "cliente",
        "numero_telefono": "77777777",
        "direccion": "San Miguel",
        "password": "Test12345",
        "password_confirmation": "Test12345",
        "url_imagen": "https://via.placeholder.com/150"
    }

    r = session.post(USUARIOS_URL, data=data, allow_redirects=True)
    print(f"   -> HTTP {r.status_code} | URL final: {r.url}")

    if r.status_code in [200, 302]:
        print(Fore.GREEN + "    Usuario creado exitosamente.")
        return True
    else:
        print(Fore.RED + "  Error al crear usuario.")
        return False

# ------------------------------------------------------------
def verificar_usuario(correo):
    print(Fore.CYAN + "\n Verificando existencia del usuario en el listado (todas las páginas)...")

    for intento in range(5):
        time.sleep(2)

        # Revisar hasta 10 páginas del listado
        for page in range(1, 11):
            url = f"{USUARIOS_URL}?page={page}"
            r = session.get(url)
            if correo.lower() in r.text.lower():
                print(Fore.GREEN + f" Usuario encontrado ({correo}) en página {page}.")
                return True

        print(Fore.YELLOW + f"   ... intento {intento+1}: aún no aparece.")
    print(Fore.RED + "   Usuario no visible en el listado.")
    return False

# ------------------------------------------------------------
def obtener_id_usuario(correo):
    """Busca el ID del usuario en todas las páginas del listado."""
    for page in range(1, 11):
        r = session.get(f"{USUARIOS_URL}?page={page}")
        soup = BeautifulSoup(r.text, "html.parser")
        filas = soup.select("table tbody tr")
        for fila in filas:
            columnas = [td.get_text(strip=True).lower() for td in fila.find_all("td")]
            if len(columnas) >= 2 and correo.lower() in columnas[1].lower():
                btn = fila.find("button", {"class": "btn-edit"})
                if btn and "data-id" in btn.attrs:
                    return btn["data-id"]
    return None

# ------------------------------------------------------------
def editar_usuario(user_id, nuevo_nombre):
    print(Fore.CYAN + "\n4 Editando usuario (actualizando nombre)...")

    # 🚀 Token fresco antes de enviar PUT
    r_form = session.get(f"{USUARIOS_URL}/{user_id}")
    soup = BeautifulSoup(r_form.text, "html.parser")
    token_tag = soup.find("input", {"name": "_token"})
    token = token_tag["value"] if token_tag else obtener_csrf(USUARIOS_URL)

    data = {
        "_token": token,
        "_method": "PUT",
        "nombre_completo": nuevo_nombre,
        "edad": "22",
        "sexo": "masculino",
        "nombre_usuario": nuevo_nombre.lower(),
        "correo": f"{nuevo_nombre.lower()}@cubo.com",
        "rol": "cliente",
        "numero_telefono": "77777777",
        "direccion": "San Miguel",
        "url_imagen": "https://via.placeholder.com/150"
    }

    r = session.post(f"{USUARIOS_URL}/{user_id}", data=data)
    if r.status_code in [200, 302]:
        print(Fore.GREEN + "  Usuario editado exitosamente.")
        return True
    else:
        print(Fore.RED + f"   Error al editar (HTTP {r.status_code})")
        return False

# ------------------------------------------------------------
def eliminar_usuario(user_id):
    print(Fore.CYAN + "\n Eliminando usuario temporal...")
    token = obtener_csrf(USUARIOS_URL)
    data = {"_token": token, "_method": "DELETE"}
    r = session.post(f"{USUARIOS_URL}/{user_id}", data=data)
    if r.status_code in [200, 302]:
        print(Fore.GREEN + " Usuario eliminado correctamente.")
        return True
    else:
        print(Fore.RED + f"   Error al eliminar (HTTP {r.status_code}).")
        return False

# ------------------------------------------------------------
def main():
    print("------------------------------------------------------------")
    print("PRUEBA FUNCIONAL: GESTIÓN DE USUARIOS (CUBO ADMIN)")
    print("------------------------------------------------------------")

    errores = 0

    if not login_admin():
        print(Fore.RED + " Abortando prueba.")
        return

    nombre_usuario, correo = generar_usuario()

    if not crear_usuario(nombre_usuario, correo):
        errores += 1
    elif not verificar_usuario(correo):
        errores += 1
    else:
        user_id = obtener_id_usuario(correo)
        if user_id:
            nuevo_nombre = nombre_usuario.replace("test", "editado")
            if not editar_usuario(user_id, nuevo_nombre):
                errores += 1
            if not eliminar_usuario(user_id):
                errores += 1
        else:
            print(Fore.RED + " No se pudo obtener el ID del usuario.")
            errores += 1

    print("\n------------------------------------------------------------")
    print(Fore.CYAN + f"ERRORES DETECTADOS: {errores}")
    if errores == 0:
        print(Fore.GREEN + "RESULTADO FINAL: TODO CORRECTO – CRUD COMPLETO FUNCIONAL.")
    else:
        print(Fore.YELLOW + "RESULTADO FINAL: Se detectaron fallas en el flujo del módulo.")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    main()
