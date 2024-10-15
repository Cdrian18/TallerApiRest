from fastapi import APIRouter, HTTPException, status
from utils.auth import create_recovery_token, verify_token
from utils.database import user_collection
from utils.email import send_email
from schemas.user import RecoverRequest
import bcrypt
from utils.logs import send_log

router = APIRouter()

@router.post("/password")
async def recover_password(request: RecoverRequest):
    try:
        user = await user_collection.find_one({"email": request.email})
        if not user:
            send_log(
                log_type="WARNING",
                module="AuthModule",
                summary="Intento de recuperación de contraseña fallido",
                description=f"El correo {request.email} no está registrado en el sistema"
            )
            raise HTTPException(status_code=404, detail="Correo no registrado")

        # Generar el token de recuperación
        recovery_token = create_recovery_token(user_id=str(user["public_id"]))
        recovery_link = f"http://localhost:8000/password?token={recovery_token}"

        # Enviar el correo de recuperación
        subject = "Recuperación de contraseña"
        body = f"Hola, usa el siguiente enlace para restablecer tu contraseña: {recovery_link}"
        await send_email(to_email=request.email, subject=subject, body=body)

        send_log(
            log_type="INFO",
            module="AuthModule",
            summary="Correo de recuperacion de contraseña exitosa",
            description=f"Se ha enviado un correo a {request.email} con las instrucciones de recuperacion de contraseña"
        )

        return {"message": "Se ha enviado un correo con las instrucciones de recuperación de contraseña"}
    except Exception as e:
        send_log(
            log_type="ERROR",
            module="AuthModule",
            summary="Error al recuperar la contraseña",
            description=f"Error durante la recuperación de contraseña: {e}"
        )
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/password")
async def reset_password(token: str, new_password: str):
    try:
        # Verificar el token de recuperación
        user_id = verify_token(token, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de recuperación inválido o expirado"
        ))

        send_log(
            log_type="INFO",
            module="AuthModule",
            summary="Token de recuperación verificado",
            description=f"Token verificado exitosamente para el usuario con ID {user_id}"
        )

        # Hashear la nueva contraseña
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Actualizar la contraseña en la base de datos
        update_result = await user_collection.update_one({"public_id": user_id}, {"$set": {"password": hashed_password}})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo restablecer la contraseña")

        send_log(
            log_type="INFO",
            module="AuthModule",
            summary="Contraseña restablecida con éxito",
            description=f"La contraseña ha sido actualizada correctamente para el usuario con ID {user_id}"
        )

        return {"message": "Contraseña restablecida con éxito"}

    except HTTPException as e:
        send_log(
            log_type="ERROR",
            module="AuthModule",
            summary="Error en el restablecimiento de la contraseña",
            description=f"Error durante el restablecimiento de contraseña: {e.detail}"
        )
        raise e
    except Exception as e:
        send_log(
            log_type="ERROR",
            module="AuthModule",
            summary="Error inesperado en el restablecimiento de la contraseña",
            description=f"Error inesperado durante el restablecimiento de la contraseña: {e}"
        )
        raise HTTPException(status_code=500, detail="Error interno del servidor")