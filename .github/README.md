# CI/CD y pipelines en este repositorio

Este documento describe qué son un **pipeline** y **CI/CD**, y cómo están configurados los workflows `ci_push.yml` y `ci_pr.yml` en `.github/workflows/`.

---

## Introducción

En este proyecto usamos **GitHub Actions** para ejecutar tareas automáticas cada vez que se sube código o se propone un cambio mediante un pull request. Esos flujos están definidos en archivos YAML dentro de `.github/workflows/`. No tienes que ejecutar a mano el lint, las comprobaciones de seguridad ni las pruebas básicas en el mismo orden cada vez: el servicio las corre por ti y deja el resultado visible en la pestaña **Actions** del repositorio.

---

## ¿Qué es un pipeline?

Un **pipeline** (tubería) es una secuencia **ordenada y automatizada** de pasos que se aplican al código o al entorno. Cada paso puede depender del anterior: por ejemplo, instalar dependencias → comprobar estilo → ejecutar pruebas. Si un paso falla, normalmente se detiene el flujo y se marca el conjunto como fallido. En GitHub Actions, ese pipeline se define en un **workflow** (un archivo YAML) con **jobs** (trabajos) y **steps** (pasos dentro de cada job).

---

## ¿Qué es CI/CD?

- **CI (Integración continua)**  
  Consiste en **integrar** el código de forma frecuente y **validarlo automáticamente**: formato, lint, análisis de dependencias vulnerables, pruebas, etc. Así se detectan errores antes de fusionar ramas o desplegar.

- **CD (Entrega o despliegue continuo)**  
  Va un paso más allá: **publicar** la aplicación en un entorno (staging, producción) de forma repetible, a menudo solo cuando el CI ha pasado. Este repositorio se centra sobre todo en **CI** (validación en GitHub). Un despliegue automático posterior sería una capa adicional de CD.

En conjunto, **CI/CD** nombra la idea de **automatizar** la calidad del software y, cuando aplica, su **entrega** a los entornos donde corre la aplicación.

---

## Comparación rápida

| Archivo        | Cuándo se ejecuta                         | Idea principal |
|----------------|--------------------------------------------|----------------|
| `ci_pull.yml`    | Pull requests hacia `dev`, `qa` o `prod`   | Validar el código del PR sin asumir migraciones ni seed contra un secreto de BD. |
| `ci_push.yml`  | Push a `dev`, `qa` o `prod`                | Tras integrar en esas ramas, además corre migración y seed usando el secreto `DATABASE_URL`. |

Ambos comparten **concurrencia** (`cancel-in-progress: true`): si llega un evento nuevo en la misma rama, se cancela una ejecución anterior aún en curso para no acumular jobs obsoletos.

---

## `on_pr.yml` — pull requests

**Disparador:** `pull_request` con rama base `dev`, `qa` o `prod`.

**Entorno de base de datos:** `DATABASE_URL` apunta a un **PostgreSQL 15** de prueba levantado como **service** en el runner (`localhost`, usuario/contraseña `test`, base `banco_test`). No se usan secretos del repositorio para la conexión en este flujo.

**Pasos principales:**

1. Checkout del código y Python 3.11.
2. Caché de pip e instalación de dependencias (`requirements.txt`, más `ruff` y `pip-audit`).
3. **Lint** con `ruff check src` (formato de salida compatible con anotaciones de GitHub).
4. **Formato** con `ruff format src --check`.
5. **Seguridad** con `pip-audit` sobre dependencias instaladas.
6. **Smoke test** con `TestClient` de FastAPI: la ruta raíz `/` debe responder 200 y un JSON con `success: true` y clave `data`.

No ejecuta `migrate_db.py` ni `seed_db.py`: el foco es revisar el PR de forma aislada y reproducible en CI.

---

## `on_push.yml` — push a ramas integradas

**Disparador:** `push` a `dev`, `qa` o `prod`.

**Base de datos:** `DATABASE_URL` se toma del **secret** `DATABASE_URL` en GitHub (Settings → Secrets and variables → Actions). Debe estar configurado para el entorno que corresponda a esa rama. También se levanta un contenedor **Postgres 15** como service (útil si parte del proceso sigue usando el mismo patrón que en local/CI).

**Pasos principales:**

1. Igual que en el PR: checkout, Python 3.11, caché, dependencias, `ruff` y `pip-audit`.
2. **Formato** con `ruff format src --check` (en esta versión del workflow **no** aparece el paso `ruff check` de lint).
3. `pip-audit`.
4. **Migración:** `python migrate_db.py`.
5. **Seed:** `python seed_db.py`.
6. Mismo **smoke test** que en `on_pr.yml`.

La intención es que, al integrar código en `dev` / `qa` / `prod`, el esquema y los datos iniciales previstos por el proyecto se apliquen contra la cadena definida en `DATABASE_URL`, además de las comprobaciones de formato y seguridad.

---

## Resumen

- **`on_pr.yml`:** CI en cada PR hacia `dev`, `qa` o `prod` — lint, formato, auditoría de paquetes y smoke test con BD de prueba en el runner.
- **`on_push.yml`:** CI al hacer push a esas mismas ramas — formato (sin `ruff check` en el YAML actual), auditoría, migración, seed y smoke test usando `secrets.DATABASE_URL`.

Para que `on_push.yml` complete los pasos de migración y seed hace falta que existan `migrate_db.py` y `seed_db.py` en la raíz del repositorio y que el secret `DATABASE_URL` esté correctamente definido.
