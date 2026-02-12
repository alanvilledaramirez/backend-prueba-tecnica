from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db = MongoDB()

async def connect_to_mongo():
    print(f"Conectando a mongo")
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    db.db = db.client[settings.MONGO_DB_NAME]
    print("Conectado a mongo exitosa")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Se cierra la conexion a mongo")

def get_audit_collection():
    return db.db["audit_logs"]