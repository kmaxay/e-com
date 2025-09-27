from fastapi import APIRouter, HTTPException
from models.product import Product, ProductCreate, ProductUpdate
import database

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[Product])
def get_all_products():
    return database.get_all_products()

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = database.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
def create_product(product: ProductCreate):
    return database.create_product(product.dict())

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate):
    updated_product = database.update_product(product_id, product.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: int):
    success = database.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}