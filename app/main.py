from fastapi import FastAPI
from app.routes import items

# Create an instance of the FastAPI application
app = FastAPI()

# Define a root endpoint
@app.get("/")
async def read_root():
    return {"message": "success"}

# Items router /items
app.include_router(items.router, prefix="/items")
