# backend\app\db\session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL).replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Validación básica para asegurar que la URL de la base de datos esté configurada
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurado")

# 1. Crear el motor asíncrono
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.DEBUG,  # Mostrar consultas SQL en modo debug
    future=True
)

# 2. Crear la fábrica de sesiones asíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# 3. Clase Base declarativa (Igual que antes)
Base = declarative_base()
