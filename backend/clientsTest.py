import json
import pytest
import requests
from faker import Faker

fake = Faker('es_MX')

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_CLIENTES = URL_BASE + "/clients"

# Datos necesarios
CLIENTE_JSON = {
    "country_id": 1,
    "name": fake.user_name(),
    "ci": str(fake.unique.random_number(digits=8)),
    "contact_name": fake.name(),
    "contact_email": f"{fake.unique.user_name()}@fos.com.bo",
    "contact_phone": fake.random_element(elements=("6", "7"))+str(fake.random_number(digits=8)),
    "contact_address": fake.address()
}

CLIENTE_JSON_ERROR = {
    "country_id": 1,
    "name": fake.user_name(),
    "ci": str(fake.unique.random_number(digits=8)),
    "contact_name": fake.name(),
    "contact_email": fake.email(),
    "contact_phone": fake.random_element(elements=("6", "7"))+str(fake.random_number(digits=8)),
    "contact_address": fake.address(),    
}

CLIENTE_ACTUALIZAR = {
    "contact_address": fake.address(),
}

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

#Función para llamar a los clientes
def test_client_get():
    try:
        token = obtenerToken()
        params = {"fullType": "L"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(URL_CLIENTES, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print(f"{datos['data']}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_clientes: Prueba fallida - {e}")

# Función para crear un nuevo cliente
@pytest.fixture(scope="module")
def client_post():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_CLIENTES, json=CLIENTE_JSON, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "Registro creado con éxito", f"Mensaje inesperado: {datos['message']}"
        print(f"Cliente creado con ID: {datos['data']}")
        return datos["data"]
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_cliente: Prueba fallida - {e}")

# Prueba para crear un cliente erroneo
def test_client_post_error():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_CLIENTES, json=CLIENTE_JSON_ERROR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "El correo debe tener el dominio @fos.com.bo", f"Mensaje inesperado: {datos['message']}"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crear_cliente_error: Prueba fallida - {e}")

# Prueba para llamar a un cliente específico
def test_client_get_id(client_post):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{URL_CLIENTES}/{client_post}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        print(json.dumps(datos['data'], indent=4))
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"llamar_cliente_id: Prueba fallida - {e}")

# Prueba para editar un cliente
def test_client_put(client_post):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_CLIENTES}/{client_post}", json=CLIENTE_ACTUALIZAR, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "Registro actualizado con éxito", f"Mensaje inesperado: {datos['message']}"
        print(f"Cliente actualizado")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editar_cliente: Prueba fallida - {e}")

# Prueba para eliminar un cliente
def test_client_delete(client_post):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_CLIENTES}/{client_post}", headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert "message" in datos, "La respuesta no contiene la clave 'message'"
        assert datos['message'] == "Registro eliminado con éxito", f"Mensaje inesperado: {datos['message']}"
        print(f"Cliente eliminado")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminar_cliente: Prueba fallida - {e}")