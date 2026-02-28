"""
CRUD de usuarios: conexión con los endpoints /usuarios.
"""
from src.crud.client import _delete, _get, _post, _put


def listar_usuarios() -> list:
    return _get("/usuarios")


def obtener_usuario(usuario_id: str) -> dict:
    return _get(f"/usuarios/{usuario_id}")


def crear_usuario(
    nombre: str,
    nombre_usuario: str,
    email: str,
    contraseña: str,
    telefono: str | None = None,
    activo: bool = True,
) -> dict:
    payload = {
        "nombre": nombre,
        "nombre_usuario": nombre_usuario,
        "email": email,
        "contraseña": contraseña,
        "telefono": telefono,
        "activo": activo,
    }
    return _post("/usuarios", json=payload)


def actualizar_usuario(
    usuario_id: str,
    nombre: str | None = None,
    nombre_usuario: str | None = None,
    email: str | None = None,
    contraseña: str | None = None,
    telefono: str | None = None,
    activo: bool | None = None,
) -> dict:
    payload = {}
    if nombre is not None:
        payload["nombre"] = nombre
    if nombre_usuario is not None:
        payload["nombre_usuario"] = nombre_usuario
    if email is not None:
        payload["email"] = email
    if contraseña is not None:
        payload["contraseña"] = contraseña
    if telefono is not None:
        payload["telefono"] = telefono
    if activo is not None:
        payload["activo"] = activo
    return _put(f"/usuarios/{usuario_id}", json=payload)


def eliminar_usuario(usuario_id: str) -> None:
    _delete(f"/usuarios/{usuario_id}")
