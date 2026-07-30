# backend\app\deps\auth.py

from sqlalchemy import select

from uuid import UUID

from app.models.user import User
from app.deps.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.core.config import settings
from app.core.permissions import SystemPermissions
from app.deps.auth import get_current_active_user  # Tu dependencia actual de usuario logueado

# 1. Configuración de OAuth2 (En este proyecto aún no defino el API para eso)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Decodifica el token JWT y busca al usuario de forma asíncrona.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except (JWTError, ValidationError):
        raise credentials_exception
    
    try:
        user_id_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first() 
    
    if user is None:
        raise credentials_exception
        
    return user

class PermissionChecker:
    def __init__(self, required_permission: SystemPermissions):
        self.required_permission = required_permission.value

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        # 1. Si es superusuario/admin global, le damos acceso total
        if getattr(current_user, "is_superuser", False):
            return current_user

        # 2. Extraer todos los permisos que tiene el usuario a través de sus roles
        # (Ajusta la relación según cómo tengas mapeado tu modelo User -> Role -> Permissions)
        user_permissions = set()
        if hasattr(current_user, "role") and current_user.role:
            user_permissions = {p.code for p in current_user.role.permissions}

        # 3. Validar si posee el permiso solicitado
        if self.required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes el permiso necesario: '{self.required_permission}'"
            )
        
        return current_user

