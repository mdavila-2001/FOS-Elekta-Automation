import json
import pytest
import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
URL_DASHBOARD = URL_BASE + "/dashboard"

# Datos necesarios

def obtenerToken():
    response = requests.post(f"{URL_BASE}/adm-login", json={"email": "admin@fos.com.bo", "password": "12345678"})
    response.raise_for_status()
    datos = response.json()
    return datos['data']['token']

def test_dashboard_clientes_promedio():
    try:
        token = obtenerToken()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(URL_DASHBOARD, headers=headers)
        response.raise_for_status()
        datos = response.json()
        assert 'data' in datos
        print(f"Afiliados Totales: {json.dumps(datos['data']['card1']['aff'])}")
        print(f"Afiliados nuevos hoy: {json.dumps(datos['data']['card1']['newAff'])}")
        print(f"Validados totales: {json.dumps(datos['data']['card2']['verified'])}")
        print(f"Validados nuevos hoy: {json.dumps(datos['data']['card2']['newVerified'])}")
        print(f"Clientes registrados: {json.dumps(datos['data']['card3']['client'])}")
        print(f"Clientes nuevos hoy: {json.dumps(datos['data']['card3']['newClient'])}")
        print(f"Administradores registrados: {json.dumps(datos['data']['card4']['user'])}")
        print(f"Administradores hoy: {json.dumps(datos['data']['card4']['newUser'])}")
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"test_dashboard_clientes_promedio: Prueba fallida - {e}")