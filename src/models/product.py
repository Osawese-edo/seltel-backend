from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: str = Field(..., min_length=1, max_length=2000, description="Product description")
    price: float = Field(default=0.0, ge=0, description="Product price")
    image_url: Optional[str] = Field(default=None, description="Product image URL")
    category: Optional[str] = Field(default=None, max_length=100, description="Product category")
    in_stock: bool = Field(default=True, description="Whether the product is in stock")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    price: Optional[float] = Field(None, ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    in_stock: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
