"""مسیر دمو برای صدور توکن -- بدون پایگاه‌دادهٔ کاربر واقعی (فقط برای آزمایش RBAC در این MVP).

در فاز عملیاتی باید با یک فلوی احراز هویت واقعی (کاربر/رمز یا SSO) جایگزین شود.
"""
import time

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.config import settings
from app.core.jwt_utils import encode as jwt_encode
from app.core.security import ROLES

router = APIRouter(prefix="/auth", tags=["auth"])

TOKEN_TTL_SECONDS = 8 * 60 * 60


class TokenRequest(BaseModel):
    username: str
    role: str


@router.post("/token")
async def issue_token(payload: TokenRequest) -> dict:
    if payload.role not in ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"نقش باید یکی از این‌ها باشد: {', '.join(ROLES)}",
        )
    claims = {
        "sub": payload.username,
        "role": payload.role,
        "exp": time.time() + TOKEN_TTL_SECONDS,
    }
    token = jwt_encode(claims, settings.JWT_SECRET)
    return {"access_token": token, "token_type": "bearer", "role": payload.role}
