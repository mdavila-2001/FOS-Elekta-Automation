from backend.loginTest import *

if __name__ == "__main__":
    try:
        login_exitoso()
        login_fallido()
        login_correo_invalido()
        probar_campos_faltantes()
        print("¡Todas las pruebas pasaron exitosamente!")
    except AssertionError as e:
        print(f"Prueba fallida: {e}")
        exit(1)