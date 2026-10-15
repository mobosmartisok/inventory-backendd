from pydantic import BaseModel


class PriceBase(BaseModel):
    name: str


class PriceCreate(PriceBase):
    pass


class PriceOut(PriceBase):
    id: str
