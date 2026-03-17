# backend\app\database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker 
from app.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)