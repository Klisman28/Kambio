import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Index, Numeric, SmallInteger, Text, Uuid

from app.db.base_class import Base


class CashStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class CashSession(Base):
    __tablename__ = "cash_sessions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(
        Enum(CashStatus, name="cash_status"),
        nullable=False,
        default=CashStatus.open,
    )

    # Columna auxiliar para garantizar una sola caja abierta a nivel DB.
    # Valor 1 cuando status='open', NULL cuando status='closed'.
    # MySQL ignora NULL en índices UNIQUE, permitiendo múltiples filas cerradas.
    unique_open = Column(SmallInteger, nullable=True, default=1)

    opening_amount_mxn = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    opening_amount_gtq = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))

    # Saldo corriente — se actualiza con cada transacción
    current_amount_mxn = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    current_amount_gtq = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))

    closing_amount_mxn = Column(Numeric(15, 2))
    closing_amount_gtq = Column(Numeric(15, 2))
    difference_mxn = Column(Numeric(15, 2))
    difference_gtq = Column(Numeric(15, 2))

    opened_by = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    closed_by = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    opened_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime(timezone=True))
    notes = Column(Text)

    __table_args__ = (
        CheckConstraint("opening_amount_mxn >= 0", name="ck_cash_opening_mxn_positive"),
        CheckConstraint("opening_amount_gtq >= 0", name="ck_cash_opening_gtq_positive"),
        # UNIQUE sobre unique_open garantiza que solo 1 fila tenga valor 1.
        # Las filas cerradas tienen unique_open=NULL y no participan en el constraint.
        Index("uq_one_open_cash_session", "unique_open", unique=True),
    )

    def __repr__(self) -> str:
        return f"<CashSession id={self.id} status={self.status}>"
