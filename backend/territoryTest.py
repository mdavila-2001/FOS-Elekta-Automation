import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_TERRITORIOS = URL_BASE + "/importXls"

# Datos necesarios
params = {
    "client_id": 3
}

#Obtener el token para las funciones
def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

# Función para importar territorios
def test_import_territories():
    try:
        headers = {"Authorization": f"Bearer {obtenerToken()}"}
        response = requests.post(URL_TERRITORIOS, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert response.status_code == 200
        assert datos['data']
        print(json.dumps(datos['data'], indent=2))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")