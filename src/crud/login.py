"""
CRUD de login: conexión con los endpoints /usuarios para el logueo.
"""

from src.crud.client import _post


def login(nombre_usuario: str, contraseña: str) -> dict:
    payload = {"nombre_usuario": nombre_usuario, "contraseña": contraseña}
    respuesta = _post("/usuarios/login", json=payload)
    return respuesta
