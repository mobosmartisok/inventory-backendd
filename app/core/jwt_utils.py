"""پیاده‌سازی مینیمال JWT (HS256) بدون وابستگی خارجی.

عمداً به‌جای کتابخانهٔ pyjwt نوشته شده: روی PyPI یک پکیج دیگر هم دقیقاً با نام
«jwt» وجود دارد که API کاملاً متفاوتی دارد و اگر هر دو روی یک سیستم نصب شوند
(اتفاق واقعی و شناخته‌شده)، import jwt می‌تواند بی‌سروصدا به پکیج اشتباه اشاره
کند. برای جلوگیری از این تداخل، اینجا فقط از کتابخانهٔ استاندارد پایتون استفاده
شده است.
"""
import base64
import hashlib
import hmac
import json
import time


class InvalidTokenError(Exception):
    pass


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    segments = [
        _b64url_encode(json.dumps(header, separators=(",", ":")).encode()),
        _b64url_encode(json.dumps(payload, separators=(",", ":")).encode()),
    ]
    signing_input = ".".join(segments).encode()
    signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    segments.append(_b64url_encode(signature))
    return ".".join(segments)


def decode(token: str, secret: str) -> dict:
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError:
        raise InvalidTokenError("ساختار توکن نامعتبر است") from None

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    try:
        actual_sig = _b64url_decode(sig_b64)
    except Exception as exc:
        raise InvalidTokenError("امضای توکن نامعتبر است") from exc

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise InvalidTokenError("امضای توکن نامعتبر است")

    try:
        payload = json.loads(_b64url_decode(payload_b64))
    except Exception as exc:
        raise InvalidTokenError("بار توکن نامعتبر است") from exc

    exp = payload.get("exp")
    if exp is not None and time.time() > exp:
        raise InvalidTokenError("توکن منقضی شده است")
    return payload
