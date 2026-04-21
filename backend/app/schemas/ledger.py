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


# ── Ledger agrupado por transacción ──────────────────────────────────────────
#
# Diferencia con LedgerResponse (detallado):
#   - LedgerResponse: una fila por ledger_entry (una por divisa por movimiento).
#     Dos movimientos de distinta divisa de la misma transacción → dos filas.
#   - LedgerGroupedResponse: una fila por transacción, con columnas separadas
#     para egreso/ingreso por divisa. Ideal para vista tipo Excel.
#
# Convención egreso / ingreso (perspectiva empresa):
#   egreso  = CREDIT en ledger (empresa dio al cliente)
#   ingreso = DEBIT  en ledger (empresa recibió del cliente)
#
# Convención net (perspectiva cuentas por cobrar):
#   net = ingreso - egreso
#   net > 0  → CLIENT_OWES  (empresa recibió más de lo que dio → cliente debe)
#   net < 0  → COMPANY_OWES (empresa dio más de lo que recibió → le debemos al cliente)
#   net = 0  → SETTLED

class LedgerGroupedRow(BaseModel):
    """Una fila por transacción en la vista agrupada del libro mayor."""
    transaction_id: UUID
    date: datetime
    reference: str                  # código de transacción, e.g. TXN-20260421-00001
    operation: TransactionType
    egreso_mxn: Decimal             # MXN que la empresa dio al cliente (CREDIT MXN)
    egreso_gtq: Decimal             # GTQ que la empresa dio al cliente (CREDIT GTQ)
    ingreso_mxn: Decimal            # MXN que la empresa recibió del cliente (DEBIT MXN)
    ingreso_gtq: Decimal            # GTQ que la empresa recibió del cliente (DEBIT GTQ)
    notes: Optional[str] = None
    status: str


class LedgerGroupedSummary(BaseModel):
    """
    Totales y posición neta para el rango consultado (no afectado por paginación).

    net_mxn = total_ingreso_mxn - total_egreso_mxn
    net_gtq = total_ingreso_gtq - total_egreso_gtq

    Etiquetas:
      CLIENT_OWES  → "El cliente debe"      (net > 0)
      COMPANY_OWES → "A favor del cliente"  (net < 0)
      SETTLED      → "Saldado"              (net = 0)
    """
    total_egreso_mxn: Decimal
    total_ingreso_mxn: Decimal
    total_egreso_gtq: Decimal
    total_ingreso_gtq: Decimal
    net_mxn: Decimal
    net_gtq: Decimal
    net_mxn_label: str
    net_gtq_label: str


class LedgerGroupedResponse(BaseModel):
    """
    Vista agrupada del libro mayor: una fila por transacción.
    El summary refleja el rango completo de fechas; las rows están paginadas.
    """
    client_id: UUID
    total: int
    skip: int
    limit: int
    summary: LedgerGroupedSummary
    rows: List[LedgerGroupedRow]
