from typing import List
from fastapi import Depends, HTTPException, status
from backend.app.api.deps import get_current_active_user
from backend.app.models.tenant import User

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.is_superuser:
            return True

        user_permissions = set()
        for role in user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)

        if not all(perm in user_permissions for perm in self.required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return True
