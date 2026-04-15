"""
CRUD de pago: conexión con los endpoints /pagos.
"""

from src.crud.client import _delete, _get, _post, _put


def listar_pagos() -> list:
    return _get("/pagos")


def obtener_pago(pago_id: str) -> dict:
    return _get(f"/pagos/{pago_id}")


def crear_pago(
    monto: str | float,
    id_prestamo: str,
    id_usuario_creacion: str,
    estado: str | None = "PENDIENTE",
) -> dict:
    payload = {
        "monto": float(monto) if not isinstance(monto, (int, float)) else monto,
        "id_prestamo": id_prestamo,
        "id_usuario_creacion": id_usuario_creacion,
    }
    if estado is not None:
        payload["estado"] = estado
    return _post("/pagos", json=payload)


def actualizar_pago(
    pago_id: str,
    monto: str | float | None = None,
    estado: str | None = None,
    id_usuario_edita: str | None = None,
) -> dict:
    payload = {}
    if monto is not None:
        payload["monto"] = (
            float(monto) if not isinstance(monto, (int, float)) else monto
        )
    if estado is not None:
        payload["estado"] = estado
    if id_usuario_edita is not None:
        payload["id_usuario_edita"] = id_usuario_edita
    return _put(f"/pagos/{pago_id}", json=payload)


def eliminar_pago(pago_id: str) -> None:
    _delete(f"/pagos/{pago_id}")
