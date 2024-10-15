from datetime import datetime, timezone
from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from typing import List, Optional
from utils.auth import get_current_user
from schemas.user import User, PublicUser
from schemas.error import ErrorResponse
from utils.database import user_collection, user_helper
from utils.logs import send_log

router = APIRouter()

@router.get("/users", response_model=dict)
async def list_users(
    request: Request,  
    page: int = Query(1, ge=1),  
    users_per_page: int = Query(2, ge=1, le=100), 
    timestamp: Optional[str] = None, 
    current_user: PublicUser = Depends(get_current_user) 
):
    if timestamp is None:
        from datetime import datetime, timezone
        timestamp = datetime.now(timezone.utc)

    total_users = await user_collection.count_documents({"created_at": {"$lte": timestamp}})

    total_pages = ceil(total_users / users_per_page)

    skip = (page - 1) * users_per_page
    users = []
    async for user in user_collection.find({"created_at": {"$lte": timestamp}}).skip(skip).limit(users_per_page):
        users.append(user_helper(user))

    base_url = str(request.url)
    next_page = f"{base_url}?page={page + 1}&users_per_page={users_per_page}" if page < total_pages else None
    previous_page = f"{base_url}?page={page - 1}&users_per_page={users_per_page}" if page > 1 else None

    send_log(
        log_type="INFO",
        module="UserModule",
        summary="Lista de usuarios solicitada",
        description=f"El usuario {current_user.username} solicitó la lista de usuarios, página {page}."
    )
    
    return {
        "page": page,
        "total_pages": total_pages,
        "total_users": total_users,
        "users_per_page": users_per_page,
        "users": users,
        "next_page": next_page,
        "previous_page": previous_page,
        "timestamp" : timestamp
    }

@router.get("/users/{public_id}", response_model=PublicUser)
async def read_user(public_id: str, current_user: PublicUser = Depends(get_current_user)):
    
    if current_user.public_id != public_id:
        send_log(
            log_type="WARNING",
            module="UserModule",
            summary="Acceso denegado",
            description=f"El usuario {current_user.username} intentó acceder a los datos del usuario {public_id} sin permiso."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(
                code=status.HTTP_403_FORBIDDEN,
                message="Acceso denegado",
                details="No tienes permiso para acceder a estos datos."
            ).model_dump(),
        )
    
    user = await user_collection.find_one({"public_id": public_id})
    if user is None:
        send_log(
            log_type="WARNING",
            module="UserModule",
            summary="Usuario no encontrado",
            description=f"El usuario con ID {public_id} no fue encontrado."
        )
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                code=status.HTTP_404_NOT_FOUND,
                message="Usuario no encontrado",
                details="No se encontró ningún usuario con el ID proporcionado."
            ).model_dump(),
        )
        
    send_log(
        log_type="INFO",
        module="UserModule",
        summary="Usuario leído correctamente",
        description=f"El usuario {current_user.username} accedió a los datos de {public_id}."
    )
    
    return user_helper(user)

@router.put("/users/{public_id}", response_model=PublicUser)
async def update_user(public_id: str, user: User, current_user: PublicUser = Depends(get_current_user)):
    # Verificar si el usuario autenticado está intentando actualizar sus propios datos
    if current_user.public_id != public_id:
        send_log(
            log_type="WARNING",
            module="UserModule",
            summary="Intento de actualización no autorizado",
            description=f"El usuario {current_user.username} intentó actualizar los datos de {public_id} sin permisos."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(
                code=status.HTTP_403_FORBIDDEN,
                message="Acceso denegado",
                details="No tienes permiso para actualizar estos datos."
            ).model_dump(),
        )

    # Buscar el usuario por el public_id
    existing_user = await user_collection.find_one({"public_id": public_id})
    if existing_user is None:
        send_log(
            log_type="WARNING",
            module="UserModule",
            summary="Usuario no encontrado",
            description=f"No se encontró ningún usuario con el ID {public_id} para actualizar."
        )
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                code=status.HTTP_404_NOT_FOUND,
                message="Usuario no encontrado",
                details="No se encontró ningún usuario con el ID proporcionado."
            ).model_dump(),
        )

    # Convertir el modelo a un diccionario y eliminar valores nulos
    user_model_dump = {k: v for k, v in user.model_dump().items() if v is not None}
    
    # Actualizar el usuario en la base de datos
    update_result = await user_collection.update_one({"public_id": public_id}, {"$set": user_model_dump})

    if update_result.modified_count == 1:
        updated_user = await user_collection.find_one({"public_id": public_id})
        
        if updated_user:
            send_log(
                log_type="INFO",
                module="UserModule",
                summary="Usuario actualizado correctamente",
                description=f"El usuario con ID {public_id} ha sido actualizado por {current_user.username}."
            )
            return user_helper(updated_user)
    
    return user_helper(existing_user)

@router.delete("/users/{public_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(public_id: str, current_user: PublicUser = Depends(get_current_user)):
    
    if current_user.public_id != public_id:
        send_log(
            log_type="WARNING",
            module="UserModule",
            summary="Intento de eliminación no autorizado",
            description=f"El usuario {current_user.username} intentó eliminar a {public_id} sin permisos."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(
                code=status.HTTP_403_FORBIDDEN,
                message="Acceso denegado",
                details="No tienes permiso para eliminar estos datos."
            ).model_dump(),
        )

    delete_result = await user_collection.delete_one({"public_id": public_id})
    if delete_result.deleted_count == 1:
        send_log(
            log_type="INFO",
            module="UserModule",
            summary="Usuario eliminado",
            description=f"El usuario con ID {public_id} fue eliminado por {current_user.username}."
        )
        return
    
    send_log(
        log_type="WARNING",
        module="UserModule",
        summary="Intento de eliminación fallido",
        description=f"El usuario con ID {public_id} no fue encontrado para eliminar."
    )
    raise HTTPException(
        status_code=404,
        detail=ErrorResponse(
            code=status.HTTP_404_NOT_FOUND,
            message="Usuario no encontrado",
            details="No se encontró ningún usuario con el ID proporcionado."
        ).model_dump(),
    )
