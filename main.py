from backend.loginTest import *
from backend.rolesTest import *

if __name__ == "__main__":
    try:
        # login
        print("Bienvenido, empezaremos estas pruebas con el endpoint de login")
        token = test_login_exitoso()
        test_login_fallido()
        test_login_correo_invalido()
        test_probar_campos_faltantes()
        print("Ahora probaremos con el endpoint de roles")
        test_listado_roles(token)
        print("¡Todas las pruebas pasaron exitosamente!")
    except AssertionError as e:
        print(f"Prueba fallida: {e}")
        exit(1)