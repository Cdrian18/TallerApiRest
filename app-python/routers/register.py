from fastapi import APIRouter, HTTPException, status
from schemas.error import ErrorResponse
from schemas.user import User, PublicUser
from utils.database import user_collection, user_helper
import bcrypt
import uuid
from datetime import datetime, timezone

router = APIRouter()

# Helper para generar un UUID como public_id
def generate_public_id() -> str:
    return str(uuid.uuid4())

@router.post("/users", response_model=PublicUser, status_code=status.HTTP_201_CREATED,
            responses={
                400: {"model": ErrorResponse, "description": "Datos inválidos proporcionados."},
                409: {"model": ErrorResponse, "description": "Nombre de usuario o correo electrónico ya existen."},
                500: {"model": ErrorResponse, "description": "Error interno del servidor."}
            })
async def create_user(user: User):
    try:
        # Verificar si el usuario ya existe
        if (await user_collection.find_one({"email": user.email}) or await user_collection.find_one({"username": user.username})):
            raise HTTPException(status_code=409, detail="El usuario con este correo ya existe")

        # Convertir el modelo a un diccionario
        user_dict = user.model_dump()
        
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user_dict["password"] = hashed_password.decode('utf-8')
        
        # Generar un public_id seguro
        user_dict["public_id"] = generate_public_id()

        # Asignar la fecha y hora actuales a `created_at`
        user_dict["created_at"] = datetime.now(timezone.utc)
        
        # Insertar el usuario en la base de datos
        new_user = await user_collection.insert_one(user_dict)
        
        # Obtener el usuario recién creado
        created_user = await user_collection.find_one({"_id": new_user.inserted_id})
        
        return user_helper(created_user)
    
    except HTTPException as e:
        raise e  # Ya está manejado correctamente con el esquema de error

    except Exception as e:
        # Capturar cualquier otro error inesperado
        raise HTTPException(status_code=500, detail="Error interno del servidor")
