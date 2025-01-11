import json
import random
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_TAREAS = URL_BASE + "/setuptasks"

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

#Datos necesarios para la Creación y edición
TAREA_A_CREAR = {
    "name": fake.text(max_nb_chars=50),
    "description": fake.sentence(),
    "position": random.randint(1, 100),
}

EDICION = {
    "description": fake.sentence(),
}

#Llamar a las tareas
def test_llamar_tareas():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(URL_TAREAS, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "data" in datos, "La respuesta no contiene la clave 'data'"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_clientes: Prueba fallida - {e}")

#Crear tarea
@pytest.fixture(scope="module")
def crearTarea():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_TAREAS, json=TAREA_A_CREAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "Registro creado con éxito", f"Mensaje inesperado: {datos['message']}"
        print(f"Tarea creada con ID: {datos['data']}")
        return datos["data"]
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")

#Editar tarea
def test_editarTarea(crearTarea):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_TAREAS}/{crearTarea}", json=EDICION, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar la tarea"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_tarea: Prueba fallida - {e}")

#Eliminar tarea
def test_eliminarTarea(crearTarea):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_TAREAS}/{crearTarea}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert datos['message'] == "Registro eliminado con éxito", "No se logró eliminar la tarea"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_tarea: Prueba fallida - {e}")