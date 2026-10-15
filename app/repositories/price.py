"""لایهٔ داده برای Price -- Postgres (SQLAlchemy async)."""
import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import PriceModel
from app.schemas.price import PriceOut


def _to_schema(row: PriceModel) -> PriceOut:
    return PriceOut(
        id=row.id,
        name=row.name,
    )


class PriceRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list(self) -> List[PriceOut]:
        result = await self.db.execute(select(PriceModel))
        return [_to_schema(row) for row in result.scalars().all()]

    async def get(self, item_id: str) -> Optional[PriceOut]:
        row = await self.db.get(PriceModel, item_id)
        return _to_schema(row) if row else None

    async def create(self, data: dict) -> PriceOut:
        row = PriceModel(id=str(uuid.uuid4()), **data)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return _to_schema(row)

    async def delete(self, item_id: str) -> None:
        row = await self.db.get(PriceModel, item_id)
        if row:
            await self.db.delete(row)
            await self.db.commit()
