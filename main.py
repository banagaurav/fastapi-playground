from fastapi import Depends, FastAPI
from models import Product 
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

products = [Product(id= 1, name='laptop')]

database_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def greeting():
    return "Hello Dai"

@app.get("/product")
def get_all_products(db: Session = Depends(get_db)):
    # db = session()

    db_products = db.query(database_models.Product).all()

    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post("/product")
def create_product(product: Product, db: Session = Depends(get_db)):
    # Create a database model instance from the Pydantic model
    db_product = database_models.Product(
        name=product.name
        # Add other fields as needed based on your database model
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@app.put("/product/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # Find the existing product
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if not db_product:
        return "Product not found"
    
    # Update the product fields
    db_product.name = product.name
    # Update other fields as needed based on your database model
    
    db.commit()
    db.refresh(db_product)
    
    return db_product

@app.delete("/product")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product updated Successfully"
    
    return "Product not found"