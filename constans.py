from decouple import config

SYMMETRIC_JEY = config("SYMMETRIC_JEY")
DEFAULT_EXPIRATION_MINUTES = 30
JWT_KEY = config("JWT_KEY")

# MongoDB Atlas Access Database
USERNAME = config("USERNAME_DB")
PASSWORD = config("PASSWORD")
DATABASE = config("DATABASE")

# URL CloudAMQP Access
USERNAME_AMQP = config("USERNAME_AMQP")
PASSWORD_AMQP = config("PASSWORD_AMQP")
