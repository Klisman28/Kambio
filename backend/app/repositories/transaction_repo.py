from datetime import date, datetime, time
from typing import List, NamedTuple, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.transaction import Transaction, TransactionStatus, TransactionType


class TransactionRow(NamedTuple):
    transaction: Transaction
    client_name: str


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

    def list_all(
        self,
        skip: int = 0,
        limit: int = 50,
        status_filter: str | None = None,
        client_id: UUID | None = None,
        transaction_type: TransactionType | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> List[TransactionRow]:
        q = (
            self.db.query(Transaction, Client.full_name)
            .join(Client, Transaction.client_id == Client.id)
        )
        if status_filter:
            q = q.filter(Transaction.status == status_filter)
        if client_id:
            q = q.filter(Transaction.client_id == client_id)
        if transaction_type:
            q = q.filter(Transaction.transaction_type == transaction_type)
        if date_from:
            q = q.filter(Transaction.created_at >= datetime.combine(date_from, time.min))
        if date_to:
            q = q.filter(Transaction.created_at <= datetime.combine(date_to, time.max))
        rows = q.order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
        return [TransactionRow(transaction=txn, client_name=name) for txn, name in rows]

    def count_by_date(self, d: date) -> int:
        """Count of transactions created on a specific calendar date (UTC)."""
        start = datetime.combine(d, time.min)
        end = datetime.combine(d, time.max)
        return (
            self.db.query(func.count(Transaction.id))
            .filter(Transaction.created_at >= start, Transaction.created_at <= end)
            .scalar()
            or 0
        )

    def create(self, txn: Transaction) -> Transaction:
        self.db.add(txn)
        self.db.flush()
        return txn

    def update(self, txn: Transaction) -> Transaction:
        self.db.flush()
        return txn
