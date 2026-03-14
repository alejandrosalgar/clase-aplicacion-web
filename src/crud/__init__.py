"""
Cliente CRUD que llama a los endpoints de la API (lógica banco).
Nombres alineados con entities: usuarios, sucursal, tipo_cuenta, cuenta, tipo_transaccion, transaccion.
La API debe estar corriendo (uvicorn src.app:app --port 8000).
"""

from src.crud.usuarios import (
    listar_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
)
from src.crud.sucursal import (
    listar_sucursales,
    obtener_sucursal,
    crear_sucursal,
    actualizar_sucursal,
    eliminar_sucursal,
)
from src.crud.tipo_cuenta import (
    listar_tipos_cuenta,
    obtener_tipo_cuenta,
    crear_tipo_cuenta,
    actualizar_tipo_cuenta,
    eliminar_tipo_cuenta,
)
from src.crud.cuenta import (
    listar_cuentas,
    obtener_cuenta,
    crear_cuenta,
    actualizar_cuenta,
    eliminar_cuenta,
)
from src.crud.tipo_transaccion import (
    listar_tipos_transaccion,
    obtener_tipo_transaccion,
    crear_tipo_transaccion,
    actualizar_tipo_transaccion,
    eliminar_tipo_transaccion,
)
from src.crud.transaccion import (
    listar_transacciones,
    obtener_transaccion,
    crear_transaccion,
    actualizar_transaccion,
    eliminar_transaccion,
)
from src.crud.login import login

__all__ = [
    "listar_usuarios",
    "obtener_usuario",
    "crear_usuario",
    "actualizar_usuario",
    "eliminar_usuario",
    "listar_sucursales",
    "obtener_sucursal",
    "crear_sucursal",
    "actualizar_sucursal",
    "eliminar_sucursal",
    "listar_tipos_cuenta",
    "obtener_tipo_cuenta",
    "crear_tipo_cuenta",
    "actualizar_tipo_cuenta",
    "eliminar_tipo_cuenta",
    "listar_cuentas",
    "obtener_cuenta",
    "crear_cuenta",
    "actualizar_cuenta",
    "eliminar_cuenta",
    "listar_tipos_transaccion",
    "obtener_tipo_transaccion",
    "crear_tipo_transaccion",
    "actualizar_tipo_transaccion",
    "eliminar_tipo_transaccion",
    "listar_transacciones",
    "obtener_transaccion",
    "crear_transaccion",
    "actualizar_transaccion",
    "eliminar_transaccion",
    "login",
]
