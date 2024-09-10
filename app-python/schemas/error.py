from typing import Optional
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    code: int = Field(..., example=400)
    message: str = Field(..., example="Solicitud inválida.")
    details: Optional[str] = Field(None, example="El campo 'email' es obligatorio.")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 400,
                "message": "Solicitud inválida.",
                "details": "El campo 'email' es obligatorio."
            }
        }
