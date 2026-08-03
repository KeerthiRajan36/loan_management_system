from fastapi import Depends
from fastapi import HTTPException

from app.utils.dependencies import get_current_user


def role_required(allowed_roles):

    def checker(user=Depends(get_current_user)):

        if user.role.value not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )

        return user

    return checker