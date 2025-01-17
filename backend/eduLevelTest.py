import json
import random
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_EDU_LEVEL = URL_BASE + "/educations"

# Datos necesarios
educacion = {
    "client_id": 1,
    "name": "Universidad",
}

educacion_edit = {
    "client_id": 1,
    "name": "Universitario",
}

params = {
    "client_id": 1,
    "fullType": "L"
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_get_educations():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(URL_EDU_LEVEL, headers=headers, params=params)
        response.raise_for_status()
        assert response.status_code == 200
        assert response.json()['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

@pytest.fixture(scope="module")
def post_education():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_EDU_LEVEL, json=educacion, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Nivel creado con el ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_update_education(post_education):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_EDU_LEVEL}/{post_education}", json=educacion_edit, headers=headers)
        response.raise_for_status()
        assert response.status_code == 200
        assert response.json()['message'] == "Registro actualizado con éxito"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_delete_education(post_education):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_EDU_LEVEL}/{post_education['id']}", headers=headers, params={"client_id": 1})
        response.raise_for_status()
        assert response.status_code == 200
        assert response.json()['message'] == "Registro eliminado con éxito"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")