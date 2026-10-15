"""قالب قفل‌شدهٔ پاسخ موفق -- همهٔ اندپوینت‌ها از همین تابع استفاده می‌کنند."""
from typing import Any


def success(data: Any) -> dict:
    return {"success": True, "data": data}
