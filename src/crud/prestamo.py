"""
CRUD de prestamo: conexión con los endpoints /prestamos.
"""
from src.crud.client import _delete, _get, _post, _put

ESTADOS = ["ACTIVO", "PAGADO", "MORA", "CANCELADO"]

def listar_prestamos() -> list:
    return _get("/prestamos")

def obtener_prestamo(id_prestamo: str) -> dict:
    return _get(f"/prestamos/{id_prestamo}")

def crear_prestamo(
    valor: float,
    interes: float,
    plazo: int,
    id_usuario:str,
    estado: str = "ACTIVO"
) ->dict:
    payload = {
        "valor": valor,
        "interes": interes,
        "plazo": plazo,
        "id_usuario": id_usuario,
        "estado": estado
    }
    return _post("/prestamos", json = payload)

def actualizar_prestamo(
    id_prestamo: str,
    valor: float | None= None,
    interes: float | None= None,
    plazo: int | None = None,
    id_usuario: str |None = None,
    estado: str | None = None
) -> dict:
    payload = {

    }

    if valor is not None:
        payload["valor"] = valor
    
    if interes is not None:
        payload["interes"] = interes
    
    if plazo is not None:
        payload["plazo"] = plazo
    
    if id_usuario is not None:
        payload["id_usuario"] = id_usuario
    
    if estado is not None:
        payload["estado"] = estado
    
    return _put(f"/prestamos/{id_prestamo}", json= payload)

def eliminar_prestamo(id_prestamo: str) -> None:
    _delete(f"/prestamos/{id_prestamo}")
