"""
Menú por consola que usa el CRUD (cliente de la API).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""
import sys
import threading
import time

# Permitir importar desde src cuando se ejecuta desde la raíz del proyecto
sys.path.insert(0, ".")

from src.crud import (
    listar_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    listar_productos,
    obtener_producto,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
)


def mostrar_usuarios():
    try:
        usuarios = listar_usuarios()
        if not usuarios:
            print("  No hay usuarios.")
            return
        for u in usuarios:
            print(f"  {u['id']} | {u['nombre_usuario']} | {u['email']} | activo={u['activo']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")


def mostrar_productos():
    try:
        productos = listar_productos()
        if not productos:
            print("  No hay productos.")
            return
        for p in productos:
            print(f"  {p['id_producto']} | {p['nombre']} | {p.get('descripcion') or '-'}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")


def menu_usuarios():
    while True:
        print("\n--- Usuarios ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_usuarios()
        elif op == "2":
            uid = input("ID usuario: ").strip()
            if uid:
                try:
                    u = obtener_usuario(uid)
                    print(f"  {u}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            nombre = input("Nombre: ").strip()
            nombre_usuario = input("Nombre usuario: ").strip()
            email = input("Email: ").strip()
            contraseña = input("Contraseña: ").strip()
            if nombre and nombre_usuario and email and contraseña:
                try:
                    crear_usuario(nombre, nombre_usuario, email, contraseña)
                    print("  Usuario creado.")
                except Exception as e:
                    print(f"  Error: {e}")
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
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID usuario a eliminar: ").strip()
            if uid:
                try:
                    eliminar_usuario(uid)
                    print("  Usuario eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_productos():
    while True:
        print("\n--- Productos ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_productos()
        elif op == "2":
            pid = input("ID producto: ").strip()
            if pid:
                try:
                    p = obtener_producto(pid)
                    print(f"  {p}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            nombre = input("Nombre producto: ").strip()
            id_usuario = input("ID usuario creador: ").strip()
            desc = input("Descripción (opcional): ").strip() or None
            if nombre and id_usuario:
                try:
                    crear_producto(nombre, id_usuario, desc)
                    print("  Producto creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan nombre o ID usuario.")
        elif op == "4":
            pid = input("ID producto: ").strip()
            if not pid:
                continue
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            desc = input("Descripción (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if desc:
                    kwargs["descripcion"] = desc
                actualizar_producto(pid, **kwargs)
                print("  Producto actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            pid = input("ID producto a eliminar: ").strip()
            if pid:
                try:
                    eliminar_producto(pid)
                    print("  Producto eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def _iniciar_api():
    """Ejecuta uvicorn en un hilo en segundo plano."""
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="warning")


def main():
    print("API Usuarios y Productos - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_iniciar_api, daemon=True)
    server.start()
    time.sleep(1.5)
    print("API lista.\n")
    while True:
        print("\n========== MENÚ ==========")
        print("1. Usuarios  2. Productos  0. Salir")
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        if op == "1":
            menu_usuarios()
        elif op == "2":
            menu_productos()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
