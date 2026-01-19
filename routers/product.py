from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
import database_models
from dependencies import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(name=product.name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.name = product.name
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}