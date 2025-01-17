import json
import random
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_NIVELES = URL_BASE + "/levels"

# Datos necesarios
nivel = {
    "client_id": 1,
    "name": "1",
    "description": "Desc Nivel 0",
    "league_id": 2,
    "points": 0
}

nivel_edit = {
    "client_id": 1,
    "description": "Nivel de prueba"
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Función para llamar a un nivel
def test_get_levels():
    try:
        headers = {"Authorization": f"Bearer {obtenerToken()}"}
        params = {"client_id": 1}
        response = requests.get(URL_NIVELES, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['data']
        print(json.dumps(datos['data'], indent=2))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Función para crear un nivel
@pytest.fixture(scope="module")
def create_level():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_NIVELES, json=nivel, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 20
        assert 'data' in datos
        print(f"Nivel creado con el ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_get_level_id(create_level):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1}
        response = requests.get(f"{URL_NIVELES}/{create_level}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(json.dumps(datos['data'], indent=2))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_update_level(create_level):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_NIVELES}/{create_level}", json=nivel_edit, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert 'message' in datos
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar el nivel"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_delete_level(create_level):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1}
        response = requests.delete(f"{URL_NIVELES}/{create_level}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert 'message' in datos
        assert datos['message'] == "Registro eliminado con éxito", "No se logró eliminar el nivel"
        print(json.dumps(datos, indent=2))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")