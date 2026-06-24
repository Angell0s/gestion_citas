# backend\app\deps\business.py
from fastapi import Header
from uuid import UUID

from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User

from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import BusinessMember
from app.core.permissions import SystemPermissions

# Dependencia para obtener el business_id desde un header (o podría ser path)
async def get_business_id(business_id: UUID = Header(..., alias="X-Business-ID")):
    return business_id

async def get_current_membership(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    business_id: UUID = Depends(get_business_id)  # header o path
):
    result = await db.execute(
        select(BusinessMember)
        .where(
            BusinessMember.user_id == current_user.id,
            BusinessMember.business_id == business_id
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(403, "No pertenece a este negocio")

    return membership

def require_permission(permission: SystemPermissions):
    async def checker(
        membership: BusinessMember = Depends(get_current_membership)
    ):
        if permission.value not in membership.role.permissions:
            raise HTTPException(403, "No autorizado")
        return membership

    return checker