# Autenticación JWT y CORS en la API Banco

Este documento describe cómo está configurada la **autenticación con JWT** y el **CORS** en el proyecto, qué variables de entorno usar y cómo consumir la API desde un cliente (navegador u otra aplicación).

---

## JWT (JSON Web Token)

### Qué problema resuelve

Las rutas de negocio (cuentas, sucursales, transacciones, etc.) exigen que el cliente demuestre **quién es** sin enviar la contraseña en cada petición. Tras un login correcto, la API devuelve un **token firmado** (JWT). El cliente lo guarda y lo envía en la cabecera `Authorization` hasta que expire o el usuario cierre sesión.

### Flujo resumido

1. El cliente hace `POST /usuarios/login` con `nombre_usuario` y `contraseña`.
2. Si el usuario existe, la contraseña es válida y el usuario está **activo**, la respuesta incluye (dentro de `data`) `access_token`, `token_type` (`bearer`), `expires_in` (segundos), `id_usuario`, `rol`, etc.
3. En las rutas protegidas, el cliente envía:  
   `Authorization: Bearer <access_token>`.

### Claims incluidos en el token

El token se firma con **HS256** e incluye entre otros: `sub` (UUID del usuario), `nombre_usuario`, `rol`, `iat` y `exp`. La dependencia `get_current_user` en `src/core/auth.py` valida la firma, la expiración y que el usuario siga existiendo y **activo** en base de datos.

### Variables de entorno (JWT)

| Variable | Descripción |
|----------|-------------|
| `JWT_SECRET_KEY` | Clave secreta para firmar y verificar tokens. En producción debe ser larga y aleatoria (por ejemplo `openssl rand -hex 32`). Si no se define, el proyecto usa un valor solo para desarrollo (no usar en producción). |
| `JWT_ALGORITHM` | Por defecto `HS256`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos (entre 5 y 1440). Por defecto `60`. |

Carga típica desde un archivo `.env` en la raíz del proyecto (véase `src/core/config.py`).

### Rutas públicas y protegidas

- **Sin token:** `GET /`, `POST /usuarios/login`, `POST /usuarios` (registro de usuario).
- **Con token:** el resto de endpoints de la API (incluidos listado, detalle, actualización y borrado de usuarios; no el alta por `POST /usuarios`).

### Código relevante

- `src/core/config.py` — ajustes JWT y CORS.
- `src/core/auth.py` — creación del token, `get_current_user`, modelo `CurrentUser`.
- `src/endpoints/login.py` — emisión del token tras login.
- `src/crud/client.py` — el cliente de consola guarda el token y lo envía en las peticiones HTTP.

### Errores habituales

- **401** — Falta cabecera, token inválido, expirado o usuario inactivo/eliminado.
- Recordar el prefijo exacto: `Bearer ` (con espacio) antes del token.

---

## CORS (Cross-Origin Resource Sharing)

### Qué problema resuelve

Si el **front** (por ejemplo React en `http://localhost:5173`) llama a la API en otro origen (por ejemplo `http://localhost:8000`), el navegador aplica la política de mismo origen. Sin CORS, esas peticiones fallan. El middleware CORS indica al navegador qué **orígenes** pueden leer respuestas de la API y qué **cabeceras** y **métodos** están permitidos en las peticiones preflight (`OPTIONS`).

### Configuración en este proyecto

En `src/app.py` se añade `CORSMiddleware` con:

- `allow_origins`: lista obtenida de la variable de entorno `CORS_ORIGINS` (orígenes separados por coma; sin espacios problemáticos tras el split).
- `allow_credentials=True`: permite cookies o credenciales en peticiones cross-origin cuando el cliente las use. **Importante:** con `allow_credentials=True` no se puede usar `*` como origen; hay que enumerar orígenes concretos.

| Variable | Descripción |
|----------|-------------|
| `CORS_ORIGINS` | Lista separada por comas, por ejemplo `http://localhost:3000,http://localhost:5173`. Valores por defecto en código incluyen puertos típicos de desarrollo. |

Métodos permitidos: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`.  
Cabeceras permitidas: `Authorization`, `Content-Type`, `Accept`.

### Frontends y JWT

El navegador enviará la cabecera `Authorization` en peticiones cross-origin solo si el origen del front está en `CORS_ORIGINS` y la configuración CORS lo permite (como en este proyecto).

---

## Ejemplo mínimo (fetch)

```javascript
const res = await fetch("http://localhost:8000/usuarios/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nombre_usuario: "...", contraseña: "..." }),
});
const body = await res.json();
const token = body.data.access_token;

await fetch("http://localhost:8000/cuentas", {
  headers: { Authorization: `Bearer ${token}` },
});
```

(Ajusta URLs y manejo de errores según tu entorno.)

---

## Documentación relacionada

- Pipelines CI/CD del repositorio: `.github/README.md`.
