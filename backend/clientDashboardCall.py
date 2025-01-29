import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_CLIENT_DASHBOARD = URL_BASE + "/client-dashboard"

# Datos necesarios

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_dashboard_clientes():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"client_id": 3}
        response = requests.get(URL_CLIENT_DASHBOARD, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
        assert 'data' in datos
        print(json.dumps(datos['data'], indent=2))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")