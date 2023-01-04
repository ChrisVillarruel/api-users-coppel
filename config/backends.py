from cryptography.fernet import Fernet
from constans import SYMMETRIC_JEY


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
