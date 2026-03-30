from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.models.ledger_entry import Currency, EntryDirection


class LedgerEntryOut(BaseModel):
    id: UUID
    transaction_id: UUID
    currency: Currency
    direction: EntryDirection
    amount: Decimal
    balance_after: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class BalanceOut(BaseModel):
    client_id: UUID
    mxn: Decimal
    gtq: Decimal


class LedgerResponse(BaseModel):
    client_id: UUID
    entries: List[LedgerEntryOut]
    balance: BalanceOut
