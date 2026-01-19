# services/product_service.py
from sqlalchemy.orm import Session
from fastapi import Depends
import database_models  # Your SQLAlchemy models
from dependencies import get_db  # Your database dependency

class ProductService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    def get_all(self):
        return self.db.query(database_models.Product).all()
    
    def get_by_id(self, id: int):
        return self.db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    def create(self, name: str):
        product = database_models.Product(name=name)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update(self, id: int, name: str):
        product = self.get_by_id(id)
        if product:
            product.name = name
            self.db.commit()
            self.db.refresh(product)
        return product
    
    def delete(self, id: int):
        product = self.get_by_id(id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False