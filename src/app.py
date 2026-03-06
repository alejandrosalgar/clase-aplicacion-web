"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import (
    usuarios,
    sucursal,
    tipo_cuenta,
    cuenta,
    tipo_transaccion,
    transaccion,
)

# Importar modelos para que Base.metadata los conozca
import src.entities.usuarios  # noqa: F401
import src.entities.sucursal  # noqa: F401
import src.entities.tipo_cuenta  # noqa: F401
import src.entities.cuenta  # noqa: F401
import src.entities.tipo_transaccion  # noqa: F401
import src.entities.transaccion  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API Banco",
    description="API con FastAPI, SQLAlchemy y PostgreSQL - Usuarios, Sucursales, Cuentas, Transacciones",
    lifespan=lifespan,
)

app.include_router(usuarios.router)
app.include_router(sucursal.router)
app.include_router(tipo_cuenta.router)
app.include_router(cuenta.router)
app.include_router(tipo_transaccion.router)
app.include_router(transaccion.router)


@app.get("/")
def inicio():
    return {"mensaje": "API Banco", "docs": "/docs"}
