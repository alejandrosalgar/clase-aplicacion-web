"""
CRUD de tipo_transaccion: conexión con los endpoints /tipos-transaccion.
"""
from src.crud.client import _delete, _get, _post, _put


def listar_tipos_transaccion() -> list:
    return _get("/tipos-transaccion")


def obtener_tipo_transaccion(tipo_id: str) -> dict:
    return _get(f"/tipos-transaccion/{tipo_id}")


def crear_tipo_transaccion(codigo: str, nombre: str) -> dict:
    return _post("/tipos-transaccion", json={"codigo": codigo, "nombre": nombre})


def actualizar_tipo_transaccion(
    tipo_id: str,
    codigo: str | None = None,
    nombre: str | None = None,
) -> dict:
    payload = {}
    if codigo is not None:
        payload["codigo"] = codigo
    if nombre is not None:
        payload["nombre"] = nombre
    return _put(f"/tipos-transaccion/{tipo_id}", json=payload)


def eliminar_tipo_transaccion(tipo_id: str) -> None:
    _delete(f"/tipos-transaccion/{tipo_id}")
