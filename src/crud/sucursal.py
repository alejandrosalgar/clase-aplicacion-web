"""
CRUD de sucursal: conexión con los endpoints /sucursales.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_sucursales() -> list:
    return _get("/sucursales")


def obtener_sucursal(sucursal_id: str) -> dict:
    return _get(f"/sucursales/{sucursal_id}")


def crear_sucursal(
    nombre: str,
    id_usuario_creacion: str,
    direccion: str | None = None,
    ciudad: str | None = None,
    telefono: str | None = None,
) -> dict:
    payload = {
        "nombre": nombre,
        "direccion": direccion,
        "ciudad": ciudad,
        "telefono": telefono,
        "id_usuario_creacion": id_usuario_creacion,
    }
    return _post("/sucursales", json=payload)


def actualizar_sucursal(
    sucursal_id: str,
    nombre: str | None = None,
    direccion: str | None = None,
    ciudad: str | None = None,
    telefono: str | None = None,
    id_usuario_edita: str | None = None,
) -> dict:
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if direccion is not None:
        payload["direccion"] = direccion
    if ciudad is not None:
        payload["ciudad"] = ciudad
    if telefono is not None:
        payload["telefono"] = telefono
    if id_usuario_edita is not None:
        payload["id_usuario_edita"] = id_usuario_edita
    return _put(f"/sucursales/{sucursal_id}", json=payload)


def eliminar_sucursal(sucursal_id: str) -> None:
    _delete(f"/sucursales/{sucursal_id}")
