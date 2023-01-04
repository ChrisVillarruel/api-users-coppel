import pymongo
from constans import USERNAME, PASSWORD, DATABASE

conn_str = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.h3y8s8p.mongodb.net/{DATABASE}?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=90000)
