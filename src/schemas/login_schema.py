from pydantic import BaseModel


class Login(BaseModel):
    nombre_usuario: str
    contraseña: str
