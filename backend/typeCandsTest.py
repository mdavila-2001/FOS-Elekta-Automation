import json
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_TIPO_CAND = URL_BASE + "/typecands"

# Datos necesarios
typeCand = {
    "name": "Alcalde",
    "client_id": 1
}

typeCand_Edit = {
    "name": "Diputado",
    "client_id": 1
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_listar_typecands():
    try:
        token = obtenerToken()
        params = {"fullType": "L", "client_id": 1}
        response = requests.get(URL_TIPO_CAND, headers={"Authorization": f"Bearer {token}"}, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert "data" in datos, "La respuesta no contiene la clave 'data'"
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"test_listar_typecands: Error de HTTP - {err}")

@pytest.fixture(scope="module")
def crear_typecand():
    try:
        token = obtenerToken()
        response = requests.post(URL_TIPO_CAND, json=typeCand, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert "data" in datos, "La respuesta no contiene la clave 'data'"
        print(json.dumps(datos, indent=4))
        return datos['data']
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"crear_typecand: Error de HTTP - {err}")

def test_actualizar_typecand(crear_typecand):
    try:
        token = obtenerToken()
        typeCand['name'] = fake.name()
        response = requests.put(f"{URL_TIPO_CAND}/{crear_typecand}", json=typeCand_Edit, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "Registro actualizado con éxito", f"Mensaje inesperado: {datos['message']}"
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"test_actualizar_typecand: Error de HTTP - {err}")

def test_eliminar_typecand(crear_typecand):
    try:
        token = obtenerToken()
        response = requests.delete(f"{URL_TIPO_CAND}/{crear_typecand}", headers={"Authorization": f"Bearer {token}"}, json={"client_id": 1})
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "Registro eliminado con éxito", f"Mensaje inesperado: {datos['message']}"
    except requests.exceptions.HTTPError as err:
        pytest.fail(f"test_eliminar_typecand: Error de HTTP - {err}")