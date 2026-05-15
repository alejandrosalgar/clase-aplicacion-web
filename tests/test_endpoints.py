"""Pruebas HTTP contra rutas públicas y flujo login + recurso protegido."""

import uuid


def test_openapi_documentation_available(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    assert "openapi" in body
    assert "paths" in body


def test_crear_usuario_y_login_y_listar_con_token(client):
    suffix = uuid.uuid4().hex[:12]
    nombre_usuario = f"pytest_user_{suffix}"
    payload = {
        "nombre": "Usuario Pytest",
        "nombre_usuario": nombre_usuario,
        "email": f"{nombre_usuario}@test.example.com",
        "contraseña": "TestPass12!",
        "telefono": "3000000000",
        "activo": True,
        "rol": "cliente",
    }
    create = client.post("/usuarios", json=payload)
    assert create.status_code == 201
    created = create.json()
    assert created["success"] is True
    assert created["data"]["nombre_usuario"] == nombre_usuario

    login = client.post(
        "/usuarios/login",
        json={"nombre_usuario": nombre_usuario, "contraseña": "TestPass12!"},
    )
    assert login.status_code == 200
    login_body = login.json()
    assert login_body["success"] is True
    token = login_body["data"]["access_token"]
    assert token

    lista = client.get(
        "/usuarios",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert lista.status_code == 200
    lista_body = lista.json()
    assert lista_body["success"] is True
    assert isinstance(lista_body["data"], list)
