from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from utils.config import MONGO_DETAILS
import logging

logging.basicConfig(level=logging.INFO)
# Crear el cliente de Motor
client = AsyncIOMotorClient(MONGO_DETAILS)

# Seleccionar la base de datos
database = client.userdb

# Seleccionar la colección de usuarios
user_collection = database.get_collection("users")

async def check_mongo_connection():
    try:
        logging.info(f"Conectando a MongoDB con: {MONGO_DETAILS}")
        await client.admin.command('ping')
        logging.info("Conexión exitosa a MongoDB")
    except Exception as e:
        logging.error(f"Error al conectar a MongoDB: {e}")

def user_helper(user) -> dict:
    return {
        "public_id": user.get("public_id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "created_at": user.get("created_at")
    }