from decouple import config

SYMMETRIC_JEY = config("SYMMETRIC_JEY")
DEFAULT_EXPIRATION_MINUTES = 30
JWT_KEY = config("JWT_KEY")

USERNAME = config("USERNAME")
PASSWORD = config("PASSWORD")
DATABASE = config("DATABASE")
