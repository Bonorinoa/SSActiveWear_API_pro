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

def get_filter_options(db: Session):
    categories = db.query(models.Product.baseCategory).distinct().all()
    colors = db.query(models.Product.colorName).distinct().all()
    brands = db.query(models.Product.brandName).distinct().all()
    
    # The queries return a list of tuples, so we extract the first element of each tuple.
    return {
        "categories": sorted([c[0] for c in categories if c[0] is not None]),
        "colors": sorted([c[0] for c in colors if c[0] is not None]),
        "brands": sorted([b[0] for b in brands if b[0] is not None])
    }