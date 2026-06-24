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