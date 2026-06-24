# backend\app\database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker 
from backend.app.core.config import settings
    
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)