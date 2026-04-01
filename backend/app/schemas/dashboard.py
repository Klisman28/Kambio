from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class RecentTransactionOut(BaseModel):
    id: UUID
    code: str
    client_name: str
    transaction_type: str
    amount_mxn: Decimal
    amount_gtq: Decimal
    commission: Decimal
    status: str

    model_config = {"from_attributes": True}


class CashSummary(BaseModel):
    is_open: bool
    opening_mxn: Decimal = Decimal("0")
    opening_gtq: Decimal = Decimal("0")


class DashboardSummary(BaseModel):
    active_clients: int
    transactions_today: int
    commission_today: Decimal
    cash: CashSummary
    recent_transactions: List[RecentTransactionOut]
