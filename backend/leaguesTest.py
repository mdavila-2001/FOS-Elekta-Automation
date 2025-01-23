import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_LEAGUES = URL_BASE + "/leagues"

# Datos necesarios
liga = {
    "client_id": 1,
    "name": "Liga Prueba",
    "description": "Pruebas"
}

liga_editada = {
    "client_id": 1,
    "description": "Liga para Afiliados"
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Función para llamar a todas las ligas
def test_obtenerLigas():
    try:
        token = obtenerToken()
        params = {"client_id": 1, "fullType": "L"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(URL_LEAGUES, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert 'data' in datos
        print(f"Ligas obtenidas: {json.dumps(datos['data'], indent=4)}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"obtenerLigas: Prueba fallida - {e}")

# Pruebas para la creación, edición y eliminación de ligas
@pytest.fixture(scope="module")
def crear_liga():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(URL_LEAGUES, json=liga, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        print(f"Liga creada con el ID: {datos['data']}")
        return datos['data']
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"crearLiga: Prueba fallida - {e}")
        print(f"crearLiga: Prueba fallida - {e}")

def test_editar_liga(crear_liga):
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{URL_LEAGUES}/{crear_liga}", json=liga_editada, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro actualizado con éxito", "No se logró actualizar la liga"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"editarLiga: Prueba fallida - {e}")

def test_eliminar_liga(crear_liga):
    try:
        token = obtenerToken()
        params = {"client_id": 1}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{URL_LEAGUES}/{crear_liga}", headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['message'] == "Registro eliminado con éxito", f"El mensaje de respuesta es: {datos['message']}"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"eliminarLiga: Prueba fallida - {e}")