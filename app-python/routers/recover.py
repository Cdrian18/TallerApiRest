from fastapi import APIRouter, HTTPException, status
from utils.auth import create_recovery_token, verify_token
from utils.database import user_collection
from utils.email import send_email
from schemas.user import RecoverRequest
import bcrypt

router = APIRouter()

@router.post("/password")
async def recover_password(request: RecoverRequest):
    user = await user_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="Correo no registrado")

    # Generar el token de recuperación
    recovery_token = create_recovery_token(user_id=str(user["public_id"]))
    recovery_link = f"http://localhost:8000/password?token={recovery_token}"

    # Enviar el correo de recuperación
    subject = "Recuperación de contraseña"
    body = f"Hola, usa el siguiente enlace para restablecer tu contraseña: {recovery_link}"
    await send_email(to_email=request.email, subject=subject, body=body)

    return {"message": "Se ha enviado un correo con las instrucciones de recuperación de contraseña"}

@router.put("/password")
async def reset_password(token: str, new_password: str):
    # Verificar el token de recuperación
    user_id = verify_token(token, HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token de recuperación inválido o expirado"
    ))

    # Hashear la nueva contraseña
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Actualizar la contraseña en la base de datos
    update_result = await user_collection.update_one({"public_id": user_id}, {"$set": {"password": hashed_password}})
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo restablecer la contraseña")

    return {"message": "Contraseña restablecida con éxito"}
