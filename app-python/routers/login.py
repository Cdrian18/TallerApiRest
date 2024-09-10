import bcrypt
from fastapi import APIRouter, HTTPException, status
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
from utils.database import user_collection
from schemas.user import LoginRequest
from schemas.error import ErrorResponse

router = APIRouter()

@router.post("/login", response_model=dict,
            responses={
                200: {
                    "description": "Autenticación exitosa",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "token": {
                                        "type": "string",
                                        "description": "Token JWT de autenticación"
                                    }
                                }
                            }
                        }
                    }
                },
                400: {"model": ErrorResponse, "description": "Solicitud inválida"},
                401: {"model": ErrorResponse, "description": "Credenciales incorrectas"},
                500: {"model": ErrorResponse, "description": "Error interno del servidor"}
            })
async def login_user(form_data: LoginRequest):
    try:
        # Buscar al usuario por nombre de usuario
        user = await user_collection.find_one({"username": form_data.username})
        
        # Verificar las credenciales
        if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crear el token de acceso
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user["public_id"]}, expires_delta=access_token_expires)
        
        # Devolver el token de acceso
        return {"token": access_token}

    except HTTPException as e:
        raise e  # Manejo de excepción ya gestionada

    except Exception as e:
        # Capturar cualquier otro error inesperado
        raise HTTPException(status_code=500, detail="Error interno del servidor")
