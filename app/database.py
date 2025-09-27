from app.schemas.product import Product, ProductCreate
from app.schemas.user import User, UserCreate
from app.schemas.cart import CartItem, CartItemCreate
from app.schemas.order import Order, OrderItem, OrderStatus, OrderCreate
from app.schemas.address import Address, AddressCreate
from app.auth import get_password_hash, verify_password
from typing import List, Optional
from datetime import datetime

# ===== IN-MEMORY DATABASES =====
products_db = []
users_db = []
cart_items_db = []
orders_db = []
addresses_db = []

# ===== ID COUNTERS =====
current_product_id = 1
current_user_id = 1
current_cart_id = 1
current_order_id = 1
current_address_id = 1



# Persistant DB
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== PRODUCT OPERATIONS =====
def get_all_products() -> List[Product]:
    return products_db

def get_product_by_id(product_id: int) -> Optional[Product]:
    for product in products_db:
        if product.id == product_id:
            return product
    return None

def create_product(product_data: dict) -> Product:
    global current_product_id
    product = Product(id=current_product_id, **product_data)
    products_db.append(product)
    current_product_id += 1
    return product

def update_product(product_id: int, product_data: dict) -> Optional[Product]:
    for index, product in enumerate(products_db):
        if product.id == product_id:
            updated_data = product.dict()
            updated_data.update({k: v for k, v in product_data.items() if v is not None})
            products_db[index] = Product(**updated_data)
            return products_db[index]
    return None

def delete_product(product_id: int) -> bool:
    for index, product in enumerate(products_db):
        if product.id == product_id:
            products_db.pop(index)
            return True
    return False

def update_product_quantity(product_id: int, quantity_change: int) -> bool:
    """Update product quantity (for inventory management)"""
    product = get_product_by_id(product_id)
    if product:
        new_quantity = product.quantity + quantity_change
        if new_quantity >= 0:
            product.quantity = new_quantity
            return True
    return False

# ===== USER OPERATIONS =====
def create_user(user_data: UserCreate) -> User:
    global current_user_id
    
    # Check if phone number already exists
    if get_user_by_phone(user_data.phone_number):
        raise ValueError("Phone number already registered")
    
    hashed_password = get_password_hash(user_data.password)
    user = User(
        id=current_user_id,
        phone_number=user_data.phone_number,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    users_db.append(user)
    current_user_id += 1
    return user

def get_user_by_id(user_id: int) -> Optional[User]:
    for user in users_db:
        if user.id == user_id:
            return user
    return None

def get_user_by_phone(phone_number: str) -> Optional[User]:
    for user in users_db:
        if user.phone_number == phone_number:
            return user
    return None

# ===== CART OPERATIONS =====
def add_to_cart(user_id: int, cart_item: CartItemCreate) -> CartItem:
    global current_cart_id
    
    # Check if item already exists in cart
    for item in cart_items_db:
        if item.user_id == user_id and item.product_id == cart_item.product_id:
            item.quantity += cart_item.quantity
            return item
    
    # Create new cart item
    cart_item_obj = CartItem(
        id=current_cart_id,
        user_id=user_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    cart_items_db.append(cart_item_obj)
    current_cart_id += 1
    return cart_item_obj

def get_user_cart(user_id: int) -> List[CartItem]:
    return [item for item in cart_items_db if item.user_id == user_id]

def remove_from_cart(user_id: int, item_id: int) -> bool:
    for index, item in enumerate(cart_items_db):
        if item.user_id == user_id and item.id == item_id:
            cart_items_db.pop(index)
            return True
    return False

def update_cart_item(user_id: int, item_id: int, quantity: int) -> bool:
    for item in cart_items_db:
        if item.user_id == user_id and item.id == item_id:
            item.quantity = quantity
            return True
    return False

def clear_user_cart(user_id: int) -> bool:
    """Clear user's cart (after order placement)"""
    global cart_items_db
    initial_count = len(cart_items_db)
    cart_items_db = [item for item in cart_items_db if item.user_id != user_id]
    return len(cart_items_db) < initial_count

# ===== ADDRESS OPERATIONS =====
def create_address(user_id: int, address_data: dict) -> Address:
    global current_address_id
    
    # If this is the first address, set it as default
    user_addresses = get_user_addresses(user_id)
    if not user_addresses:
        address_data['is_default'] = True
    
    address = Address(id=current_address_id, user_id=user_id, **address_data)
    addresses_db.append(address)
    current_address_id += 1
    return address

def get_user_addresses(user_id: int) -> List[Address]:
    return [addr for addr in addresses_db if addr.user_id == user_id]

def get_user_address(user_id: int, address_id: int) -> Optional[Address]:
    for addr in addresses_db:
        if addr.user_id == user_id and addr.id == address_id:
            return addr
    return None

def set_default_address(user_id: int, address_id: int) -> bool:
    """Set an address as default for the user"""
    target_address = None
    
    # First, remove default status from all user addresses
    for addr in addresses_db:
        if addr.user_id == user_id:
            if addr.id == address_id:
                target_address = addr
            addr.is_default = False
    
    # Set the target address as default
    if target_address:
        target_address.is_default = True
        return True
    return False

def get_default_address(user_id: int) -> Optional[Address]:
    for addr in addresses_db:
        if addr.user_id == user_id and addr.is_default:
            return addr
    return None

def delete_address(user_id: int, address_id: int) -> bool:
    for index, addr in enumerate(addresses_db):
        if addr.user_id == user_id and addr.id == address_id:
            addresses_db.pop(index)
            
            # If deleted address was default, set another as default
            if addr.is_default:
                user_addresses = get_user_addresses(user_id)
                if user_addresses:
                    user_addresses[0].is_default = True
            return True
    return False

# ===== ORDER OPERATIONS =====
def create_order(user_id: int, cart_items: List[CartItem], order_data: dict) -> Order:
    global current_order_id
    
    # Calculate total amount and prepare order items
    total_amount = 0
    order_items = []
    
    for item in cart_items:
        product = get_product_by_id(item.product_id)
        if product:
            # Check stock availability
            if product.quantity < item.quantity:
                raise ValueError(f"Not enough stock for {product.name}")
            
            total_amount += product.price * item.quantity
            order_items.append(OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            ))
    
    if not order_items:
        raise ValueError("Cart is empty")
    
    # Verify address belongs to user
    address = get_user_address(user_id, order_data['address_id'])
    if not address:
        raise ValueError("Invalid address")
    
    # Create order
    order = Order(
        id=current_order_id,
        user_id=user_id,
        items=order_items,
        total_amount=round(total_amount, 2),
        status=OrderStatus.PENDING,
        address_id=order_data['address_id'],
        payment_method=order_data['payment_method'],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Update product quantities (reduce inventory)
    for item in cart_items:
        update_product_quantity(item.product_id, -item.quantity)
    
    orders_db.append(order)
    current_order_id += 1
    return order

def get_user_orders(user_id: int) -> List[Order]:
    return [order for order in orders_db if order.user_id == user_id]

def get_order_by_id(order_id: int) -> Optional[Order]:
    for order in orders_db:
        if order.id == order_id:
            return order
    return None

def get_user_order(user_id: int, order_id: int) -> Optional[Order]:
    for order in orders_db:
        if order.id == order_id and order.user_id == user_id:
            return order
    return None

def update_order_status(order_id: int, user_id: int, status: OrderStatus) -> bool:
    order = get_user_order(user_id, order_id)
    if order:
        order.status = status
        order.updated_at = datetime.now()
        return True
    return False

def admin_update_order_status(order_id: int, status: OrderStatus) -> bool:
    """Admin function to update any order status"""
    order = get_order_by_id(order_id)
    if order:
        order.status = status
        order.updated_at = datetime.now()
        return True
    return False

def get_all_orders() -> List[Order]:
    """Admin function to get all orders"""
    return orders_db

def cancel_order(order_id: int, user_id: int) -> bool:
    """Cancel order and restore product quantities"""
    order = get_user_order(user_id, order_id)
    if order and order.status == OrderStatus.PENDING:
        # Restore product quantities
        for item in order.items:
            update_product_quantity(item.product_id, item.quantity)
        
        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.now()
        return True
    return False

# ===== ADMIN OPERATIONS =====
def get_sales_stats():
    """Get basic sales statistics"""
    total_orders = len(orders_db)
    total_revenue = sum(order.total_amount for order in orders_db 
                       if order.status != OrderStatus.CANCELLED)
    pending_orders = len([o for o in orders_db if o.status == OrderStatus.PENDING])
    
    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "pending_orders": pending_orders,
        "completed_orders": len([o for o in orders_db if o.status == OrderStatus.DELIVERED])
    }

# ===== INITIAL SAMPLE DATA =====
def initialize_sample_data():
    """Add some sample products and a default admin user for testing"""
    global products_db, users_db, current_product_id
    
    # Sample products
    sample_products = [
        {
            "name": "iPhone 15 Pro", 
            "price": 999.99, 
            "quantity": 10, 
            "category": "Electronics",
            "description": "Latest iPhone with advanced camera"
        },
        {
            "name": "MacBook Pro 14-inch", 
            "price": 1999.99, 
            "quantity": 5, 
            "category": "Electronics",
            "description": "Powerful laptop for professionals"
        },
        {
            "name": "AirPods Pro", 
            "price": 249.99, 
            "quantity": 20, 
            "category": "Electronics",
            "description": "Wireless earbuds with noise cancellation"
        },
        {
            "name": "Cotton T-Shirt", 
            "price": 19.99, 
            "quantity": 50, 
            "category": "Clothing",
            "description": "Comfortable cotton t-shirt"
        },
        {
            "name": "Running Shoes", 
            "price": 89.99, 
            "quantity": 30, 
            "category": "Footwear",
            "description": "Comfortable running shoes"
        },
    ]
    
    for product_data in sample_products:
        create_product(product_data)
    
    # Create a default admin user
    try:
        admin_user = UserCreate(
            phone_number="+919876543210",
            password="admin123",
            username="admin",
            full_name="Admin User"
        )
        create_user(admin_user)
    except ValueError:
        pass  # Admin user already exists

# Initialize sample data when module loads
initialize_sample_data()