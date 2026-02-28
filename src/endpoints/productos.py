from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.producto import Producto
from src.entities.usuarios import Usuario
from src.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("", response_model=ProductoResponse, status_code=201)
def crear_producto(dato: ProductoCreate, db: Session = Depends(get_db)):
    if db.query(Producto).filter(Producto.nombre == dato.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")
    usuario = db.query(Usuario).filter(Usuario.id == dato.id_usuario_crea).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario creador no encontrado")
    producto = Producto(
        nombre=dato.nombre,
        descripcion=dato.descripcion,
        id_usuario_crea=dato.id_usuario_crea,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: UUID, dato: ProductoUpdate, db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(producto, k, v)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return None
