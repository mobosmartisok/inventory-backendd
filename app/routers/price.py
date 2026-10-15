from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.responses import success
from app.core.security import get_current_user, require_delete_access, require_write_access
from app.schemas.price import PriceCreate
from app.services import price_service as service

router = APIRouter(
    prefix="/prices",
    tags=["prices"],
)


@router.get("", dependencies=[Depends(get_current_user)])
async def list_items(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_prices(db))


@router.get("/{item_id}", dependencies=[Depends(get_current_user)])
async def get_item(item_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.get_price(db, item_id))


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_write_access)])
async def create_item(payload: PriceCreate, db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.create_price(db, payload))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_delete_access)])
async def delete_item(item_id: str, db: AsyncSession = Depends(get_db)) -> None:
    await service.delete_price(db, item_id)
