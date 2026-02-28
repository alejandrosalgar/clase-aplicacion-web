# API Usuarios y Productos (FastAPI)

## Estructura

- **src/entities** – Modelos SQLAlchemy (tablas: `Usuario`, `Producto`)
- **src/database** – Conexión PostgreSQL y sesión
- **src/schemas** – Modelos Pydantic para request/response
- **src/endpoints** – Rutas FastAPI (usuarios y productos)
- **src/crud** – Cliente que llama a los endpoints (httpx)
- **main.py** – Menú por consola que usa el CRUD

## Requisitos

- Python 3.10+
- Variable de entorno `DATABASE_URL` (PostgreSQL, ej. Neon)

## Instalación

```bash
pip install -r requirements.txt
```

Crear `.env` en la raíz con:

```
DATABASE_URL=postgresql://user:password@host/db?sslmode=require
```

## Migración / crear tablas en Neon

Para crear las tablas en la base de datos (sin levantar la API):

```bash
python init_db.py
```

Solo hace falta ejecutarlo una vez (o cuando cambies las entidades y quieras aplicar el esquema). La API también puede crear las tablas al arrancar si no existen.

## Ejecución

1. **Levantar la API** (en una terminal):

```bash
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

2. **Menú por consola** (en otra terminal):

```bash
python main.py
```

El menú permite listar, crear, ver, actualizar y eliminar usuarios y productos usando la API.

## Documentación API

Con la API en marcha: http://localhost:8000/docs (Swagger UI).
