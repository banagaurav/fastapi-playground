from fastapi import FastAPI
import database_models
from database import engine
from routers import product

app = FastAPI()

# Create database tables
database_models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(product.router)

@app.get('/')
def greeting():
    return "Hello Dai"