import json
import random
import requests
from faker import Faker

fake = Faker('es_MX')

# Datos a enviar
candidato = {
    "client_id": 1,
    "name": fake.first_name_male(),
    "middle_name": fake.first_name_male(),
    "last_name": fake.last_name_male(),
    "mother_last_name": fake.last_name_male(),
    "title": fake.sentence(),
    "typecand_id": random.randint(1, 5),
    "born": "Santa Cruz de la Sierra",
    "profession": fake.job_male(),
    "biography" : "Nacido en 1980",
    "experience": fake.sentence(),
    "plan_goverment": "qwertyuiop",
    "prov_id": random.randint(1, 9),
    "position": 0,
    "twitter": "",
    "linkedin": "",
    "instagram": "",
    "facebook": "",
    "ideology": 0
}

print(json.dumps(candidato, indent=4))