# API Banco — Aplicación y Servicios Web

API REST con **FastAPI**, **SQLAlchemy** y **PostgreSQL** para gestión de usuarios, sucursales, tipos de cuenta, cuentas y transacciones. Incluye **validación de datos**, **manejo de errores unificado**, **estructuras de respuesta estándar** y **pipeline CI**.

---

## Contenido de la clase

- **Validación de datos** en servicios web (Pydantic, `Field`, validators).
- **Manejo de errores** centralizado y respuestas de error homogéneas.
- **Estructuras de respuesta** (éxito y error) en todos los endpoints.
- **Pipelines** (CI) con GitHub Actions: lint, formato y pruebas.

---

## Estructura del proyecto

```
├── src/
│   ├── app.py              # Aplicación FastAPI y manejadores globales
│   ├── core/               # Núcleo: excepciones y respuestas estándar
│   │   ├── exceptions.py   # Excepciones de negocio (NotFound, Conflict, BadRequest…)
│   │   ├── responses.py    # ApiResponse, ApiErrorDetail, success_response, error_response
│   │   └── error_handlers.py # Manejadores que traducen excepciones → JSON estándar
│   ├── database/          # Configuración PostgreSQL y sesión
│   ├── entities/          # Modelos SQLAlchemy (tablas)
│   ├── schemas/            # Modelos Pydantic (validación y serialización)
│   ├── endpoints/          # Rutas FastAPI por recurso
│   ├── crud/               # Cliente HTTP (httpx) que consume la API
│   └── utils/              # Utilidades (ej. hash de contraseñas)
├── main.py                 # Menú por consola que usa el CRUD contra la API
├── init_db.py              # Crear tablas en la base de datos
├── requirements.txt
├── .github/workflows/ci.yml # Pipeline CI (lint + smoke test)
└── README.md
```

---

## 1. Validación de datos

La validación se hace con **Pydantic** en `src/schemas/`:

- **Campos obligatorios y opcionales** con tipos claros (`str`, `UUID`, `Decimal`, `EmailStr`, etc.).
- **Restricciones con `Field()`**:
  - Longitud: `min_length`, `max_length` (nombre, usuario, contraseña, códigos, etc.).
  - Rangos: `ge=0` para saldos y montos positivos, `gt=0` para monto de transacción.
  - Patrones: `pattern=r"^[a-zA-Z0-9_.-]+$"` para nombre de usuario.
- **Validadores personalizados**: por ejemplo, en `UsuarioCreate` un `@field_validator` para que la contraseña no esté vacía.

Ejemplo (fragmento de `usuario_schema.py`):

```python
nombre_usuario: str = Field(
    ...,
    min_length=3,
    max_length=50,
    pattern=r"^[a-zA-Z0-9_.-]+$",
)
contraseña: str = Field(..., min_length=8, max_length=100)
```

Si los datos no cumplen las reglas, FastAPI devuelve **422** con el formato de error estándar (ver sección 3).

---

## 2. Manejo de errores

En `src/core/` se definen:

- **Excepciones de aplicación** (`exceptions.py`):
  - `NotFoundError` → 404
  - `ConflictError` → 409 (o 400 si se indica)
  - `BadRequestError` → 400
  - `ValidationError` → 422
- **Manejadores globales** (`error_handlers.py`):
  - `AppException` → respuesta JSON con código, mensaje y opcionalmente `details`.
  - `HTTPException` (FastAPI) → mismo formato.
  - `RequestValidationError` (Pydantic) → 422 con lista de errores en `details`.
  - Cualquier otra excepción → 500 con mensaje genérico.

Los endpoints usan `raise NotFoundError("Usuario no encontrado")` (y similares) en lugar de `HTTPException`; el manejador se encarga de devolver siempre la misma estructura de error.

---

## 3. Estructuras de respuesta

### Respuesta exitosa

Toda respuesta exitosa (excepto DELETE 204) tiene la forma:

```json
{
  "success": true,
  "data": { ... } | [ ... ],
  "message": "Mensaje opcional"
}
```

- `data`: recurso creado/actualizado, listado o único.
- `message`: texto breve (ej. "Usuario creado", "Listado de usuarios").

### Respuesta de error

Cualquier error (404, 400, 409, 422, 500) devuelve:

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Usuario no encontrado",
    "details": null
  }
}
```

- `code`: identificador del tipo de error (`NOT_FOUND`, `CONFLICT`, `BAD_REQUEST`, `VALIDATION_ERROR`, `INTERNAL_ERROR`, etc.).
- `message`: mensaje legible.
- `details`: opcional; en 422 suele ser la lista de errores de validación de Pydantic.

El cliente en `src/crud/client.py` extrae automáticamente `data` de las respuestas exitosas para que el resto del código siga trabajando con listas y diccionarios como antes.

---

## 4. Pipelines (CI)

En `.github/workflows/ci.yml` se define un pipeline que se ejecuta en **push** y **pull requests** a `main`/`master`:

1. **Checkout** del repositorio.
2. **Python 3.11** y caché de pip.
3. **Servicio PostgreSQL** para pruebas (con `SSL_MODE=disable` en CI).
4. **Instalación** de dependencias (`requirements.txt`) y **Ruff**.
5. **Lint**: `ruff check src`.
6. **Formato**: `ruff format src --check`.
7. **Creación de tablas**: `python init_db.py` contra la BD de prueba.
8. **Smoke test**: petición `GET /` y comprobación de que la respuesta tiene `success: true` y `data`.

Para usar Ruff en local (opcional):

```bash
pip install ruff
ruff check src
ruff format src
```

---

## Requisitos

- Python 3.10+
- PostgreSQL (por ejemplo [Neon](https://neon.tech) o local).
- Variable de entorno `DATABASE_URL`.

---

## Instalación

```bash
pip install -r requirements.txt
```

Crear `.env` en la raíz:

```env
DATABASE_URL=postgresql://usuario:contraseña@host/base?sslmode=require
```

Para entornos locales o CI sin SSL:

```env
SSL_MODE=disable
```

---

## Crear tablas

Ejecutar una vez (o cuando cambien las entidades):

```bash
python init_db.py
```

---

## Ejecución

1. **Levantar la API** (en una terminal):

```bash
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

2. **Menú por consola** (en otra terminal):

```bash
python main.py
```

El menú permite listar, crear, ver, actualizar y eliminar usuarios, sucursales, tipos de cuenta, cuentas, tipos de transacción y transacciones usando la API.

---

## Documentación de la API

Con la API en marcha:

- **Swagger UI**: http://localhost:8000/docs  
- **ReDoc**: http://localhost:8000/redoc  

---

## Resumen de buenas prácticas aplicadas

| Tema | Implementación |
|------|----------------|
| **Validación** | Schemas Pydantic con `Field`, patrones y validators en `src/schemas/`. |
| **Errores** | Excepciones en `src/core/exceptions.py` y manejadores en `error_handlers.py`. |
| **Respuestas** | `success_response()` y formato de error unificado en todos los endpoints. |
| **Pipeline** | GitHub Actions: lint (Ruff), formato y smoke test con PostgreSQL. |
