# Inventory

> ساخته‌شده با **Forge** -- کارخانهٔ استاندارد بک اند تیم.

## دربارهٔ سرویس
Mange Product

## متادیتای ساخت
- گروه گیت‌لب: `backend`
- نام ریپو: `inventory_backendd`
- موجودیت‌ها: Product, Price
- کش: بله
- صف: بله
- احراز هویت: JWT + RBAC
  - مدل RBAC: سلسله‌مراتبی
  - نقش‌ها (بالا→پایین): admin > editor > viewer -- حذف: `admin`، نوشتن: admin، editor
- دیتابیس: PostgreSQL (اتصال واقعی -- SQLAlchemy async)
- تاریخ ساخت: 2026-10-15 14:06

## اجرا
یک فایل `.env` بساز (در `.gitignore` است) و `DATABASE_URL` واقعی خودت را بگذار، مثلاً:
```
DATABASE_URL=postgresql+asyncpg://forge:change-me@localhost:5432/inventory_backendd
```
جدول‌ها خودکار و در لحظهٔ بالا آمدن سرویس ساخته می‌شوند (`Base.metadata.create_all`)؛ migration واقعی (Alembic) در فاز بعد است.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

سپس:
- `GET http://localhost:8000/health/live`
- `GET http://localhost:8000/health/ready`
- `GET/POST http://localhost:8000/products`
- `GET/POST http://localhost:8000/prices`

### گرفتن توکن (دمو RBAC -- بدون کاربر واقعی)
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "role": "admin"}'
# پاسخ: {"access_token": "...", "token_type": "bearer", "role": "admin"}

curl http://localhost:8000/products \
  -H "Authorization: Bearer <access_token>"
```
نقش‌ها از بالا به پایین رتبه‌بندی شده‌اند: admin > editor > viewer. فقط `admin` اجازهٔ DELETE دارد؛ نقش‌های admin، editor اجازهٔ POST دارند؛ همه (از جمله پایین‌ترین نقش، `viewer`) فقط می‌توانند بخوانند.

## تست
```bash
pytest -q
```

## معماری قفل‌شده
```
app/
  main.py          مسیر ورود و ثبت روترها
  core/             تنظیمات، پاسخ استاندارد، خطای استاندارد، احراز هویت، پیکربندی دیتابیس
  routers/          لایهٔ مسیر (HTTP) -- شامل auth.py برای صدور توکن دمو  services/         لایهٔ منطق کسب‌وکار
  repositories/      لایهٔ داده (Postgres واقعی (SQLAlchemy async))
  models/           مدل‌های SQLAlchemy (جدول‌های واقعی)
  schemas/          قراردادهای ورودی و خروجی
```

## ⚠️ محدودهٔ این نسخه (اثبات مفهوم)
این ریپو توسط Forge و به‌صورت لوکال ساخته شده است:
- ✅ اسکلت معماری قفل‌شده، ماژول سلامت، فایل پایپ‌لاین و قرارداد برنچ (`develop`/`main`) آماده است.
- ❌ اتصال خودکار به GitLab واقعی با توکن محدود وصل نیست -- این ریپو باید دستی push شود.
- ❌ اتصال زنده به بازوی بله وصل نیست -- ورودی از طریق CLI یا فرم وب جایگزین گرفته شده.
