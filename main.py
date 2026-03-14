"""
Menú por consola que usa el CRUD (cliente de la API Banco).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""

import sys
import threading
import time

sys.path.insert(0, ".")
id_usuario_actual = None

from src.crud import (
    actualizar_cuenta,
    actualizar_sucursal,
    actualizar_tipo_cuenta,
    actualizar_tipo_transaccion,
    actualizar_transaccion,
    actualizar_usuario,
    crear_cuenta,
    crear_sucursal,
    crear_tipo_cuenta,
    crear_tipo_transaccion,
    crear_transaccion,
    crear_usuario,
    eliminar_cuenta,
    eliminar_sucursal,
    eliminar_tipo_cuenta,
    eliminar_tipo_transaccion,
    eliminar_transaccion,
    eliminar_usuario,
    listar_cuentas,
    listar_sucursales,
    listar_tipos_cuenta,
    listar_tipos_transaccion,
    listar_transacciones,
    listar_usuarios,
    obtener_cuenta,
    obtener_sucursal,
    obtener_tipo_cuenta,
    obtener_tipo_transaccion,
    obtener_transaccion,
    obtener_usuario,
    login,
)


def _err_conexion(e):
    err = str(e)
    if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
        print(
            "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
        )
    else:
        print(f"  Error: {e}")


def menu_login():
    global id_usuario_actual
    while True:
        print("\n--- LOGUEO BANCO ---")
        print(" ¿Tienes cuenta?")
        print("1. Si   2. No   0. Cancelar")
        op = input("Opción: ").strip()
        if op == "0":
            return False
        if op == "1":
            nombre_usuario = input("Nombre usuario: ").strip()
            contraseña = input("Contraseña: ").strip()
            if nombre_usuario and contraseña:
                try:
                    confirma_login = login(nombre_usuario, contraseña)
                    if confirma_login.get("resultado") == "Login exitoso":
                        print(" Logueo exitoso")
                        id_usuario_actual = confirma_login.get("id_usuario")
                        return True
                    else:
                        print("Error en el login: ", confirma_login)
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan datos.")
        elif op == "2":
            print(" Por favor crea tu usuario:")
            nombre = input("Nombre: ").strip()
            nombre_usuario = input("Nombre usuario: ").strip()
            email = input("Email: ").strip()
            contraseña = input("Contraseña: ").strip()
            rol = input("Rol (admin/cliente): ").strip()
            telefono = input("Teléfono: ").strip()
            if nombre and nombre_usuario and email and contraseña and rol and telefono:
                try:
                    crear_usuario(
                        nombre, nombre_usuario, email, telefono, contraseña, rol
                    )
                    print("  Usuario creado.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan datos.")


def menu_usuarios() -> None:
    while True:
        print("\n--- Usuarios ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            try:
                usuarios = listar_usuarios()
                if not usuarios:
                    print("  No hay usuarios.")
                else:
                    for u in usuarios:
                        print(
                            f"  {u['id_usuario']} | {u['nombre_usuario']} | {u['email']} | rol={u['rol']} | tel={u['telefono']} | activo={u['activo']}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif op == "2":
            uid = input("ID usuario: ").strip()
            if uid:
                try:
                    u = obtener_usuario(uid)
                    print(f"  {u}")
                except Exception as e:
                    _err_conexion(e)
        elif op == "3":
            nombre = input("Nombre: ").strip()
            nombre_usuario = input("Nombre usuario: ").strip()
            email = input("Email: ").strip()
            contraseña = input("Contraseña: ").strip()
            rol = input("Rol (admin/cliente): ").strip()
            telefono = input("Teléfono: ").strip()
            if nombre and nombre_usuario and email and contraseña and rol and telefono:
                try:
                    crear_usuario(
                        nombre, nombre_usuario, email, telefono, contraseña, rol
                    )
                    print("  Usuario creado.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan datos.")
        elif op == "4":
            uid = input("ID usuario: ").strip()
            if not uid:
                continue
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            email = input("Email (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if email:
                    kwargs["email"] = email
                actualizar_usuario(uid, **kwargs)
                print("  Usuario actualizado.")
            except Exception as e:
                _err_conexion(e)
        elif op == "5":
            uid = input("ID usuario a eliminar: ").strip()
            if uid:
                try:
                    eliminar_usuario(uid)
                    print("  Usuario eliminado.")
                except Exception as e:
                    _err_conexion(e)


def menu_sucursales():
    while True:
        print("\n--- Sucursales ---")
        print("1. Listar  2. Ver una  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            try:
                items = listar_sucursales()
                if not items:
                    print("  No hay sucursales.")
                else:
                    for s in items:
                        print(
                            f"  {s['id_sucursal']} | {s['nombre']} | {s.get('ciudad') or '-'}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif op == "2":
            sid = input("ID sucursal: ").strip()
            if sid:
                try:
                    print(obtener_sucursal(sid))
                except Exception as e:
                    _err_conexion(e)
        elif op == "3":
            nombre = input("Nombre sucursal: ").strip()
            if nombre:
                try:
                    crear_sucursal(
                        nombre,
                        id_usuario_actual,
                        input("Dirección (opcional): ").strip() or None,
                        input("Ciudad (opcional): ").strip() or None,
                        input("Teléfono (opcional): ").strip() or None,
                    )
                    print("  Sucursal creada.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Falta nombre.")
        elif op == "4":
            sid = input("ID sucursal: ").strip()
            if not sid:
                continue
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            try:
                actualizar_sucursal(
                    sid,
                    nombre=nombre if nombre else None,
                    id_usuario_edita=id_usuario_actual,
                )
                print("  Sucursal actualizada.")
            except Exception as e:
                _err_conexion(e)
        elif op == "5":
            sid = input("ID sucursal a eliminar: ").strip()
            if sid:
                try:
                    eliminar_sucursal(sid)
                    print("  Sucursal eliminada.")
                except Exception as e:
                    _err_conexion(e)


def menu_tipos_cuenta():
    while True:
        print("\n--- Tipos de cuenta ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            try:
                items = listar_tipos_cuenta()
                if not items:
                    print("  No hay tipos de cuenta.")
                else:
                    for t in items:
                        print(
                            f"  {t['id_tipo_cuenta']} | {t['codigo']} | {t['nombre']}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif op == "2":
            tid = input("ID tipo: ").strip()
            if tid:
                try:
                    print(obtener_tipo_cuenta(tid))
                except Exception as e:
                    _err_conexion(e)
        elif op == "3":
            codigo = input("Código: ").strip()
            nombre = input("Nombre (ej. Ahorros): ").strip()
            if codigo and nombre:
                try:
                    crear_tipo_cuenta(codigo, nombre, id_usuario_actual)
                    print("  Tipo de cuenta creado.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan código o nombre.")
        elif op == "4":
            tid = input("ID tipo cuenta: ").strip()
            if not tid:
                continue
            codigo = input("Código (vacío=no cambiar): ").strip()
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            try:
                actualizar_tipo_cuenta(
                    tid,
                    codigo=codigo or None,
                    nombre=nombre or None,
                    id_usuario_edita=id_usuario_actual,
                )
                print("  Tipo de cuenta actualizado.")
            except Exception as e:
                _err_conexion(e)
        elif op == "5":
            tid = input("ID tipo a eliminar: ").strip()
            if tid:
                try:
                    eliminar_tipo_cuenta(tid)
                    print("  Tipo de cuenta eliminado.")
                except Exception as e:
                    _err_conexion(e)


def menu_cuentas():
    while True:
        print("\n--- Cuentas ---")
        print("1. Listar  2. Ver una  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            try:
                items = listar_cuentas()
                if not items:
                    print("  No hay cuentas.")
                else:
                    for c in items:
                        print(
                            f"  {c['id_cuenta']} | {c['numero_cuenta']} | saldo={c['saldo']}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif op == "2":
            cid = input("ID cuenta: ").strip()
            if cid:
                try:
                    print(obtener_cuenta(cid))
                except Exception as e:
                    _err_conexion(e)
        elif op == "3":
            num = input("Número de cuenta: ").strip()
            uid = input("ID usuario (titular): ").strip()
            sid = input("ID sucursal: ").strip()
            tid = input("ID tipo cuenta: ").strip()
            saldo = input("Saldo inicial (0): ").strip() or "0"
            if num and uid and sid and tid:
                try:
                    crear_cuenta(num, uid, sid, tid, saldo, id_usuario_actual)
                    print("  Cuenta creada.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan datos.")
        elif op == "4":
            cid = input("ID cuenta: ").strip()
            if not cid:
                continue
            saldo = input("Nuevo saldo (vacío=no cambiar): ").strip()
            try:
                actualizar_cuenta(
                    cid,
                    saldo=saldo if saldo else None,
                    id_usuario_edita=id_usuario_actual,
                )
                print("  Cuenta actualizada.")
            except Exception as e:
                _err_conexion(e)
        elif op == "5":
            cid = input("ID cuenta a eliminar: ").strip()
            if cid:
                try:
                    eliminar_cuenta(cid)
                    print("  Cuenta eliminada.")
                except Exception as e:
                    _err_conexion(e)


def menu_tipos_transaccion():
    while True:
        print("\n--- Tipos de transacción ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            try:
                items = listar_tipos_transaccion()
                if not items:
                    print("  No hay tipos de transacción.")
                else:
                    for t in items:
                        print(
                            f"  {t['id_tipo_transaccion']} | {t['codigo']} | {t['nombre']}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif op == "2":
            tid = input("ID tipo: ").strip()
            if tid:
                try:
                    print(obtener_tipo_transaccion(tid))
                except Exception as e:
                    _err_conexion(e)
        elif op == "3":
            codigo = input("Código: ").strip()
            nombre = input("Nombre (ej. Depósito): ").strip()
            if codigo and nombre:
                try:
                    crear_tipo_transaccion(codigo, nombre, id_usuario_actual)
                    print("  Tipo de transacción creado.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan código o nombre.")
        elif op == "4":
            tid = input("ID tipo de transacción: ").strip()
            if not tid:
                continue
            codigo = input("Código (vacío=no cambiar): ").strip()
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            try:
                actualizar_tipo_transaccion(
                    tid,
                    codigo=codigo or None,
                    nombre=nombre or None,
                    id_usuario_edita=id_usuario_actual,
                )
                print("  Tipo de transacción actualizado.")
            except Exception as e:
                _err_conexion(e)
        elif op == "5":
            tid = input("ID tipo de transacción a eliminar: ").strip()
            if tid:
                try:
                    eliminar_tipo_transaccion(tid)
                    print("  Tipo de transacción eliminada.")
                except Exception as e:
                    _err_conexion(e)


def menu_transacciones():
    while True:
        print("\n--- Transacciones ---")
        print("1. Listar  2. Ver una  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            try:
                items = listar_transacciones()
                if not items:
                    print("  No hay transacciones.")
                else:
                    for t in items:
                        print(
                            f"  {t['id_transacciones']} | cuenta={t['id_cuenta']} | monto={t['monto']} | {t.get('fecha')}"
                        )
            except Exception as e:
                _err_conexion(e)
        elif op == "2":
            tid = input("ID transacción: ").strip()
            if tid:
                try:
                    print(obtener_transaccion(tid))
                except Exception as e:
                    _err_conexion(e)
        elif op == "3":
            cid = input("ID cuenta: ").strip()
            ttid = input("ID tipo transacción: ").strip()
            monto = input("Monto: ").strip()
            cid_dest = (
                input("ID cuenta destino (opcional, transferencias): ").strip() or None
            )
            desc = input("Descripción (opcional): ").strip() or None
            if cid and ttid and monto:
                try:
                    crear_transaccion(
                        cid, ttid, monto, cid_dest, desc, id_usuario_actual
                    )
                    print("  Transacción creada.")
                except Exception as e:
                    _err_conexion(e)
            else:
                print("  Faltan cuenta, tipo o monto.")
        elif op == "4":
            tid = input("ID transacción: ").strip()
            if not tid:
                continue
            desc = input("Descripción (vacío=no cambiar): ").strip()
            try:
                actualizar_transaccion(
                    tid,
                    descripcion=desc if desc else None,
                    id_usuario_edita=id_usuario_actual,
                )
                print("  Transacción actualizada.")
            except Exception as e:
                _err_conexion(e)
        elif op == "5":
            tid = input("ID transacción a eliminar: ").strip()
            if tid:
                try:
                    eliminar_transaccion(tid)
                    print("  Transacción eliminada.")
                except Exception as e:
                    _err_conexion(e)


def _iniciar_api():
    import uvicorn

    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="warning")


def main():
    print("API Banco - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_iniciar_api, daemon=True)
    server.start()
    time.sleep(1.5)
    print("API lista.\n")

    if not menu_login():
        print("No se inició sesión")
        return
    while True:
        print("\n========== MENÚ BANCO ==========")
        print(
            "1. Usuarios  2. Sucursales  3. Tipos cuenta  4. Cuentas  5. Tipos transacción  6. Transacciones  0. Salir"
        )
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        if op == "1":
            menu_usuarios()
        elif op == "2":
            menu_sucursales()
        elif op == "3":
            menu_tipos_cuenta()
        elif op == "4":
            menu_cuentas()
        elif op == "5":
            menu_tipos_transaccion()
        elif op == "6":
            menu_transacciones()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
