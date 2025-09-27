from pydantic import BaseModel

class AddressBase(BaseModel):
    full_name: str
    phone_number: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str = "India"
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    user_id: int