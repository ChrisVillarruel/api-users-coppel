from bson import ObjectId
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from config.backends import set_password, CreateJWTToken, get_password, DecodeJWTToken
from config.db import client as db

from producer import publish

router = APIRouter()


class RegisterUser(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    age: int
    token: str | None = None
    is_active: bool = False


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


async def data_user_info(user: dict):
    """ Información que se publicara en RabbitMQ """

    return {
        "user_id": str(user.get("_id")),
        "name": user.get("name"),
        "is_active": user.get("is_active"),
        "token": user.get("token"),
    }


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
        newvalues = {"$set": {'token': token, "is_active": True}}
        my_collection.update_one(query, newvalues)

        user = my_collection.find_one({"email": login.email})
        publish("user_login", await data_user_info(user))
        return {"status": f"Bienvenido {user.get('name')}!!!", "token": token}


async def verify_token(x_token: str):
    try:
        prefix = "Bearer"
        autorization_token = x_token.split(" ")
        prefix_token = autorization_token[0]
        token = autorization_token[1]

        my_db = db["miapp"]
        my_collection = my_db["users"]
        query = {"token": token}

        if len(autorization_token) > 2:
            newvalues = {"$set": {"is_active": False}}
            my_collection.update_one(query, newvalues)
            raise HTTPException(detail="Prefijo de token no valido", status_code=400)
        if prefix != prefix_token:
            newvalues = {"$set": {"is_active": False}}
            my_collection.update_one(query, newvalues)
            raise HTTPException(detail="Prefijo de token no valido", status_code=400)
        jwt_decode = DecodeJWTToken(token).decode_jwt()
        return jwt_decode.get("iss")
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    except Exception as e:
        raise HTTPException(detail=f"Error al autenticar su token", status_code=400)


async def user_data(user: dict):
    return {
        "id": str(user.get("_id")),
        "name": user.get("name"),
        "age": user.get("age"),
        "token": user.get("token"),
    }


@router.get("/user/")
async def user_info(x_token: str = Header()):
    user_id = await verify_token(x_token)
    my_db = db["miapp"]
    my_collection = my_db["users"]
    data = my_collection.find_one({'_id': ObjectId(user_id)})
    if not data:
        raise HTTPException(detail="Usuario no encontrado", status_code=400)
    return await user_data(data)
