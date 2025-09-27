from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartResponse(BaseModel):
    items: List[CartItem]
    total_items: int
    total_price: float