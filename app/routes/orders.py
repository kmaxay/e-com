from fastapi import APIRouter, Depends, HTTPException
from models.order import Order, OrderCreate, OrderResponse, OrderStatus
from routes.auth import get_current_user
import database

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(order_data: OrderCreate, user_id: int = Depends(get_current_user)):
    try:
        # Get user cart
        cart_items = database.get_user_cart(user_id)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")
        
        # Create order
        order = database.create_order(user_id, cart_items, order_data.dict())
        
        # Clear cart after successful order
        database.clear_user_cart(user_id)
        
        return OrderResponse(
            id=order.id,
            total_amount=order.total_amount,
            status=order.status,
            item_count=len(order.items),
            created_at=order.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[OrderResponse])
def get_user_orders(user_id: int = Depends(get_current_user)):
    orders = database.get_user_orders(user_id)
    return [
        OrderResponse(
            id=order.id,
            total_amount=order.total_amount,
            status=order.status,
            item_count=len(order.items),
            created_at=order.created_at
        )
        for order in orders
    ]

@router.get("/{order_id}", response_model=Order)
def get_order_details(order_id: int, user_id: int = Depends(get_current_user)):
    order = database.get_user_order(user_id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, user_id: int = Depends(get_current_user)):
    success = database.cancel_order(order_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel order")
    return {"message": "Order cancelled successfully"}