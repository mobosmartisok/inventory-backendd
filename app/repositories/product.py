"""لایهٔ داده برای Product -- Postgres (SQLAlchemy async)."""
import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import ProductModel
from app.schemas.product import ProductOut


def _to_schema(row: ProductModel) -> ProductOut:
    return ProductOut(
        id=row.id,
        name=row.name,
    )


class ProductRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list(self) -> List[ProductOut]:
        result = await self.db.execute(select(ProductModel))
        return [_to_schema(row) for row in result.scalars().all()]

    async def get(self, item_id: str) -> Optional[ProductOut]:
        row = await self.db.get(ProductModel, item_id)
        return _to_schema(row) if row else None

    async def create(self, data: dict) -> ProductOut:
        row = ProductModel(id=str(uuid.uuid4()), **data)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return _to_schema(row)

    async def delete(self, item_id: str) -> None:
        row = await self.db.get(ProductModel, item_id)
        if row:
            await self.db.delete(row)
            await self.db.commit()
