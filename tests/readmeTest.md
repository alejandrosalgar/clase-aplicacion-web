# Guía de pruebas automatizadas del backend (pytest + FastAPI)

Este documento explica **qué son** estas pruebas, **para qué sirven**, **cómo ejecutarlas**, **qué significa cada pieza de código** que usamos (`fixture`, `TestClient`, `assert`, etc.) y un **paso a paso** para replicar el mismo enfoque en otros proyectos.

---

## 1. Concepto: ¿qué es una “prueba automatizada”?

Una **prueba automatizada** es un programa que **ejecuta tu aplicación** y **comprueba** que el comportamiento coincide con lo esperado (respuesta HTTP, JSON, cabeceras, reglas de seguridad).

En este proyecto las pruebas son principalmente **pruebas de integración ligera contra la API**:

- Se arranca la aplicación FastAPI **en memoria** (no hace falta abrir un navegador ni `uvicorn` manualmente para estas pruebas).
- Se envían peticiones HTTP **simuladas** (`GET`, `POST`, `OPTIONS`, etc.).
- Se validan **código de estado**, **cuerpo JSON** y **cabeceras**.

**pytest** es el **motor** que descubre archivos `test_*.py`, ejecuta las funciones `test_*` y reporta éxitos y fallos. Si algo cambia en el código y rompe un contrato (por ejemplo, `/` ya no devuelve `success: true`), la prueba **falla** y te avisa antes de desplegar.

---

## 2. ¿Por qué se hace esto?

| Motivo | Qué aporta |
|--------|------------|
| **Evitar regresiones** | Un cambio en middleware, CORS o JWT no rompe silenciosamente el comportamiento público de la API. |
| **Documentación ejecutable** | Las pruebas describen “cómo debe comportarse” la API; si miente, el CI falla. |
| **Confianza en CI** | En cada Pull Request se puede ejecutar lo mismo que en local (`python -m pytest -v`). |
| **Velocidad de feedback** | Segundos frente a probar todo a mano en Postman o el front. |

No sustituye pruebas manuales ni auditorías de seguridad profundas, pero cubre **contratos básicos** muy útiles en proyectos de clase y en APIs REST.

---

## 3. Herramientas que intervienen

| Herramienta | Rol |
|-------------|-----|
| **pytest** | Ejecutor de pruebas: descubre tests, muestra trazas si algo falla. |
| **FastAPI `TestClient`** | Cliente HTTP de prueba basado en **Starlette** / **httpx**: simula peticiones contra la app sin red real. |
| **`pytest.ini`** | Configura pytest (`testpaths`, `pythonpath`) para que `import src` funcione. |
| **`conftest.py`** | Archivo especial de pytest donde se definen **fixtures** compartidas por todos los tests del carpeta `tests/`. |

La API usa base de datos según el proyecto: si no hay `DATABASE_URL`, en desarrollo suele usarse **SQLite** (`dev.db`). El *lifespan* de FastAPI crea tablas al iniciar; las pruebas **disparan ese arranque** al usar `TestClient(app)`.

---

## 4. Estructura de archivos en esta carpeta

| Archivo | Propósito |
|---------|-----------|
| `conftest.py` | Define la fixture `client` (una vez por test, típicamente). |
| `test_api_security.py` | Prueba forma de respuesta en `/`, cabeceras de seguridad, CORS (preflight) y que rutas protegidas dan **401** sin token. |
| `test_endpoints.py` | Prueba `/openapi.json` y el flujo **crear usuario → login → listar con Bearer**. |
| `readmeTest.md` | Esta guía. |

---

## 5. Configuración: `pytest.ini`

```ini
[pytest]
testpaths = tests
pythonpath = .
```

- **`testpaths = tests`**: solo busca pruebas dentro de la carpeta `tests/`.
- **`pythonpath = .`**: añade la raíz del proyecto al path de Python para poder hacer `from src.app import app` sin instalar el paquete como editable.

En otros proyectos, si tus imports son distintos (`from mi_paquete.app`), ajusta la raíz en `pythonpath` o la estructura de carpetas.

---

## 6. Fixture compartida: `conftest.py`

```python
@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
```

### ¿Qué es una **fixture**?

En pytest, una **fixture** es una función que **prepara algo** que los tests necesitan. pytest **inyecta** el resultado llamando a la fixture por nombre en el parámetro de la función de test.

### ¿Qué hace `@pytest.fixture`?

Es un **decorador**: marca la función `client` como fixture registrada en pytest. Cuando escribes:

```python
def test_algo(client):
    ...
```

pytest ve el nombre `client`, busca una fixture llamada `client` y **ejecuta** esa función antes del test, pasándote el valor devuelto (`TestClient(app)`).

Opciones habituales (no las usamos aquí, pero aparecen en otros tutoriales):

- `scope="module"` — crear el cliente una vez por archivo.
- `scope="session"` — una vez por toda la sesión de pytest.

Aquí el alcance por defecto es **function**: cada test recibe un cliente nuevo (simple y seguro para empezar).

### ¿Qué es `TestClient`?

`TestClient(app)` envuelve la aplicación ASGI (`app`). Métodos típicos:

- **`client.get(url)`** — petición GET.
- **`client.post(url, json=dict)`** — POST con cuerpo JSON.
- **`client.options(url, headers=...)`** — útil para simular **preflight CORS**.

Devuelve un objeto **`response`** con `.status_code`, `.json()`, `.headers`.

---

## 7. Funciones de prueba: convención `test_*`

pytest ejecuta **funciones** cuyo nombre empieza por `test_` (y clases `Test*` si usaras estilo clase).

Ejemplo:

```python
def test_root_health_response_shape(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
```

### ¿Qué hace cada parte?

| Pieza | Significado |
|-------|-------------|
| `client.get("/")` | Simula un navegador o cliente que llama al endpoint raíz. |
| `response.status_code` | Código HTTP (200, 401, 404…). |
| `response.json()` | Parsea el cuerpo como JSON (dict/list). Falla si no es JSON válido. |
| `response.headers` | Diccionario-like de cabeceras HTTP (en Starlette suelen ser **case-insensitive** para lectura). |
| **`assert condición`** | Si es falsa, pytest marca el test como fallido y muestra la línea. |

### Cabeceras de seguridad (`test_security_headers_are_present`)

Aquí comprobamos que el middleware de la API añade cabeceras como `X-Content-Type-Options`, `X-Frame-Options`, etc. Son **contratos** entre servidor y clientes / políticas de seguridad.

### CORS preflight (`test_cors_preflight_allows_localhost_4200`)

El navegador, ante ciertos métodos u orígenes, envía antes una petición **`OPTIONS`** (“preflight”). El test simula eso con `client.options(...)` y comprueba que las cabeceras `Access-Control-*` permiten el origen de desarrollo (`localhost:4200`).

### Rutas protegidas (`test_protected_endpoint_requires_bearer_token`)

`client.get("/usuarios")` **sin** `Authorization` debe devolver **401** y un JSON de error acorde al proyecto (`success: false`, mensaje en `error`).

---

## 8. Flujo con datos: `test_endpoints.py`

### `uuid.uuid4().hex`

Genera un sufijo **único** para `nombre_usuario` y el email, para que las ejecuciones repetidas no fallen por “usuario ya existe” en la misma base SQLite de desarrollo.

### `client.post("/usuarios", json=payload)`

Crea un usuario (endpoint público de alta). Se comprueba **201** y el payload de éxito del proyecto.

### `client.post("/usuarios/login", json={...})`

Obtiene `access_token` en la respuesta JSON.

### `client.get("/usuarios", headers={"Authorization": f"Bearer {token}"})`

Comprueba que con token válido la lista de usuarios responde **200** y que `data` es una **lista**.

---

## 9. Cómo ejecutar (local)

Desde la carpeta del proyecto donde están **`requirements.txt`** y **`pytest.ini`** (aquí: `clase-aplicacion-web`):

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Comandos útiles:

```bash
python -m pytest -v                           # todos los tests, modo verboso
python -m pytest tests/test_api_security.py   # solo seguridad / CORS / 401
python -m pytest tests/test_endpoints.py      # solo OpenAPI y flujo login
python -m pytest -k "cors"                    # por nombre (substring)
```

---

## 10. Integración continua (CI)

El workflow **`.github/workflows/ci_pull.yml`** instala dependencias con `pip install -r requirements.txt` y ejecuta:

```bash
python -m pytest -v
```

Así, cada Pull Request hacia `dev`, `qa` o `prod` repite las mismas comprobaciones que en tu máquina.

**Importante:** el workflow asume que la **raíz del repositorio** es la carpeta donde están `requirements.txt` y `pytest.ini`. Si tu repo de GitHub es un monorepo y el backend está en un subdirectorio, hay que añadir `working-directory` en el job o rutas relativas en los pasos.

---

## 11. Paso a paso: replicar este enfoque en **otro** proyecto

### Paso 1 — Dependencias

En `requirements.txt` (o `pyproject.toml`) del backend:

- framework web (FastAPI, Flask, Django…),
- **`pytest`**,
- para FastAPI: ya tienes **`httpx`** como dependencia típica; `TestClient` viene de **`starlette.testclient`** expuesto como `fastapi.testclient`.

### Paso 2 — Carpeta de tests

Crea `tests/` en la raíz del backend y, si hace falta, `pytest.ini` con `pythonpath = .` apuntando a la raíz donde viven tus imports (`src`, `app`, etc.).

### Paso 3 — Cliente de prueba

- **FastAPI / Starlette:** `from fastapi.testclient import TestClient` y `TestClient(app)`.
- **Flask:** `app.test_client()`.
- **Django:** `django.test.Client`.

La idea es la misma: **simular HTTP** sin abrir puertos.

### Paso 4 — `conftest.py`

Define fixtures que **todas** las pruebas reutilicen (cliente, sesión de BD de prueba, usuario semilla, etc.).

### Paso 5 — Escribir el primer test

Empieza por un **smoke test**: `GET /` o `/health` → `200` y estructura mínima esperada.

### Paso 6 — Añadir tests de reglas de negocio

Copia el patrón: **arrange** (datos), **act** (`post`/`get`), **assert** (status + JSON).

### Paso 7 — Base de datos en tests (recomendación para crecer)

En proyectos grandes suele usarse:

- una **base SQLite en memoria** (`sqlite:///:memory:`) o un archivo temporal,
- o **contenedores** (PostgreSQL en Docker) en CI.

Este proyecto usa la misma configuración que desarrollo si no defines `DATABASE_URL`; para otros proyectos evalúa aislar tests para no mezclar `dev.db` real.

### Paso 8 — CI

Añade un job que ejecute `python -m pip install -r requirements.txt` y `python -m pytest -v` en la rama correcta.

### Paso 9 — Mantenimiento

Cuando cambies contratos de API (campos JSON, códigos HTTP), **actualiza los tests** en el mismo PR: los tests son parte del contrato público de tu servicio.

---

## 12. Resumen rápido

| Elemento | Para qué sirve |
|----------|----------------|
| **pytest** | Ejecutar y reportar `test_*`. |
| **`@pytest.fixture`** | Definir datos/cliente reutilizable (`client`). |
| **`TestClient(app)`** | Simular peticiones HTTP contra la app. |
| **`assert`** | Condición que debe cumplirse; si no, el test falla. |
| **`pytest.ini`** | Dónde buscar tests y cómo resolver imports. |

Con esto puedes **entender**, **ejecutar** y **replicar** el mismo estilo de pruebas en otros backends Python.
