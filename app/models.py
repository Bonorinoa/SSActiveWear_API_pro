# app/models.py

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

# The Base class is a factory that our model will inherit from.
# It allows SQLAlchemy's ORM to map our class to the database table.
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    # Core product identifiers
    sku = Column(String, primary_key=True, index=True)
    styleID = Column(Integer, index=True)
    
    # Information for display and filtering
    brandName = Column(String, index=True)
    title = Column(String)
    baseCategory = Column(String, index=True)
    colorName = Column(String, index=True)
    sizeName = Column(String)
    description = Column(String, nullable=True) # Description can be optional
    
    # Pricing and inventory
    piecePrice = Column(Float)
    qty = Column(Integer)
    
    # Features for filtering and display
    sustainableStyle = Column(Boolean, default=False)
    colorFrontImage = Column(String, nullable=True)
    colorBackImage = Column(String, nullable=True)
    colorSwatchImage = Column(String, nullable=True)
    colorSwatchTextColor = Column(String, nullable=True)