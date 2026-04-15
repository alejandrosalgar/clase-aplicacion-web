"""
CRUD de tipo_prestamo: conexión con los endpoints /tipo_prestamo.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_tipos_prestamo() -> list:
    return _get("/tipo_prestamo")


def obtener_tipo_prestamo(tipo_id: str) -> dict:
    return _get(f"/tipo_prestamo/{tipo_id}")


def crear_tipo_prestamo(
    nombre: str,
    descripcion: str | None,
    id_usuario_creacion: str,
    estado: str | None = "ACTIVO",
) -> dict:
    payload = {
        "nombre": nombre,
        "descripcion": descripcion,
        "id_usuario_creacion": id_usuario_creacion,
    }
    if estado is not None:
        payload["estado"] = estado
    return _post("/tipo_prestamo", json=payload)


def actualizar_tipo_prestamo(
    tipo_id: str,
    nombre: str | None = None,
    descripcion: str | None = None,
    estado: str | None = None,
    id_usuario_edita: str | None = None,
) -> dict:
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if descripcion is not None:
        payload["descripcion"] = descripcion
    if estado is not None:
        payload["estado"] = estado
    if id_usuario_edita is not None:
        payload["id_usuario_edita"] = id_usuario_edita
    return _put(f"/tipo_prestamo/{tipo_id}", json=payload)


def eliminar_tipo_prestamo(tipo_id: str) -> None:
    _delete(f"/tipo_prestamo/{tipo_id}")