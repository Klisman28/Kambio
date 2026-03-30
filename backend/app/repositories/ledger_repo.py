from decimal import Decimal
from typing import List
from uuid import UUID

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.ledger_entry import Currency, EntryDirection, LedgerEntry
from app.models.transaction import Transaction, TransactionStatus


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

    def get_entries(
        self,
        client_id: UUID,
        currency: Currency | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[LedgerEntry]:
        """Historial de entradas del libro mayor, paginado."""
        q = (
            self.db.query(LedgerEntry)
            .join(Transaction, LedgerEntry.transaction_id == Transaction.id)
            .filter(
                LedgerEntry.client_id == client_id,
                Transaction.status == TransactionStatus.ACTIVE,
            )
        )
        if currency:
            q = q.filter(LedgerEntry.currency == currency)
        return q.order_by(LedgerEntry.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, entry: LedgerEntry) -> LedgerEntry:
        self.db.add(entry)
        # No flush aquí; el servicio controla el flush y commit
        return entry
