# backend\models\__init__.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .user import User
from .business import Businesses, BusinessHours, Role, BusinessMember
from .clients import Client, ClientReputation
from .appointments import Service, Appointment