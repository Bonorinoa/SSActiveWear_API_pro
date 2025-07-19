# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# This line creates the database tables based on our models,
# but only if they don't exist yet. We'll run the sync script
# to do the main table creation, but this is good practice.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: This function creates and yields a new database session
# for each request, then ensures it's closed afterward.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the SS Activewear Catalog API!"}


@app.get("/api/products", response_model=List[schemas.ProductDisplay])
def read_products(
    category: str = None,
    color: str = None,
    brand: str = None,
    sustainable: bool = None,
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db)
):
    # Calculate the number of items to skip for pagination
    skip = (page - 1) * page_size
    
    products = crud.get_products(
        db=db, 
        category=category,
        color=color,
        brand=brand,
        sustainable=sustainable,
        skip=skip, 
        limit=page_size
    )
    return products


@app.get("/api/filters")
def read_filter_options(db: Session = Depends(get_db)):
    return crud.get_filter_options(db=db)