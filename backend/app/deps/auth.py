# backend/app/deps/auth.py

from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.permissions import SystemPermissions
from app.deps.db import get_db
from app.models.user import User

# 1. Ruta exacta de tu endpoint de login para que Swagger UI sepa a dónde enviar credenciales
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Decodifica el token JWT recibido en la cabecera Authorization y busca al usuario en BD.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificamos el token con la clave secreta
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception
    
    try:
        user_id_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception
    
    # Consultamos al usuario en la BD de forma asíncrona
    result = await db.execute(select(User).where(User.id == user_id_uuid))
    user = result.scalars().first() 
    
    if user is None:
        raise credentials_exception
        
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica que el usuario obtenido del token esté activo.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    return current_user

async def get_current_system_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Verifica que el usuario actual tenga privilegios de administrador del sistema.
    """
    if not current_user.is_system_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador del sistema",
        )
    return current_user

class PermissionChecker:
    def __init__(self, required_permission: SystemPermissions):
        self.required_permission = required_permission.value

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        # 1. Si es superusuario/admin global (is_system_admin), acceso total
        if getattr(current_user, "is_system_admin", False):
            return current_user

        # 2. Extraer todos los permisos que tiene el usuario a través de sus roles
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