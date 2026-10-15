"""وابستگی‌های احراز هویت -- بر اساس نوع انتخاب‌شده در زمان ساخت سرویس (AUTH_TYPE)."""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.jwt_utils import InvalidTokenError, decode as jwt_decode

bearer_scheme = HTTPBearer(auto_error=False)

ROLES = ["admin", "editor", "viewer"]


class CurrentUser:
    def __init__(self, username: str, role: str) -> None:
        self.username = username
        self.role = role


def _decode(token: str) -> dict:
    try:
        return jwt_decode(token, settings.JWT_SECRET)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="توکن ارسال نشده است")
    payload = _decode(credentials.credentials)
    return CurrentUser(username=payload.get("sub", ""), role=payload.get("role", ""))

# مدل RBAC: hierarchy -- نقش‌ها از بالاترین به پایین‌ترین امتیاز مرتب شده‌اند: admin > editor > viewer
# هر نقش همهٔ دسترسی‌های نقش‌های پایین‌تر از خودش را هم دارد (سطح پایین‌تر = امتیاز کمتر).
ROLE_LEVELS = {role: index for index, role in enumerate(ROLES)}
DELETE_LEVEL = 0  # فقط بالاترین نقش (admin) اجازهٔ حذف دارد
WRITE_LEVEL = max(len(ROLES) - 2, 0)  # همهٔ نقش‌ها به‌جز پایین‌ترین (viewer) اجازهٔ نوشتن دارند


def _role_level(role: str) -> int:
    return ROLE_LEVELS.get(role, len(ROLES))  # نقش ناشناس = کمترین امتیاز ممکن


def require_write_access(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if _role_level(user.role) > WRITE_LEVEL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"این عملیات نیاز به نقشی در سطح «{ROLES[WRITE_LEVEL]}» یا بالاتر دارد (نقش شما: «{user.role}»)",
        )
    return user


def require_delete_access(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if _role_level(user.role) > DELETE_LEVEL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"این عملیات فقط برای نقش «{ROLES[DELETE_LEVEL]}» مجاز است (نقش شما: «{user.role}»)",
        )
    return user
