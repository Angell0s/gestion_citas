# backend/app/api/api_v1/endpoints/auth.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.deps.db import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login_access_token(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    # OAuth2PasswordRequestForm usa el campo 'username' (que puede ser el email)
    user = db.query(User).filter(User.email == data.username).first()
    
    if not user or not security.verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Usuario inactivo"
        )
    
    return {
        "access_token": security.create_access_token(
            str(user.id),
            remember_me=data.remember_me
        ),
        "token_type": "bearer",
    }
