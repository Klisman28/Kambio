from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.client import IdType


class ClientCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    id_type: Optional[IdType] = None
    id_number: Optional[str] = None
    notes: Optional[str] = None


class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    id_type: Optional[IdType] = None
    id_number: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class ClientOut(BaseModel):
    id: UUID
    code: str
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    id_type: Optional[IdType] = None
    id_number: Optional[str] = None
    is_active: bool
    notes: Optional[str] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
