"""Punto de entrada para ejecutar solo la API con Uvicorn."""

import uvicorn


def main() -> None:
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
