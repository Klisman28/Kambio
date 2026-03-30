import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Index, Numeric, Text, text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class CashStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class CashSession(Base):
    __tablename__ = "cash_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(
        Enum(CashStatus, name="cash_status"),
        nullable=False,
        default=CashStatus.open,
    )

    opening_amount_mxn = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    opening_amount_gtq = Column(Numeric(15, 2), nullable=False, default=Decimal("0"))
    closing_amount_mxn = Column(Numeric(15, 2))
    closing_amount_gtq = Column(Numeric(15, 2))
    difference_mxn = Column(Numeric(15, 2))
    difference_gtq = Column(Numeric(15, 2))

    opened_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    closed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    opened_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime(timezone=True))
    notes = Column(Text)

    __table_args__ = (
        CheckConstraint("opening_amount_mxn >= 0", name="ck_cash_opening_mxn_positive"),
        CheckConstraint("opening_amount_gtq >= 0", name="ck_cash_opening_gtq_positive"),
        # Partial unique index: solo una caja puede estar abierta a la vez (PostgreSQL)
        Index(
            "uq_one_open_cash_session",
            "status",
            unique=True,
            postgresql_where=text("status = 'open'"),
        ),
    )

    def __repr__(self) -> str:
        return f"<CashSession id={self.id} status={self.status}>"
