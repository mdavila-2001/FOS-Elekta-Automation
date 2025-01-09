import pytest
import random

# Fixture para crear un ID aleatorio con alcance de módulo
@pytest.fixture(scope="module")
def id_aleatorio():
    return random.randint(1000, 9999)  # Genera un ID aleatorio

# Prueba que usa el ID aleatorio
def test_funcion_1(id_aleatorio):
    print(f"ID usado en función 1: {id_aleatorio}")
    assert id_aleatorio > 0  # Ejemplo de validación

# Otra prueba que usa el mismo ID aleatorio
def test_funcion_2(id_aleatorio):
    print(f"ID usado en función 2: {id_aleatorio}")
    assert id_aleatorio > 0  # Ejemplo de validación