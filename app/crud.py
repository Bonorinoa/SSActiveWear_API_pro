# app/crud.py

from sqlalchemy.orm import Session
from . import models

def get_products(
    db: Session, 
    category: str | None,
    color: str | None,
    brand: str | None,
    sustainable: bool | None,
    skip: int = 0, 
    limit: int = 100
):
    # Start with a query object for the Product model
    query = db.query(models.Product)

    # Dynamically apply filters only if they are provided
    if category:
        query = query.filter(models.Product.baseCategory == category)
    if color:
        query = query.filter(models.Product.colorName == color)
    if brand:
        query = query.filter(models.Product.brandName == brand)
    if sustainable is not None:
        query = query.filter(models.Product.sustainableStyle == sustainable)

    # Apply pagination and execute the query
    return query.offset(skip).limit(limit).all()