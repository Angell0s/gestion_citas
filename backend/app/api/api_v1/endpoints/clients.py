# backend/app/api/api_v1/endpoints/clients.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.schemas.users import UserRead # Tu schema

router = APIRouter()

@router.get("/", response_model=list[UserRead])
def get_clients(db: Session = Depends(get_db)):
    # Aquí va la lógica o llamada al servicio
    return []