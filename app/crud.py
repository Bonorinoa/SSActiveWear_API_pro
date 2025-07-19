# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def get_products(
    db: Session,
    category: str | None,
    color: str | None,
    brand: str | None,
    sustainable: bool | None,
    skip: int = 0,
    limit: int = 50  # Changed default to 50 to match previous steps
):
    # Define the columns we want to select.
    # These are the common columns plus our new aggregated columns.
    query = db.query(
        models.Product.styleID,
        models.Product.brandName,
        models.Product.title,
        models.Product.baseCategory,
        models.Product.colorName,
        models.Product.description,
        models.Product.sustainableStyle,
        models.Product.colorFrontImage,
        models.Product.colorBackImage,
        # Aggregate Functions:
        func.min(models.Product.piecePrice).label("startingPrice"),
        func.sum(models.Product.qty).label("totalStock"),
        func.array_agg(models.Product.sizeName).label("availableSizes")
    )

    # Dynamically apply filters only if they are provided
    if category:
        query = query.filter(models.Product.baseCategory == category)
    if color:
        query = query.filter(models.Product.colorName == color)
    if brand:
        query = query.filter(models.Product.brandName == brand)
    if sustainable is not None:
        query = query.filter(models.Product.sustainableStyle == sustainable)

    # Group by all the non-aggregated columns
    query = query.group_by(
        models.Product.styleID,
        models.Product.brandName,
        models.Product.title,
        models.Product.baseCategory,
        models.Product.colorName,
        models.Product.description,
        models.Product.sustainableStyle,
        models.Product.colorFrontImage,
        models.Product.colorBackImage
    )

    # Apply pagination and execute the query
    return query.offset(skip).limit(limit).all()


def get_filter_options(db: Session):
    # This function remains the same as it correctly fetches distinct values.
    categories = db.query(models.Product.baseCategory).distinct().all()
    colors = db.query(models.Product.colorName).distinct().all()
    brands = db.query(models.Product.brandName).distinct().all()
    
    return {
        "categories": sorted([c[0] for c in categories if c[0] is not None]),
        "colors": sorted([c[0] for c in colors if c[0] is not None]),
        "brands": sorted([b[0] for b in brands if b[0] is not None])
    }