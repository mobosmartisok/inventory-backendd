"""منطق کسب‌وکار Price -- جدا از لایهٔ مسیر و لایهٔ داده."""
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.repositories.price import PriceRepository
from app.schemas.price import PriceCreate, PriceOut


async def list_prices(db: AsyncSession) -> List[PriceOut]:
    return await PriceRepository(db).list()


async def get_price(db: AsyncSession, item_id: str) -> PriceOut:
    item = await PriceRepository(db).get(item_id)
    if item is None:
        raise AppError("not_found", "Price پیدا نشد", status_code=404)
    return item


async def create_price(db: AsyncSession, payload: PriceCreate) -> PriceOut:
    return await PriceRepository(db).create(payload.model_dump())


async def delete_price(db: AsyncSession, item_id: str) -> None:
    await get_price(db, item_id)
    await PriceRepository(db).delete(item_id)
