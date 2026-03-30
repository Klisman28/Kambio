from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator, model_validator

from app.models.transaction import TransactionStatus, TransactionType


class TransactionCreate(BaseModel):
    client_id: UUID
    transaction_type: TransactionType
    amount_mxn: Decimal = Decimal("0")
    amount_gtq: Decimal = Decimal("0")
    commission: Decimal = Decimal("0")
    exchange_rate: Optional[Decimal] = None
    notes: Optional[str] = None

    @field_validator("amount_mxn", "amount_gtq", "commission")
    @classmethod
    def must_be_non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Los montos no pueden ser negativos")
        return v

    @model_validator(mode="after")
    def validate_amounts_by_type(self) -> "TransactionCreate":
        t = self.transaction_type
        mxn = self.amount_mxn
        gtq = self.amount_gtq

        if t in (TransactionType.SELL_MXN, TransactionType.BUY_MXN):
            if mxn <= 0 or gtq <= 0:
                raise ValueError(
                    f"{t} requiere amount_mxn > 0 y amount_gtq > 0"
                )
        elif t in (TransactionType.PAYMENT, TransactionType.WITHDRAWAL):
            active = (1 if mxn > 0 else 0) + (1 if gtq > 0 else 0)
            if active != 1:
                raise ValueError(
                    f"{t} requiere exactamente una divisa con monto > 0"
                )
        return self


class VoidRequest(BaseModel):
    void_reason: str

    @field_validator("void_reason")
    @classmethod
    def reason_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El motivo de anulación no puede estar vacío")
        return v.strip()


class TransactionOut(BaseModel):
    id: UUID
    code: str
    client_id: UUID
    cash_session_id: UUID
    transaction_type: TransactionType
    amount_mxn: Decimal
    amount_gtq: Decimal
    commission: Decimal
    exchange_rate: Optional[Decimal] = None
    status: TransactionStatus
    voided_by: Optional[UUID] = None
    voided_at: Optional[datetime] = None
    void_reason: Optional[str] = None
    void_of_id: Optional[UUID] = None
    created_by: UUID
    created_at: datetime
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
