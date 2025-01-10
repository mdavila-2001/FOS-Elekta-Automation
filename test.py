import json

# Supongamos que esta es la respuesta JSON
response_json = {
    "success": True,
    "data": {
        "id": "9dede462-9162-40e3-bc53-8b30c8f7042d",
        "role_id": 1,
        "ci": "12345678",
        "name": "Admin",
        "middle_name": None,
        "last_name": "FOS",
        "mother_last_name": None,
        "phone": None,
        "address": None,
        "birthdate": None,
        "gender": None,
        "url_avatar": None,
        "email_verified_at": None,
        "email": "admin@fos.com.bo",
        "type": "ADM",
        "status": "A",
        "is_special": "A",
        "request_user": None,
        "emergency_contact": None,
        "emergency_phone": None,
        "created_at": "2025-01-09T19:24:04.000000Z",
        "updated_at": "2025-01-09T19:24:04.000000Z",
        "deleted_at": None
    },
    "message": "Show",
    "Debug_Querys": [
        {"query": "select * from `personal_access_tokens` where `personal_access_tokens`.`id` = ? limit 1", "bindings": ["67"], "time": 63.41},
        {"query": "select * from `users` where `users`.`id` = ? and `users`.`deleted_at` is null limit 1", "bindings": ["9dede462-9162-40e3-bc53-8b30c8f7042d"], "time": 1.71},
        {"query": "update `personal_access_tokens` set `last_used_at` = ?, `personal_access_tokens`.`updated_at` = ? where `id` = ?", "bindings": ["2025-01-10 13:45:23", "2025-01-10 13:45:23", 67], "time": 12.62},
        {"query": "select * from `users` where `users`.`id` = ? and `users`.`deleted_at` is null limit 1", "bindings": ["9dede462-9162-40e3-bc53-8b30c8f7042d"], "time": 1.11}
    ],
    "debugMsg": []
}

# Acceder a todo lo que está dentro de "data"
data = response_json["data"]

# Imprimir el contenido de "data" de manera formateada
print(json.dumps(data, indent=4))