# backend/app/api/api_v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.deps.db import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # <--- Acepta el formulario de Swagger UI
    db: AsyncSession = Depends(get_db),
):
    # 1. Buscar usuario por email o por username
    stmt = select(User).where(
        (User.email == form_data.username) | (User.username == form_data.username)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()

    # 2. Validar credenciales
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Validar estado del usuario
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Usuario inactivo"
        )

    # 4. Generar el token
    return {
        "access_token": security.create_access_token(str(user.id)),
        "token_type": "bearer",
    }