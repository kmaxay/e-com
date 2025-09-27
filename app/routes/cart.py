from fastapi import APIRouter, Depends, HTTPException
from app.schemas.cart import CartItem, CartItemCreate, CartResponse
from app.routes.auth import get_current_user
import app.database

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add", response_model=CartItem)
def add_to_cart(
    cart_item: CartItemCreate,
    user_id: int = Depends(get_current_user)
):
    # Check if product exists
    product = database.get_product_by_id(cart_item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product has enough quantity
    if product.quantity < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    return database.add_to_cart(user_id, cart_item)

@router.get("/", response_model=CartResponse)
def get_cart(user_id: int = Depends(get_current_user)):
    cart_items = database.get_user_cart(user_id)
    total_items = sum(item.quantity for item in cart_items)
    
    # Calculate total price
    total_price = 0
    for item in cart_items:
        product = database.get_product_by_id(item.product_id)
        if product:
            total_price += product.price * item.quantity
    
    return CartResponse(
        items=cart_items,
        total_items=total_items,
        total_price=round(total_price, 2)
    )

@router.delete("/item/{item_id}")
def remove_from_cart(item_id: int, user_id: int = Depends(get_current_user)):
    success = database.remove_from_cart(user_id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@router.put("/item/{item_id}")
def update_cart_item(
    item_id: int, 
    quantity: int,
    user_id: int = Depends(get_current_user)
):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    success = database.update_cart_item(user_id, item_id, quantity)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart item updated"}