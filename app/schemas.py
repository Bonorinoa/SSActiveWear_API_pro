# app/schemas.py

from pydantic import BaseModel
from typing import Optional

# This is our Pydantic model for the Product data.
# It defines the shape and data types for API responses.
class Product(BaseModel):
    # Core product identifiers
    sku: str
    styleID: int
    
    # Information for display and filtering
    brandName: str
    title: str
    baseCategory: str
    colorName: str
    sizeName: str
    description: Optional[str] = None # Use Optional for fields that can be null
    
    # Pricing and inventory
    piecePrice: float
    qty: int
    
    # Features for filtering and display
    sustainableStyle: bool
    colorFrontImage: Optional[str] = None
    colorBackImage: Optional[str] = None

    # This special Config class enables "ORM Mode".
    # It allows Pydantic to read data directly from our SQLAlchemy model objects.
    class Config:
        from_attributes = True