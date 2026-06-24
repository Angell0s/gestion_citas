# backend\app\schemas\business.py
import uuid
import re
import unicodedata
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator, ConfigDict

# 1. ESQUEMA BASE: Lo que comparten tanto la creación como la lectura.
# Ponemos las reglas estrictas aquí.<
class BusinessBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre oficial del negocio")
    display_name: str = Field(..., min_length=2, max_length=120)
    # Por defecto, todos los negocios nuevos asumen esta zona horaria
    timezone: str = Field(default="America/Mexico_City", max_length=50)
    logo: Optional[str] = None


# 2. ESQUEMA CREATE: Lo que el frontend envía en un POST (Registro de negocio).
class BusinessCreate(BusinessBase):
    # El slug lo hacemos opcional porque si el frontend no lo manda, el backend lo genera.
    slug: Optional[str] = None 

    @model_validator(mode='before')
    @classmethod
    def generate_slug_if_missing(cls, data: any) -> any:
        # Pydantic ejecuta esto ANTES de validar los tipos.
        # Si recibimos un JSON (dict) que tiene 'name' pero no tiene 'slug'...
        if isinstance(data, dict) and 'name' in data and not data.get('slug'):
            nombre = data['name']
            
            # Paso 1: Quitar acentos (Pánuco -> Panuco)
            sin_acentos = ''.join(
                c for c in unicodedata.normalize('NFD', nombre)
                if unicodedata.category(c) != 'Mn'
            )
            
            # Paso 2: Convertir a minúsculas y cambiar espacios/símbolos por guiones
            # "Reparaciones Panuco!" -> "reparaciones-panuco-"
            slug_crudo = re.sub(r'[^a-z0-9]+', '-', sin_acentos.lower())
            
            # Paso 3: Quitar guiones extra al inicio o al final
            data['slug'] = slug_crudo.strip('-')
            
        return data


# 3. ESQUEMA UPDATE: Lo que el frontend envía en un PATCH (Editar perfil).
# Fíjate que NO hereda de BusinessBase porque aquí TODO debe ser opcional.
class BusinessUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    display_name: Optional[str] = Field(None, min_length=2, max_length=120)
    timezone: Optional[str] = Field(None, max_length=50)
    logo: Optional[str] = None
    # Nota de Arquitecto: El 'slug' normalmente NO se deja actualizar, 
    # porque rompería los enlaces (URLs) o códigos QR que el negocio ya haya impreso.


# 4. ESQUEMA RESPONSE: Lo que el servidor le responde al frontend (GET).
class BusinessResponse(BusinessBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    slug: str
    created_at: datetime
    updated_at: datetime

    # LA MAGIA DE PYDANTIC V2:
    # Esto le dice a Pydantic: "No te asustes si recibes un objeto de SQLAlchemy en lugar de un diccionario, tú léelo y conviértelo a JSON".
    model_config = ConfigDict(from_attributes=True)