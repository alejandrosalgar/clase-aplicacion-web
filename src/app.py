"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import productos, usuarios

# Importar modelos para que Base.metadata los conozca
import src.entities.usuarios  # noqa: F401
import src.entities.producto  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    # shutdown si hiciera falta


app = FastAPI(
    title="API Usuarios y Productos",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

app.include_router(usuarios.router)
app.include_router(productos.router)


@app.get("/")
def inicio():
    return {"mensaje": "API Usuarios y Productos", "docs": "/docs"}
