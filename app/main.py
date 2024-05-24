from fastapi import FastAPI
from app.routes import items
from app.db import models, database

# Create an instance of the FastAPI application
app = FastAPI()

# Define a root endpoint
@app.get("/")
async def read_root():
    return {"message": "success"}

# Items router /items
app.include_router(items.router, prefix="/items")

@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        # Create all tables
        await conn.run_sync(models.Base.metadata.create_all)
