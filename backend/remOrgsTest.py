import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
PERMISOS = {"fullType": "EXTRA"}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Prueba para listar roles
def test_listado_organizaciones():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/organizations-remote", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La response no contiene la clave 'message'"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listado_roles: Prueba fallida - {e}")

# Prueba para crear un rol
@pytest.fixture(scope="module")
def crear_organizacion():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        datos_rol = {"name": "OP", "descritpion": "Organización de Prueba", "client_id": 3}
        response = requests.post(f"{URL_BASE}/organizations-remote", json=datos_rol, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "data" in datos, "La respuesta no contiene el ID del rol creado"
        print(f"Rol creado con ID: {datos['data']}")
        return datos["data"]
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_rol: Prueba fallida - {e}")

# Prueba para listar un rol en específico
def test_llamar_organizacion(crear_organizacion):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"fullType": "DET", "client_id": 3, "searchBy": crear_organizacion}
        response = requests.get(f"{URL_BASE}/roles-remote", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        info = datos['data']
        assert "message" in datos, "La response no contiene la clave 'message'"
        print(json.dumps(info, indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_roles: Prueba fallida - {e}")

# Prueba para editar un rol
def test_editar_organizacion(crear_organizacion):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        datos_edicion = {"name": "ODP", "client_id": 3}
        response = requests.put(f"{URL_BASE}/organizations-remote/{crear_organizacion}", json=datos_edicion, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos["message"] == "Registro actualizado con éxito", f"El mensaje de respuesta es: {datos['message']}"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_rol: Prueba fallida - {e}")

# Prueba para eliminar un rol
def test_eliminar_organizacion(crear_organizacion):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 3}
        response = requests.delete(f"{URL_BASE}/organizations-remote/{crear_organizacion}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos["message"] == "Registro eliminado con éxito", f"El mensaje de respuesta es: {datos['message']}"
        print(f"Rol eliminado con éxito")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_rol: Prueba fallida - {e}")