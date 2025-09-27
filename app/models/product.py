from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    category: Optional[str] = None

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    category: Optional[str] = None