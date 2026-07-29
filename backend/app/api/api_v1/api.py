# backend/app/api/api_v1/api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import clients, business, appointments

api_router = APIRouter()
api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])
# api_router.include_router(business.router, prefix="/business", tags=["Business"])
# api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])