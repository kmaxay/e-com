from fastapi import APIRouter, Depends, HTTPException
from models.address import Address, AddressCreate
from routes.auth import get_current_user
import database

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.post("/", response_model=Address)
def create_address(address_data: AddressCreate, user_id: int = Depends(get_current_user)):
    return database.create_address(user_id, address_data)

@router.get("/", response_model=list[Address])
def get_user_addresses(user_id: int = Depends(get_current_user)):
    return database.get_user_addresses(user_id)

@router.put("/{address_id}/default")
def set_default_address(address_id: int, user_id: int = Depends(get_current_user)):
    success = database.set_default_address(user_id, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Default address updated"}