# backend/app/api/api_v1/endpoints/auth.py
from fastapi import Depends, HTTPException, status
from app.core.permissions import SystemPermissions
from app.models.user import User
from app.deps.auth import get_current_active_user  # Tu dependencia actual de usuario logueado

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