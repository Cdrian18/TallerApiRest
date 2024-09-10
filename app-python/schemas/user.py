from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from fastapi import HTTPException
import re
from schemas.error import ErrorResponse 

# Schema para la creación y actualización de usuarios
class User(BaseModel):
    username: str = Field(..., min_length=3, example="user123")
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="StrongPassword123!")
    created_at: Optional[datetime] = Field(None, example="2023-09-02T00:00:00Z")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user123",
                "email": "user@example.com",
                "password": "StrongPassword123!",
                "created_at": "2023-09-02T00:00:00Z"
            }
        }

# Schema para la respuesta pública del usuario
class PublicUser(BaseModel):
    public_id: str = Field(..., example="e137c3e6-4121-48a7-8c6d-c4e7d623b255")
    username: str = Field(..., example="user123")
    email: EmailStr = Field(..., example="user@example.com")
    created_at: Optional[datetime] = Field(None, example="2023-09-02T00:00:00Z")

    class Config:
        json_schema_extra = {
            "example": {
                "public_id": "e137c3e6-4121-48a7-8c6d-c4e7d623b255",
                "username": "user123",
                "email": "user@example.com",
                "created_at": "2023-09-02T00:00:00Z"
            }
        }

# Schema para la solicitud de login
class LoginRequest(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(
        ...,
        min_length=8,
        example="StrongPassword123!"
    )

    @field_validator('password')
    def validate_password(cls, v):
        # Patrón que exige una letra minúscula, una mayúscula, un número y un carácter especial
        pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$")
        if not pattern.match(v):
            raise HTTPException(
                status_code=401,
                detail=ErrorResponse(
                    code=401,
                    message="Credenciales incorrectas"
                ).model_dump()
            )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user123",
                "password": "StrongPassword123!"
            }
        }

# Schema para la solicitud de recuperación de contraseña
class RecoverRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

