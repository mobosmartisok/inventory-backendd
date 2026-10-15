"""مدل SQLAlchemy برای Price -- جدول واقعی در Postgres."""
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PriceModel(Base):
    __tablename__ = "prices"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
