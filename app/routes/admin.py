from fastapi import APIRouter, Depends, HTTPException
from models.product import ProductCreate
from models.order import OrderStatus
import database

router = APIRouter(prefix="/admin", tags=["admin"])

# Simple admin check (implement proper admin auth later)
def is_admin(user_id: int):
    return user_id == 1  # First user is admin

@router.post("/products/")
def admin_create_product(product_data: ProductCreate, user_id: int):
    if not is_admin(user_id):
        raise HTTPException(status_code=403, detail="Admin access required")
    return database.create_product(product_data.dict())

@router.get("/orders/")
def admin_get_orders(user_id: int):
    if not is_admin(user_id):
        raise HTTPException(status_code=403, detail="Admin access required")
    return database.get_all_orders()

@router.put("/orders/{order_id}/status")
def admin_update_order_status(order_id: int, status: OrderStatus, user_id: int):
    if not is_admin(user_id):
        raise HTTPException(status_code=403, detail="Admin access required")
    success = database.admin_update_order_status(order_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated"}