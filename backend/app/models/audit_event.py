from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, JSON, Uuid

from app.db.base_class import Base


class AuditEvent(Base):
    """
    Log inmutable de acciones críticas del sistema.
    Solo INSERT — nunca UPDATE ni DELETE en producción.
    """

    __tablename__ = "audit_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)       # ej. "transaction.create"
    resource_type = Column(String(50), nullable=False)  # ej. "transaction"
    resource_id = Column(Uuid(as_uuid=True))

    ip_address = Column(String(45))
    payload = Column(JSON)  # snapshot antes/después del cambio

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<AuditEvent action={self.action} resource={self.resource_type}/{self.resource_id}>"
