from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.ledger_entry import Currency, EntryDirection
from app.models.transaction import TransactionType


# ── Posición financiera ──────────────────────────────────────────────────────

class BalancePosition(str, Enum):
    """
    Interpretación semántica del saldo neto de un cliente en una divisa.

    Convención de signo (perspectiva empresa — accounts receivable):
      raw_balance > 0  →  CLIENT_OWES   el cliente nos debe esa cantidad
      raw_balance < 0  →  COMPANY_OWES  le debemos al cliente esa cantidad
      raw_balance == 0 →  SETTLED       cuenta saldada
    """
    CLIENT_OWES = "CLIENT_OWES"    # el cliente me debe
    COMPANY_OWES = "COMPANY_OWES"  # yo le debo al cliente
    SETTLED = "SETTLED"            # saldo cero — saldado


class CurrencyBalance(BaseModel):
    """Posición financiera de un cliente en una sola divisa."""
    raw_balance: Decimal
    """Saldo con signo: positivo = debe al negocio, negativo = negocio le debe."""
    absolute_balance: Decimal
    """Valor absoluto del saldo, siempre >= 0."""
    position: BalancePosition
    """Interpretación financiera del signo."""
    display_label: str
    """Etiqueta legible para UI: 'El cliente debe' | 'A favor del cliente' | 'Saldado'."""


# ── Saldo agregado del cliente ───────────────────────────────────────────────

class BalanceOut(BaseModel):
    client_id: UUID
    mxn: CurrencyBalance
    gtq: CurrencyBalance

    # ── Equivalencias referenciales ─────────────────────────────────────────
    # IMPORTANTE: estos campos son puramente visuales. NO son saldo oficial.
    # Solo se calculan si el consumidor envía reference_exchange_rate.
    # La tasa la provee el operador; el sistema no tiene tasa automática.
    equivalent_in_mxn: Optional[Decimal] = None
    """Saldo GTQ convertido a MXN a la tasa de referencia. Solo referencial."""
    equivalent_in_gtq: Optional[Decimal] = None
    """Saldo MXN convertido a GTQ a la tasa de referencia. Solo referencial."""
    reference_exchange_rate: Optional[Decimal] = None
    """
    Tasa enviada por el consumidor (MXN por 1 GTQ).
    Convención: reference_exchange_rate = amount_mxn / amount_gtq.
    Solo para equivalencia visual — no afecta el saldo oficial.
    """


# ── Libro mayor ──────────────────────────────────────────────────────────────

class LedgerEntryOut(BaseModel):
    """
    Una fila del libro mayor enriquecida con contexto de la transacción.

    Semántica de direction para la UI:
      CREDIT (+) → dinero que ENTRA al cliente en esa divisa
      DEBIT  (−) → dinero que SALE del cliente en esa divisa

    Solo aparecen entradas de transacciones ACTIVE.
    Las transacciones anuladas se excluyen porque no afectan el saldo real.
    """
    id: UUID
    transaction_id: UUID
    transaction_code: str           # e.g. "TXN-20260401-00001"
    transaction_type: TransactionType  # e.g. SELL_MXN, PAYMENT, etc.
    currency: Currency              # MXN | GTQ
    direction: EntryDirection       # CREDIT (+) | DEBIT (−)
    amount: Decimal
    balance_after: Decimal          # saldo snapshot tras este movimiento
    created_at: datetime
    notes: Optional[str] = None     # notas de la transacción origen, si existen


class LedgerResponse(BaseModel):
    client_id: UUID
    total: int                      # total de entradas en el filtro (para paginación)
    skip: int
    limit: int
    entries: List[LedgerEntryOut]
    balance: BalanceOut             # saldo actual (siempre calculado, nunca almacenado)
