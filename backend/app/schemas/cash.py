from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.models.cash_session import CashStatus


class CashOpenRequest(BaseModel):
    opening_amount_mxn: Decimal = Decimal("0")
    opening_amount_gtq: Decimal = Decimal("0")
    notes: Optional[str] = None

    @field_validator("opening_amount_mxn", "opening_amount_gtq")
    @classmethod
    def must_be_non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("El monto de apertura no puede ser negativo")
        return v


class CashCloseRequest(BaseModel):
    closing_amount_mxn: Decimal
    closing_amount_gtq: Decimal
    notes: Optional[str] = None

    @field_validator("closing_amount_mxn", "closing_amount_gtq")
    @classmethod
    def must_be_non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("El monto de cierre no puede ser negativo")
        return v


class CashSessionOut(BaseModel):
    id: UUID
    status: CashStatus
    opening_amount_mxn: Decimal
    opening_amount_gtq: Decimal
    closing_amount_mxn: Optional[Decimal] = None
    closing_amount_gtq: Optional[Decimal] = None
    difference_mxn: Optional[Decimal] = None
    difference_gtq: Optional[Decimal] = None
    opened_by: UUID
    closed_by: Optional[UUID] = None
    opened_at: datetime
    closed_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
