# backend\app\core\config.py
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

# Cargar variables de entorno desde ambos archivos .env
# 1. Raíz del proyecto (para variables globales)
load_dotenv(ROOT_DIR / ".env")
# 2. Directorio app
load_dotenv(BASE_DIR / ".env")

class Settings:
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))

    # JWT y seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Datos del proyecto
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Sistema de Citas")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
# Instancia global de configuración, settings se puede importar desde cualquier parte del proyecto.
settings = Settings()