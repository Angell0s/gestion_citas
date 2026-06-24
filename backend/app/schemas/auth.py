# backend\app\schemas\auth.py
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Nombre de usuario o correo electrónico")
    password: str = Field(..., description="Contraseña del usuario")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token, generalmente 'bearer'")

class TokenPayload(BaseModel):
    sub: str = Field(..., description="Identificador del usuario (user_id)")
    exp: int = Field(..., description="Fecha de expiración del token en formato timestamp")