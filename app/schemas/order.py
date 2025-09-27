from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    address_id: int
    payment_method: str

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    address_id: int
    payment_method: str
    created_at: datetime
    updated_at: datetime

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: OrderStatus
    item_count: int
    created_at: datetime