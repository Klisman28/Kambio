import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class TransactionType(str, enum.Enum):
    # Empresa vende MXN al cliente: cliente entrega GTQ, recibe MXN
    SELL_MXN = "SELL_MXN"
    # Empresa compra MXN del cliente: cliente entrega MXN, recibe GTQ
    BUY_MXN = "BUY_MXN"
    # Abono al cliente (solo una divisa)
    PAYMENT = "PAYMENT"
    # Retiro del cliente (solo una divisa)
    WITHDRAWAL = "WITHDRAWAL"


class TransactionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    VOIDED = "VOIDED"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(30), unique=True, nullable=False, index=True)

    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    cash_session_id = Column(UUID(as_uuid=True), ForeignKey("cash_sessions.id"), nullable=False)

    transaction_type = Column(
        Enum(TransactionType, name="transaction_type"),
        nullable=False,
    )

    amount_mxn = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    amount_gtq = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    commission = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    exchange_rate = Column(Numeric(10, 6))

    status = Column(
        Enum(TransactionStatus, name="transaction_status"),
        nullable=False,
        default=TransactionStatus.ACTIVE,
    )

    # Anulación
    voided_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    voided_at = Column(DateTime(timezone=True))
    void_reason = Column(Text)
    void_of_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"))

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    notes = Column(Text)

    __table_args__ = (
        CheckConstraint("amount_mxn >= 0", name="ck_txn_amount_mxn_positive"),
        CheckConstraint("amount_gtq >= 0", name="ck_txn_amount_gtq_positive"),
        CheckConstraint(
            "amount_mxn > 0 OR amount_gtq > 0",
            name="ck_txn_at_least_one_amount",
        ),
        CheckConstraint("commission >= 0", name="ck_txn_commission_positive"),
        Index("ix_transactions_client_status", "client_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<Transaction code={self.code} type={self.transaction_type} status={self.status}>"
