"""منطق کسب‌وکار Product -- جدا از لایهٔ مسیر و لایهٔ داده."""
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductOut


async def list_products(db: AsyncSession) -> List[ProductOut]:
    return await ProductRepository(db).list()


async def get_product(db: AsyncSession, item_id: str) -> ProductOut:
    item = await ProductRepository(db).get(item_id)
    if item is None:
        raise AppError("not_found", "Product پیدا نشد", status_code=404)
    return item


async def create_product(db: AsyncSession, payload: ProductCreate) -> ProductOut:
    return await ProductRepository(db).create(payload.model_dump())


async def delete_product(db: AsyncSession, item_id: str) -> None:
    await get_product(db, item_id)
    await ProductRepository(db).delete(item_id)
