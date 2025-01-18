import json
import random
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_CANDIDATOS = URL_BASE + "/candidates"

#Datos para el candiato
candidato = {
    "client_id": 1,
    "name": fake.first_name_male(),
    "middle_name": fake.first_name_male(),
    "last_name": fake.last_name_male(),
    "mother_last_name": fake.last_name_male(),
    "title": fake.sentence(),
    "typecand_id": 1,
    "born": "Santa Cruz de la Sierra",
    "profession": fake.job_male(),
    "biography" : "Nacido en 1980",
    "experience": fake.sentence(),
    "plan_goverment": "qwertyuiop",
    "prov_id": 2,
    "position": 0,
    "twitter": "",
    "linkedin": "",
    "instagram": "",
    "facebook": "",
    "ideology": 0
}

CAND_EDIT = {
    "client_id": 1,
    "facebook": "facebook.com",
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_listar_candidatos():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"fullType": "L","client_id": 1}
        response = requests.get(URL_CANDIDATOS, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(datos['data'])
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"listar_candidatos: Prueba fallida - {e}")

@pytest.fixture(scope="module")
def crear_candidato():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        print(json)
        response = requests.post(URL_CANDIDATOS, json=candidato, headers=headers)
        response.raise_for_status()
        datos = response.json()
        print(f"El candidato fue creado con el ID: {datos['data']}")
        print(json.dumps(datos, indent=4))
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_candidato: Error de HTTP - {e}")

def test_actualizar_candidato(crear_candidato):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_CANDIDATOS}/{crear_candidato}", json=CAND_EDIT, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['data']
        print(datos['data'])
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"actualizar_candidato: Error de HTTP - {e}")

def test_llamar_candidato(crear_candidato):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"fullType": "L","client_id": 1}
        response = requests.get(f"{URL_CANDIDATOS}/{crear_candidato}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['data']
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_candidato: Prueba fallida - {e}")

def test_eliminar_candidato(crear_candidato):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1}
        response = requests.delete(f"{URL_CANDIDATOS}/{crear_candidato}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro eliminado con éxito", f"El mensaje de respuesta es: {datos['message']}"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_candidato: Error de HTTP - {e}")