from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: str
