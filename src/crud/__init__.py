"""
Cliente CRUD que llama a los endpoints de la API.
Nombres alineados con entities: usuarios, producto.
La API debe estar corriendo (uvicorn src.app:app --port 8000).
"""
from src.crud.usuarios import (
    listar_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
)
from src.crud.producto import (
    listar_productos,
    obtener_producto,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
)

__all__ = [
    "listar_usuarios",
    "obtener_usuario",
    "crear_usuario",
    "actualizar_usuario",
    "eliminar_usuario",
    "listar_productos",
    "obtener_producto",
    "crear_producto",
    "actualizar_producto",
    "eliminar_producto",
]
