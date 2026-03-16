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
    "rol": "admin",
}


def get_or_create_admin(db) -> Usuario:
    """Crea el usuario admin si no existe y devuelve su instancia (para id_usuario_creacion)."""
    admin = db.query(Usuario).filter(Usuario.nombre_usuario == USUARIO_INICIAL["nombre_usuario"]).first()
    if admin:
        return admin
    u = USUARIO_INICIAL.copy()
    u["contraseña_hash"] = hash_password(u.pop("contraseña"))
    admin = Usuario(**u)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("  Usuario creado: admin")
    return admin


def seed_tipos_cuenta(db, id_usuario_creacion):
    for d in TIPOS_CUENTA:
        if db.query(TipoCuenta).filter(TipoCuenta.codigo == d["codigo"]).first():
            continue
        db.add(
            TipoCuenta(
                codigo=d["codigo"],
                nombre=d["nombre"],
                id_usuario_creacion=id_usuario_creacion,
            )
        )
        print(f"  Tipo cuenta creado: {d['codigo']}")
    db.commit()


def seed_tipos_transaccion(db, id_usuario_creacion):
    for d in TIPOS_TRANSACCION:
        if db.query(TipoTransaccion).filter(TipoTransaccion.codigo == d["codigo"]).first():
            continue
        db.add(
            TipoTransaccion(
                codigo=d["codigo"],
                nombre=d["nombre"],
                id_usuario_creacion=id_usuario_creacion,
            )
        )
        print(f"  Tipo transacción creado: {d['codigo']}")
    db.commit()


def seed_sucursal(db, id_usuario_creacion):
    if db.query(Sucursal).filter(Sucursal.nombre == SUCURSAL_INICIAL["nombre"]).first():
        return
    db.add(
        Sucursal(
            **SUCURSAL_INICIAL,
            id_usuario_creacion=id_usuario_creacion,
        )
    )
    db.commit()
    print("  Sucursal creada: Sucursal Principal")


def main():
    try:
        db = SessionLocal()
        try:
            print("Sembrando usuario admin (si no existe)...")
            admin = get_or_create_admin(db)
            id_creacion = admin.id_usuario

            print("Sembrando tipos de cuenta...")
            seed_tipos_cuenta(db, id_creacion)
            print("Sembrando tipos de transacción...")
            seed_tipos_transaccion(db, id_creacion)
            print("Sembrando sucursal inicial...")
            seed_sucursal(db, id_creacion)
            print("Seed completado.")
        finally:
            db.close()
    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
