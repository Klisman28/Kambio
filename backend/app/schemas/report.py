from decimal import Decimal
from typing import List

from pydantic import BaseModel

from app.models.transaction import TransactionType
from app.schemas.cash import CashSessionOut
from app.schemas.transaction import TransactionOut


class TransactionReportSummary(BaseModel):
    total_transactions: int
    total_commission: Decimal
    total_amount_mxn: Decimal
    total_amount_gtq: Decimal


class TransactionReport(BaseModel):
    summary: TransactionReportSummary
    transactions: List[TransactionOut]


class CashReportSummary(BaseModel):
    total_sessions: int
    total_difference_mxn: Decimal
    total_difference_gtq: Decimal


class CashReport(BaseModel):
    summary: CashReportSummary
    sessions: List[CashSessionOut]


# ── Analytics ────────────────────────────────────────────────────────────────

class DailyDataPoint(BaseModel):
    """Un punto por día calendario dentro del rango solicitado."""
    date: str           # "YYYY-MM-DD"
    count: int
    amount_mxn: Decimal
    amount_gtq: Decimal
    commission: Decimal


class TypeDistributionItem(BaseModel):
    """Agregado por tipo de transacción dentro del rango solicitado."""
    transaction_type: TransactionType
    count: int
    total_mxn: Decimal
    total_gtq: Decimal
    total_commission: Decimal


class TransactionAnalytics(BaseModel):
    """
    Datos pre-agregados para gráficas de la UI de reportes.
    Solo incluye transacciones ACTIVE.
    """
    start_date: str                             # "YYYY-MM-DD"
    end_date: str                               # "YYYY-MM-DD"
    daily_series: List[DailyDataPoint]          # para gráficas de línea/barra por día
    type_distribution: List[TypeDistributionItem]  # para donut/pie por tipo
