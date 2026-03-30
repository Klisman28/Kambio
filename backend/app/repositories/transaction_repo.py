from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionStatus


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, txn_id: UUID) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == txn_id).first()

    def get_by_code(self, code: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.code == code).first()

    def list_by_client(
        self,
        client_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.client_id == client_id)
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_all(self) -> int:
        from sqlalchemy import func
        return self.db.query(func.count(Transaction.id)).scalar() or 0

    def create(self, txn: Transaction) -> Transaction:
        self.db.add(txn)
        self.db.flush()
        return txn

    def update(self, txn: Transaction) -> Transaction:
        self.db.flush()
        return txn
