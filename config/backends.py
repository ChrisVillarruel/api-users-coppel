import datetime as dt
from typing import ClassVar

import jwt

from cryptography.fernet import Fernet
from constans import SYMMETRIC_JEY, DEFAULT_EXPIRATION_MINUTES, JWT_KEY


def set_password(user_password: str) -> str:
    fernet = Fernet(SYMMETRIC_JEY.encode("utf-8"))
    hash_user_password = fernet.encrypt(user_password.encode("utf-8"))
    return hash_user_password.decode()


def get_password(hash_user_password: str, user_password) -> bool:
    fernet = Fernet(SYMMETRIC_JEY.encode("utf-8"))
    decrypt_password = fernet.decrypt(hash_user_password)
    if decrypt_password.decode() == user_password:
        return True
    return False


class CreateJWTToken:
    _DEFAULT_EXPIRATION_MINUTES: ClassVar[int] = DEFAULT_EXPIRATION_MINUTES

    def __init__(self, user_id: str):
        self.user_id = user_id

    @staticmethod
    def _unix_time(date_time: dt.datetime):
        return dt.datetime.timestamp(date_time)

    @property
    def payload(self) -> dict:
        return {
            "iss": self.user_id,
            "exp": self._unix_time(dt.datetime.now() + dt.timedelta(minutes=self._DEFAULT_EXPIRATION_MINUTES)),
            "iat": self._unix_time(dt.datetime.now())
        }

    @property
    def headers(self) -> dict:
        return {
            "alg": "HS256",
            "typ": "JWT"
        }

    def create_jwt(self) -> str:
        return jwt.encode(
            payload=self.payload,
            headers=self.headers,
            key=JWT_KEY
        )


class DecodeJWTToken:
    def __init__(self, jwt_token: str):
        self.jwt_token = jwt_token

    def decode_jwt(self) -> dict:
        try:
            return jwt.decode(jwt=self.jwt_token, key=JWT_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError as _:
            raise ValueError("El token de acceso ya expiro")
        except jwt.exceptions as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(str(e))
