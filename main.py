import time
from backend.loginTest import *

if __name__ == "__main__":
    try:
        # login
        print("Bienvenido, empezaremos estas pruebas con el endpoint de login")
        time.sleep(3)
        test_login_exitoso()
        test_login_fallido()
        test_login_correo_invalido()
        test_probar_campos_faltantes()
        print("¡Todas las pruebas pasaron exitosamente!")
    except AssertionError as e:
        print(f"Prueba fallida: {e}")
        exit(1)