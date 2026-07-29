# backend\app\schemas\users.py
import uuid
import re
import unicodedata
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator, ConfigDict

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    name: Optional[str] = Field(None, max_length=255, description="Nombre completo del usuario")
    email: str = Field(..., max_length=255, description="Correo electrónico único del usuario")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128, description="Contraseña del usuario")

class UserRead(UserBase):
    id: uuid.UUID
    slug: str
    is_system_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    username: str = Field(..., description="Nombre de usuario o correo electrónico")
    password: str = Field(..., description="Contraseña del usuario")

class UserInDB(UserRead):
    password_hash: str

