"""
Seeder: datos iniciales para dev/QA/prod.
Idempotente: no duplica registros si ya existen (por codigo o identificador).

Uso:
  python seed_db.py

Requiere DATABASE_URL. Ejecutar después de migrate_db.py.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from sqlalchemy.exc import OperationalError

from src.database.config import SessionLocal
from src.entities.tipo_cuenta import TipoCuenta
from src.entities.tipo_transaccion import TipoTransaccion
from src.entities.sucursal import Sucursal
from src.entities.usuarios import Usuario
from src.utils.security import hash_password

# Datos a insertar si no existen
TIPOS_CUENTA = [
    {"codigo": "AHORRO", "nombre": "Cuenta de ahorros"},
    {"codigo": "CORRIENTE", "nombre": "Cuenta corriente"},
]

TIPOS_TRANSACCION = [
    {"codigo": "CONSIGNACION", "nombre": "Consignación"},
    {"codigo": "RETIRO", "nombre": "Retiro"},
    {"codigo": "TRANSFERENCIA", "nombre": "Transferencia"},
]

SUCURSAL_INICIAL = {
    "nombre": "Sucursal Principal",
    "direccion": "Calle 1 # 2-3",
    "ciudad": "Medellín",
    "telefono": "+57 4 123 4567",
}

USUARIO_INICIAL = {
    "nombre": "Admin",
    "nombre_usuario": "admin",
    "email": "admin@banco.local",
    "contraseña": "Admin123!",  # Cambiar en prod
}


def seed_tipos_cuenta(db):
    for d in TIPOS_CUENTA:
        if db.query(TipoCuenta).filter(TipoCuenta.codigo == d["codigo"]).first():
            continue
        db.add(TipoCuenta(codigo=d["codigo"], nombre=d["nombre"]))
        print(f"  Tipo cuenta creado: {d['codigo']}")
    db.commit()


def seed_tipos_transaccion(db):
    for d in TIPOS_TRANSACCION:
        if db.query(TipoTransaccion).filter(TipoTransaccion.codigo == d["codigo"]).first():
            continue
        db.add(TipoTransaccion(codigo=d["codigo"], nombre=d["nombre"]))
        print(f"  Tipo transacción creado: {d['codigo']}")
    db.commit()


def seed_sucursal(db):
    if db.query(Sucursal).filter(Sucursal.nombre == SUCURSAL_INICIAL["nombre"]).first():
        return
    db.add(Sucursal(**SUCURSAL_INICIAL))
    db.commit()
    print("  Sucursal creada: Sucursal Principal")


def seed_usuario(db):
    u = USUARIO_INICIAL.copy()
    if db.query(Usuario).filter(Usuario.nombre_usuario == u["nombre_usuario"]).first():
        return
    u["contraseña_hash"] = hash_password(u.pop("contraseña"))
    db.add(Usuario(**u))
    db.commit()
    print("  Usuario creado: admin")


def main():
    try:
        db = SessionLocal()
        try:
            print("Sembrando tipos de cuenta...")
            seed_tipos_cuenta(db)
            print("Sembrando tipos de transacción...")
            seed_tipos_transaccion(db)
            print("Sembrando sucursal inicial...")
            seed_sucursal(db)
            print("Sembrando usuario inicial...")
            seed_usuario(db)
            print("Seed completado.")
        finally:
            db.close()
    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
