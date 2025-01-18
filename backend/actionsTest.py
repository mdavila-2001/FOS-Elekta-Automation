import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_ACTIONS = URL_BASE + "/gameactions"

# Datos necesarios
accion = {
    "client_id": 1,
    "name": "comment_post",
    "description": "La obtienes por comentar una noticia ...",
    "league_id": 1,
    "points": 1,
    "points_gral": 1
}

accion_editada = {
    "client_id": 1,
    "name": "comment_a_post"
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Función para llamar a todas las insignias
def test_obtener_acciones():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1, "fullType": "L"}
        response = requests.get(URL_ACTIONS, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert 'data' in datos
        print(f"Insignias obtenidas: {json.dumps(datos['data'], indent=4)}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

@pytest.fixture(scope="module")
def crear_accion():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_ACTIONS, json=accion, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Insignia creada con el ID: {datos['data']}")
        print(json.dumps(datos, indent=4))
        return datos['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Función para editar una insignia
def test_editar_accion(crear_accion):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_ACTIONS}/{crear_accion}", json=accion_editada, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print("Acción editada correctamente")
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar la accion"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Función para eliminar una insignia
def test_eliminar_accion(crear_accion):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1}
        response = requests.delete(f"{URL_ACTIONS}/{crear_accion}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print("Acción eliminada correctamente")
        assert datos['message'] == "Registro eliminado con éxito", "No se logró eliminar la acción"
        print(json.dumps(datos, indent=4))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")