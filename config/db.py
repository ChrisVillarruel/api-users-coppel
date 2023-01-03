import pymongo

USERNAME = "nico"
PASSWORD = "4busG15IKu9aqj66"
DATABASE = "miapp"

conn_str = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.h3y8s8p.mongodb.net/{DATABASE}?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
client.server_info()
