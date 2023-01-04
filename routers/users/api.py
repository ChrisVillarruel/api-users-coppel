from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.backends import set_password, CreateJWTToken, get_password
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


class Login(BaseModel):
    email: str
    password: str


@router.post("/login/")
async def login_user(login: Login):
    my_db = db["miapp"]
    my_collection = my_db["users"]
    user = my_collection.find_one({"email": login.email})

    if not user:
        raise HTTPException(detail="Ususario no registrado", status_code=400)
    elif not get_password(user.get("password"), login.password):
        raise HTTPException(detail="Dirección de correo electronico y/o contraseña no valido", status_code=400)
    else:
        token = CreateJWTToken(user_id=str(user.get("_id"))).create_jwt()
        query = {"_id": user.get("_id")}
        newvalues = {"$set": {'token': token}}
        my_collection.update_one(query, newvalues)
        return {"status": f"Bienvenido {user.get('name')}!!!", "token": token}
