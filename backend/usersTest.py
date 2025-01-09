import pytest
import requests
from faker import Faker

fake = Faker()

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
USUARIO_A_CREAR = {
    "name": fake.first_name(),
    "middle_name": "",
    "last_name": fake.last_name(),
    "mother_last_name": "",
    "phone": fake.numerify("########"),
    "email": f"{fake.user_name()}@fos.com.bo",
    "password": fake.password(length=10),
    "role_id": 28
}
COSAS_A_EDITAR = {"middle_name": "TestEditor"}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "87654321"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

#Prueba para listar a los usuarios
def test_listar_usuarios():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/users", headers=headers, params=LISTADO)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave'message'"
        print("El GET funciona correctamente")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_usuarios: Prueba fallida - {e}")

@pytest.fixture(scope="module")
def crear_usuario():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/users", json=USUARIO_A_CREAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        #assert 'data' in datos, "La respuesta no contiene el ID del usuario creado"
        assert datos['message'] == "Registro creado con éxito", "El usuario falló al crearse"
        print(f"Usuario creado con ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_usuario: Prueba fallida - {e}")

#Prueba para llamar a un usuario específico
def test_llamar_usuario(crear_usuario):
    try:
        token = obtenerToken()
        params = {"fullType": "L", "searchBy": crear_usuario}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/users", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave'message'"
        print(f"{datos['data']}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_usuario: Prueba fallida - {e}")

#Prueba para editar a un usuario
def editar_create(crear_usuario):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/users/{crear_usuario}", json=COSAS_A_EDITAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar el usuario"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_usuario: Prueba fallida - {e}")

#Prueba para eliminar un usuario
def test_eliminar_usuario(crear_usuario):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/users/{crear_usuario}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Administrador Desvinculado", "El usuario falló al ser eliminado"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_usuario: Prueba fallida - {e}")