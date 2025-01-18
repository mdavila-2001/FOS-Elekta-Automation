import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_MEDALS = URL_BASE + "/medals"

# Datos necesarios
insignia = {
    "client_id": 1,
    "name": "Haz saber a todos sobre nosotros!",
    "description": "Gracias por compartir nuestras noticias :)",
    "league_id": 1,
    "points": 100,
    "points_gral": 100
}

insignia_editada = {
    "client_id": 1,
    "description": "Te agradecemos por compartir nuestras noticias :)"
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Función para llamar a todas las insignias
def test_obtener_insignias():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1, "fullType": "L"}
        response = requests.get(URL_MEDALS, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
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
def crear_insignia():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_MEDALS, json=insignia, headers=headers)
        response.raise_for_status()
        datos = response.json()
        print(f"Insignia creada con el ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Función para editar una insignia
def test_editar_insignia(crear_insignia):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_MEDALS}/{crear_insignia}", json=insignia_editada, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar la insignia"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Función para eliminar una insignia
def test_eliminar_insignia(crear_insignia):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 1}
        response = requests.delete(f"{URL_MEDALS}/{crear_insignia}", headers=headers, params=params)
        response.raise_for_status()
        assert response.status_code == 200
        datos = response.json()
        assert 'message' in datos
        assert datos['message'] == "Registro eliminado con éxito", "No se logró eliminar la insignia"
        print(json.dumps(datos, indent=2))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")