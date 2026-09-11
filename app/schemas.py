from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "customer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True