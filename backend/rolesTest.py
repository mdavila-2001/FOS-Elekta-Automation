import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"

#Datos necesarios
LISTADO = {"fullType": "L"}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Prueba para crear un rol
def crear_rol():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        datos_rol = {"abilities": "home:R|profile:C|roles:R|", "description": "Rol de prueba", "level": 2, "name": "rpureba"}
        response = requests.post(f"{URL_BASE}/roles", json=datos_rol, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "data" in datos, "La respuesta no contiene el ID del rol creado"
        print(f"Rol creado con ID: {datos['data']}")
        return datos["data"]
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_rol: Prueba fallida - {e}")

# Prueba para listar roles
def test_listado_roles():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/roles", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La response no contiene la clave 'message'"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listado_roles: Prueba fallida - {e}")

# Prueba para editar un rol
def test_editar_rol():
    try:
        token = obtenerToken()
        rol_id = crear_rol()
        headers = {"Authorization": f"Bearer {token}"}
        datos_edicion = {"description": "Prueba de Edicion"}
        response = requests.put(f"{URL_BASE}/roles/{rol_id}", json=datos_edicion, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "Debug_Querys" in datos, "La response no contiene la clave'Debug_Querys'"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_rol: Prueba fallida - {e}")

# Prueba para eliminar un rol
def test_eliminar_rol():
    try:
        token = obtenerToken()
        rol_id = crear_rol()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/roles/{rol_id}", headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_rol: Prueba fallida - {e}")