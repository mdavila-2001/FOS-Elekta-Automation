import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_GOAL = URL_BASE + "/goals"

# Datos necesarios
metas = {
    "client_id": 1,
    "name": "Prueba de nivel",
    "level": 1,
    "position": 0,
    "color": "#B04CE4"
}

meta_editada = {
    "client_id": 1,
    "name": "Prueba de nivel editada",
    "color": "#FF0000"
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Prueba para obtener metas
def test_get_goals():
    try:
        token = obtenerToken()
        params = {"client_id": 1}
        headers = {"Authorization": f"Bearer {token}", params=params}
        response = requests.get(URL_GOAL, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert 'data' in datos
        assert isinstance(datos['data'], list)
        print(f"Metas obtenidas: {datos['data']}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Pruebas para la creación, edición y eliminación de metas
@pytest.fixture(scope="module")
def create_goal():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_GOAL, json=metas, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert 'data' in datos
        print(f"Meta creada con el ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_editar_goal(create_goal):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_GOAL}/{create_goal}", json=meta_editada, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar la meta"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def test_eliminar_goal(create_goal):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1}
        response = requests.delete(f"{URL_GOAL}/{create_goal}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro eliminado con éxito", f"No se logró eliminar la meta"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")