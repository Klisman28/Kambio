import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class IdType(str, enum.Enum):
    passport = "passport"
    national_id = "national_id"
    tax_id = "tax_id"
    other = "other"


class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    phone = Column(String(30))
    email = Column(String(255))
    address = Column(Text)
    id_type = Column(Enum(IdType, name="id_type"))
    id_number = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text)

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Client code={self.code} name={self.full_name}>"
