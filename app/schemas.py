from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int
    created_at: Optional[str]
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    created_at: Optional[str]
    class Config:
        orm_mode = True

class SaleItemIn(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    customer_id: Optional[int]
    items: List[SaleItemIn]

class SaleItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        orm_mode = True

class SaleOut(BaseModel):
    id: int
    customer_id: Optional[int]
    total: float
    items: List[SaleItemOut]
    created_at: Optional[str]
    class Config:
        orm_mode = True
