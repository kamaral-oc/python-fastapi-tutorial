from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta

DATABASE_URL = "postgresql+asyncpg://fastapi:fastapi@db/fastapi_db"

# DB engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session class
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Models base class
Base: DeclarativeMeta = declarative_base()
