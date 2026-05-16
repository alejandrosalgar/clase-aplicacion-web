"""
CRUD de tipo_transaccion: conexión con los endpoints /tipos-transaccion.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_tipos_transaccion() -> list:
    return _get("/tipos-transaccion")


def obtener_tipo_transaccion(tipo_id: str) -> dict:
    return _get(f"/tipos-transaccion/{tipo_id}")


def crear_tipo_transaccion(codigo: str, nombre: str, id_usuario_creacion: str) -> dict:
    payload = {
        "codigo": codigo,
        "nombre": nombre,
        "id_usuario_creacion": id_usuario_creacion,
    }
    return _post("/tipos-transaccion", json=payload)


def actualizar_tipo_transaccion(
    tipo_id: str,
    codigo: str | None = None,
    nombre: str | None = None,
    id_usuario_edita: str | None = None,
) -> dict:
    payload = {}
    if codigo is not None:
        payload["codigo"] = codigo
    if nombre is not None:
        payload["nombre"] = nombre
    if id_usuario_edita is not None:
        payload["id_usuario_edita"] = id_usuario_edita
    return _put(f"/tipos-transaccion/{tipo_id}", json=payload)


def eliminar_tipo_transaccion(tipo_id: str) -> None:
    _delete(f"/tipos-transaccion/{tipo_id}")
