from datetime import date, datetime, time
from decimal import Decimal
from typing import List, NamedTuple, Optional
from uuid import UUID

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.ledger_entry import Currency, EntryDirection, LedgerEntry
from app.models.transaction import Transaction, TransactionStatus, TransactionType


class LedgerEntryRow(NamedTuple):
    """Resultado enriquecido del JOIN ledger_entries + transactions."""
    entry: LedgerEntry
    transaction_code: str
    transaction_type: TransactionType
    transaction_notes: Optional[str]


class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_balance(self, client_id: UUID, currency: Currency) -> Decimal:
        """
        Calcula el saldo actual del cliente en la divisa indicada.
        Solo considera transacciones ACTIVE.
        CREDIT = entra al cliente (+), DEBIT = sale del cliente (-).
        """
        result = (
            self.db.query(
                func.coalesce(
                    func.sum(
                        case(
                            (LedgerEntry.direction == EntryDirection.CREDIT, LedgerEntry.amount),
                            else_=-LedgerEntry.amount,
                        )
                    ),
                    Decimal("0"),
                )
            )
            .join(Transaction, LedgerEntry.transaction_id == Transaction.id)
            .filter(
                LedgerEntry.client_id == client_id,
                LedgerEntry.currency == currency,
                Transaction.status == TransactionStatus.ACTIVE,
            )
            .scalar()
        )
        return result or Decimal("0")

    def _base_query(
        self,
        client_id: UUID,
        currency: Currency | None,
        date_from: date | None,
        date_to: date | None,
    ):
        """Query base compartida por get_entries y count_entries."""
        q = (
            self.db.query(
                LedgerEntry,
                Transaction.code,
                Transaction.transaction_type,
                Transaction.notes,
            )
            .join(Transaction, LedgerEntry.transaction_id == Transaction.id)
            .filter(
                LedgerEntry.client_id == client_id,
                Transaction.status == TransactionStatus.ACTIVE,
            )
        )
        if currency:
            q = q.filter(LedgerEntry.currency == currency)
        if date_from:
            start_dt = datetime.combine(date_from, time.min)
            q = q.filter(LedgerEntry.created_at >= start_dt)
        if date_to:
            end_dt = datetime.combine(date_to, time.max)
            q = q.filter(LedgerEntry.created_at <= end_dt)
        return q

    def get_entries(
        self,
        client_id: UUID,
        currency: Currency | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[LedgerEntryRow]:
        """Historial enriquecido del libro mayor, paginado, orden cronológico desc."""
        rows = (
            self._base_query(client_id, currency, date_from, date_to)
            .order_by(LedgerEntry.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            LedgerEntryRow(
                entry=entry,
                transaction_code=code,
                transaction_type=txn_type,
                transaction_notes=notes,
            )
            for entry, code, txn_type, notes in rows
        ]

    def count_entries(
        self,
        client_id: UUID,
        currency: Currency | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> int:
        """Cuenta total de entradas para metadata de paginación."""
        return (
            self._base_query(client_id, currency, date_from, date_to)
            .with_entities(func.count(LedgerEntry.id))
            .scalar()
            or 0
        )

    def create(self, entry: LedgerEntry) -> LedgerEntry:
        self.db.add(entry)
        # No flush aquí; el servicio controla el flush y commit
        return entry
