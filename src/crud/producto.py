"""
CRUD de producto: conexión con los endpoints /productos.
"""
from src.crud.client import _delete, _get, _post, _put


def listar_productos() -> list:
    return _get("/productos")


def obtener_producto(producto_id: str) -> dict:
    return _get(f"/productos/{producto_id}")


def crear_producto(nombre: str, id_usuario_crea: str, descripcion: str | None = None) -> dict:
    payload = {
        "nombre": nombre,
        "id_usuario_crea": id_usuario_crea,
        "descripcion": descripcion,
    }
    return _post("/productos", json=payload)


def actualizar_producto(
    producto_id: str,
    nombre: str | None = None,
    descripcion: str | None = None,
    id_usuario_edita: str | None = None,
) -> dict:
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if descripcion is not None:
        payload["descripcion"] = descripcion
    if id_usuario_edita is not None:
        payload["id_usuario_edita"] = id_usuario_edita
    return _put(f"/productos/{producto_id}", json=payload)


def eliminar_producto(producto_id: str) -> None:
    _delete(f"/productos/{producto_id}")
