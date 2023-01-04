from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.backends import set_password
from config.db import client as db

router = APIRouter()


class RegisterUser(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    age: int
    token: str | None = None


@router.post('/register-user/')
async def register_user(user: RegisterUser):
    my_db = db["miapp"]
    my_collection = my_db["users"]
    if my_collection.find_one({"email": user.email}):
        raise HTTPException(detail="Ususario ya registrado", status_code=400)
    else:
        user.password = set_password(user.password)
        my_collection.insert_one(user.dict())
        return {"status": "Usuario creado exitosamente!"}
