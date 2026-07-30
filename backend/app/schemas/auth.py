# backend\app\schemas\auth.py
from pydantic import BaseModel, Field

# 1. Request de login (entrada)
class LoginRequest(BaseModel):
    username: str = Field(..., description="Nombre de usuario o correo electrónico")
    password: str = Field(..., description="Contraseña del usuario")
    remember_me: bool = Field(default=False, description="Extender la duración de la sesión")

# 2. Respuesta con token (salida)
class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")

# 3. Payload interno del JWT
class TokenPayload(BaseModel):
    sub: str = Field(..., description="Identificador del usuario (user_id)")
    exp: int = Field(..., description="Fecha de expiración del token en timestamp")

# 4. Datos procesados del token 
class TokenData(BaseModel):
    user_id: str | None