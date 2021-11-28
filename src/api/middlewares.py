from fastapi import Depends, HTTPException, status

from src.api.schemas import UserTypeEnums
from src.auth.jwt import get_current_user
from src.data.models.mongodb import User


async def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.type != UserTypeEnums.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="forbidden access"
        )
