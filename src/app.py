"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.exceptions import AppException
from src.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.core.responses import success_response
from src.database.config import create_tables
from src.endpoints import (
    usuarios,
    sucursal,
    tipo_cuenta,
    cuenta,
    tipo_transaccion,
    transaccion,
    login,
    prestamo,
    pagos,
    tipo_prestamo
)

# Importar modelos para que Base.metadata los conozca
import src.entities.usuarios  # noqa: F401
import src.entities.sucursal  # noqa: F401
import src.entities.tipo_cuenta  # noqa: F401
import src.entities.cuenta  # noqa: F401
import src.entities.tipo_transaccion  # noqa: F401
import src.entities.transaccion  # noqa: F401
import src.entities.prestamo
import src.entities.pagos
import src.entities.tipo_prestamo


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API Banco",
    description="API con FastAPI, SQLAlchemy y PostgreSQL - Usuarios, Sucursales, Cuentas, Transacciones. Incluye validación de datos, manejo de errores unificado y estructuras de respuesta estándar.",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Manejadores globales de excepciones (estructura de respuesta unificada)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(usuarios.router)
app.include_router(sucursal.router)
app.include_router(tipo_cuenta.router)
app.include_router(cuenta.router)
app.include_router(tipo_transaccion.router)
app.include_router(transaccion.router)
app.include_router(login.router)
app.include_router(prestamo.router)   
app.include_router(pagos.router)              
app.include_router(tipo_prestamo.router)     


@app.get("/")
def inicio():
    return success_response(
        data={"mensaje": "API Banco", "docs": "/docs"},
        message="Bienvenido a la API Banco",
    )
