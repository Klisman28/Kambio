from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cash_session import CashSession, CashStatus


class CashRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_open(self) -> Optional[CashSession]:
        return (
            self.db.query(CashSession)
            .filter(CashSession.status == CashStatus.open)
            .first()
        )

    def get_by_id(self, session_id: UUID) -> Optional[CashSession]:
        return self.db.query(CashSession).filter(CashSession.id == session_id).first()

    def list(self, skip: int = 0, limit: int = 20) -> List[CashSession]:
        return (
            self.db.query(CashSession)
            .order_by(CashSession.opened_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, session: CashSession) -> CashSession:
        self.db.add(session)
        self.db.flush()
        return session

    def update(self, session: CashSession) -> CashSession:
        self.db.flush()
        return session
