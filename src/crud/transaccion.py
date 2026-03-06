"""
CRUD de transaccion: conexión con los endpoints /transacciones.
"""
from src.crud.client import _delete, _get, _post, _put


def listar_transacciones() -> list:
    return _get("/transacciones")


def obtener_transaccion(transaccion_id: str) -> dict:
    return _get(f"/transacciones/{transaccion_id}")


def crear_transaccion(
    id_cuenta: str,
    id_tipo_transaccion: str,
    monto: str | float,
    id_cuenta_destino: str | None = None,
    descripcion: str | None = None,
) -> dict:
    payload = {
        "id_cuenta": id_cuenta,
        "id_tipo_transaccion": id_tipo_transaccion,
        "monto": str(monto) if not isinstance(monto, (int, float)) else monto,
        "id_cuenta_destino": id_cuenta_destino,
        "descripcion": descripcion,
    }
    return _post("/transacciones", json=payload)


def actualizar_transaccion(
    transaccion_id: str,
    descripcion: str | None = None,
) -> dict:
    payload = {}
    if descripcion is not None:
        payload["descripcion"] = descripcion
    return _put(f"/transacciones/{transaccion_id}", json=payload)


def eliminar_transaccion(transaccion_id: str) -> None:
    _delete(f"/transacciones/{transaccion_id}")
