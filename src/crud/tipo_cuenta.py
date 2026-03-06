"""
CRUD de tipo_cuenta: conexión con los endpoints /tipos-cuenta.
"""
from src.crud.client import _delete, _get, _post, _put


def listar_tipos_cuenta() -> list:
    return _get("/tipos-cuenta")


def obtener_tipo_cuenta(tipo_id: str) -> dict:
    return _get(f"/tipos-cuenta/{tipo_id}")


def crear_tipo_cuenta(codigo: str, nombre: str) -> dict:
    return _post("/tipos-cuenta", json={"codigo": codigo, "nombre": nombre})


def actualizar_tipo_cuenta(
    tipo_id: str,
    codigo: str | None = None,
    nombre: str | None = None,
) -> dict:
    payload = {}
    if codigo is not None:
        payload["codigo"] = codigo
    if nombre is not None:
        payload["nombre"] = nombre
    return _put(f"/tipos-cuenta/{tipo_id}", json=payload)


def eliminar_tipo_cuenta(tipo_id: str) -> None:
    _delete(f"/tipos-cuenta/{tipo_id}")
