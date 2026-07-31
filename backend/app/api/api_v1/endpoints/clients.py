# backend/app/api/api_v1/endpoints/clients.py

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth import get_current_active_user, get_current_system_admin
from app.deps.db import get_db
from app.models.user import User
from app.schemas.users import UserRead

router = APIRouter()


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_system_admin),  # <--- Exige ser is_system_admin
):
    """
    Obtiene la lista de todos los usuarios registrados.
    Solo accesible por administradores del sistema.
    """
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users

@router.get("/saludo")
async def get_clients(current_user: User = Depends(get_current_active_user)):
    return [{"message": f"Hola {current_user.username}, aquí están tus clientes."}]