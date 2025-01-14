import json
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"

#Datos necesarios
LISTADO = {"fullType": "L"}
USUARIO_A_CREAR = {
    "ci": str(fake.unique.random_number(digits=8)),
    "name": fake.first_name(),
    "middle_name": fake.first_name(),
    "last_name": fake.last_name(),
    "mother_last_name": fake.last_name(),
    "email": f"{fake.unique.user_name()}@fos.com.bo",
    "password": fake.password(length=10),
    "phone": fake.random_element(elements=("6", "7"))+str(fake.random_number(digits=6)),
    "address": fake.address(),
    "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d"),
    "gender": fake.random_element(elements=("M", "F")),
    "emergency_contact": fake.name(),
    "emergency_phone": fake.random_element(elements=("6", "7"))+str(fake.random_number(digits=8)),
    "role_id": 2
}
USUARIO_ERROR = {
    "ci": str(fake.unique.random_number(digits=8)),
    "name": fake.first_name(),
    "last_name": fake.last_name(),
    "middle_name": fake.first_name(),
    "mother_last_name": fake.last_name(),
    "email": f"{fake.email()}",
    "password": fake.password(length=10),
    "phone": fake.random_element(elements=("6", "7"))+str(fake.random_number(digits=6)),
    "address": fake.address(),
    "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d"),
    "gender": fake.random_element(elements=("M", "F")),
    "emergency_contact": fake.name(),
    "emergency_phone": fake.random_element(elements=("6", "7"))+str(fake.random_number(digits=8)),
    "role_id": 2
}
COSAS_A_EDITAR = {"middle_name": "EditTest"}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def obtenerTokenEliminacion():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "support@fos.com.bo", "password": "12345678"})
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
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print("El GET funciona correctamente")
        print(json.dumps(datos['data'], indent=4))
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
        assert datos['message'] == "Registro creado con éxito", "El usuario falló al crearse"
        print(f"Usuario creado con ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_usuario: Prueba fallida - {e}")

def test_crear_usuario_erroneo():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/users", json=USUARIO_ERROR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "El correo debe tener el dominio @fos.com.bo", "El usuario falló al crearse"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_usuario: Prueba fallida - {e}")

#Prueba para llamar a un usuario específico
def test_llamar_usuario(crear_usuario):
    try:
        token = obtenerToken()
        params = {"fullType": "DET", "searchBy": crear_usuario}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_BASE}/users", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert "data" in datos, "La respuesta no pudo traer los datos del usuario"
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_usuario: Prueba fallida - {e}")

#Prueba para editar a un usuario
def test_editar_usuario(crear_usuario):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_BASE}/users/{crear_usuario}", json=COSAS_A_EDITAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar el usuario"
        print(json.dumps(datos['Debug_Querys'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_usuario: Prueba fallida - {e}")

#Prueba para solicitar eliminación de un usuario
def test_solicitar_eliminacion(crear_usuario):
    try:
        token = obtenerToken()
        params = {"searchBy": crear_usuario, "description": "Prueba para eliminar el usuario creado"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{URL_BASE}/adm-deletion", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Solicitud de eliminación enviada", "El usuario falló al ser eliminado"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"solicitar_eliminacion: Prueba fallida - {e}")

#Prueba para eliminar un usuario
def test_eliminar_usuario(crear_usuario):
    try:
        token = obtenerTokenEliminacion()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_BASE}/users/{crear_usuario}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Administrador Desvinculado", "El usuario falló al ser eliminado"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_usuario: Prueba fallida - {e}")