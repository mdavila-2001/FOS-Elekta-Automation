import pandas as pd
from faker import Faker

fake = Faker('es_MX')

# Definir el número de filas
num_filas = 19

# Generar datos aleatorios
datos = {
    "Nombre": [fake.first_name_male() for _ in range(num_filas)],
    "Segundo nombre": [fake.first_name_male() for _ in range(num_filas)],
    "Apellido paterno": [fake.last_name_male() for _ in range(num_filas)],
    "Apellido materno": [fake.last_name_male() for _ in range(num_filas)],
    "Apodo": [fake.user_name() for _ in range(num_filas)],
    "Profesión": [fake.job_male() for _ in range(num_filas)],
    "Título": [fake.sentence() for _ in range(num_filas)]
}

# Crear un DataFrame con los datos
df = pd.DataFrame(datos)

# Exportar el DataFrame a un archivo de Excel
df.to_excel('datos_aleatorios.xlsx', index=False)