"""
CRUD de cuenta: conexión con los endpoints /cuentas.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_cuentas() -> list:
    return _get("/cuentas")


def obtener_cuenta(cuenta_id: str) -> dict:
    return _get(f"/cuentas/{cuenta_id}")


def crear_cuenta(
    numero_cuenta: str,
    id_usuario: str,
    id_sucursal: str,
    id_tipo_cuenta: str,
    saldo: str | float | None = "0",
    id_usuario_creacion: str = None,
) -> dict:
    payload = {
        "numero_cuenta": numero_cuenta,
        "id_usuario": id_usuario,
        "id_sucursal": id_sucursal,
        "id_tipo_cuenta": id_tipo_cuenta,
        "id_usuario_creacion": id_usuario_creacion,
    }
    if saldo is not None:
        payload["saldo"] = (
            float(saldo) if not isinstance(saldo, (int, float)) else saldo
        )
    return _post("/cuentas", json=payload)


def actualizar_cuenta(
    cuenta_id: str,
    numero_cuenta: str | None = None,
    id_sucursal: str | None = None,
    id_tipo_cuenta: str | None = None,
    saldo: str | float | None = None,
    id_usuario_edita: str | None = None,
) -> dict:
    payload = {}
    if numero_cuenta is not None:
        payload["numero_cuenta"] = numero_cuenta
    if id_sucursal is not None:
        payload["id_sucursal"] = id_sucursal
    if id_tipo_cuenta is not None:
        payload["id_tipo_cuenta"] = id_tipo_cuenta
    if saldo is not None:
        payload["saldo"] = str(saldo) if not isinstance(saldo, (int, float)) else saldo
    if id_usuario_edita is not None:
        payload["id_usuario_edita"] = id_usuario_edita
    return _put(f"/cuentas/{cuenta_id}", json=payload)


def eliminar_cuenta(cuenta_id: str) -> None:
    _delete(f"/cuentas/{cuenta_id}")
