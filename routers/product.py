# routers/product.py
from fastapi import APIRouter, Depends, HTTPException
from models import Product  # Pydantic model
from services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_all_products(service: ProductService = Depends(ProductService)):
    return service.get_all()

@router.get("/{id}")
def get_product_by_id(id: int, service: ProductService = Depends(ProductService)):
    product = service.get_by_id(id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/")
def create_product(product: Product, service: ProductService = Depends(ProductService)):
    return service.create(product.name)

@router.put("/{id}")
def update_product(id: int, product: Product, service: ProductService = Depends(ProductService)):
    updated_product = service.update(id, product.name)
    if updated_product:
        return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{id}")
def delete_product(id: int, service: ProductService = Depends(ProductService)):
    if service.delete(id):
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")