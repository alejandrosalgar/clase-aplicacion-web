# Pruebas automatizadas del backend (pytest)

Este directorio contiene pruebas contra la API FastAPI usando **`pytest`** y **`httpx`** (vía `fastapi.testclient.TestClient`).

## Qué se cubre

| Archivo | Contenido |
|--------|-----------|
| `conftest.py` | Fixture compartida `client` (`TestClient` sobre `src.app:app`). |
| `test_api_security.py` | Formato de respuesta en `/`, cabeceras de seguridad, CORS (preflight) y que rutas protegidas devuelven **401** sin token. |
| `test_endpoints.py` | Disponibilidad de `/openapi.json` y flujo **crear usuario → login → listar usuarios con Bearer**. |

La base de datos sigue la lógica del proyecto: si no hay `DATABASE_URL`, se usa **SQLite** (`dev.db` en la raíz del proyecto). Al arrancar la app, el *lifespan* crea tablas con SQLAlchemy.

## Cómo ejecutar

Desde la carpeta **`clase-aplicacion-web`** (donde está `requirements.txt` y `pytest.ini`):

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Opciones útiles:

```bash
python -m pytest -v                 # más detalle
python -m pytest tests/test_api_security.py   # solo seguridad
python -m pytest tests/test_endpoints.py      # solo endpoints / flujo login
```

## CI

El workflow **`.github/workflows/ci_pull.yml`** instala dependencias con `requirements.txt` y ejecuta `python -m pytest -v` en los PR hacia `dev`, `qa` y `prod`.
