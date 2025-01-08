import requests

# Definir constantes
URL_BASE = "https://apielektadev.fos.com.bo/api"
CREDENCIALES_VALIDAS = {"email": "admin@fos.com.bo", "password": "12345678"}
DOMINIO_INCORRECTO = {"email": "admin@fost.com.bo", "password": "87654321"}
CREDENCIALES_INVALIDAS = {"email": "user@fos.com.bo", "password": "admins"}

# Prueba: Login exitoso
def test_login_exitoso():
    response = requests.post(f"{URL_BASE}/adm-login", json=CREDENCIALES_VALIDAS)
    assert response.status_code == 200
    datos = response.json()
    assert "message" in datos
    assert datos["message"] == "Login successful"

# Prueba: Login fallido con credenciales incorrectas
def test_login_fallido():
    response = requests.post(f"{URL_BASE}/adm-login", json=CREDENCIALES_INVALIDAS)
    assert response.status_code == 200
    datos = response.json()
    assert "message" in datos
    assert datos["message"] == "Acceso incorrecto"

# Prueba: Login con correo inválido
def test_login_correo_invalido():
    response = requests.post(f"{URL_BASE}/adm-login", json=DOMINIO_INCORRECTO)
    assert response.status_code == 200
    datos = response.json()
    assert "message" in datos
    assert datos["message"] == "Validation Error"

# Prueba: Campos faltantes en el login
def test_probar_campos_faltantes():
    response = requests.post(f"{URL_BASE}/adm-login", json={})
    assert response.status_code == 200
    datos = response.json()
    assert "message" in datos
    assert datos["message"] == "Validation Error"