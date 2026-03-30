import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Index, Numeric, Uuid

from app.db.base_class import Base


class Currency(str, enum.Enum):
    MXN = "MXN"
    GTQ = "GTQ"


class EntryDirection(str, enum.Enum):
    DEBIT = "DEBIT"    # sale del cliente
    CREDIT = "CREDIT"  # entra al cliente


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

    transaction_id = Column(Uuid(as_uuid=True), ForeignKey("transactions.id"), nullable=False)
    client_id = Column(Uuid(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    currency = Column(Enum(Currency, name="currency"), nullable=False)
    direction = Column(Enum(EntryDirection, name="entry_direction"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)

    # Snapshot del saldo del cliente en esta divisa después de este movimiento.
    # Permite construir running balance sin recalcular toda la historia.
    balance_after = Column(Numeric(15, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_ledger_amount_positive"),
        Index("ix_ledger_client_currency", "client_id", "currency"),
        Index("ix_ledger_client_currency_created", "client_id", "currency", "created_at"),
        Index("ix_ledger_transaction", "transaction_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<LedgerEntry client={self.client_id} "
            f"{self.direction} {self.amount} {self.currency}>"
        )
