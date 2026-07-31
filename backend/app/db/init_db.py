# backend/app/db/init_db.py

import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal 
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db(db: AsyncSession) -> None:
    # 1. Consulta asíncrona estilo SQLAlchemy 2.0
    stmt = select(User).where(
        (User.email == settings.FIRST_SUPERUSER_EMAIL) | 
        (User.username == settings.FIRST_SUPERUSER_USERNAME)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()

    # 2. Si no existe, crearlo de forma asíncrona
    if not user:
        user_in = User(
            username=settings.FIRST_SUPERUSER_USERNAME,
            name="Administrador",
            slug="admin",
            email=settings.FIRST_SUPERUSER_EMAIL,
            password_hash=hash_password(settings.FIRST_SUPERUSER_PASSWORD),
            is_system_admin=True,
            is_active=True,
        )
        db.add(user_in)
        await db.commit() 
        logger.info(f"! Superusuario '{settings.FIRST_SUPERUSER_USERNAME}' creado exitosamente.")
    else:
        logger.info(f"ℹ¡! El usuario administrador '{user.username}' ya existe. Omitiendo creación.")


async def main() -> None:
    logger.info("Verificando/Iniciando datos en la base de datos...")
    async with AsyncSessionLocal() as db:
        await init_db(db)


if __name__ == "__main__":
    # Ejecutamos el bucle de eventos de asyncio
    asyncio.run(main())