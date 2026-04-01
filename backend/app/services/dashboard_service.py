from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.cash_session import CashSession, CashStatus
from app.models.client import Client
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.dashboard import CashSummary, DashboardSummary, RecentTransactionOut


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self) -> DashboardSummary:
        today_start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        active_clients: int = (
            self.db.query(func.count(Client.id))
            .filter(Client.is_active == True)  # noqa: E712
            .scalar()
            or 0
        )

        transactions_today: int = (
            self.db.query(func.count(Transaction.id))
            .filter(
                Transaction.created_at >= today_start,
                Transaction.status == TransactionStatus.ACTIVE,
            )
            .scalar()
            or 0
        )

        commission_today: Decimal = (
            self.db.query(func.coalesce(func.sum(Transaction.commission), 0))
            .filter(
                Transaction.created_at >= today_start,
                Transaction.status == TransactionStatus.ACTIVE,
            )
            .scalar()
            or Decimal("0")
        )

        # Cash session info
        open_cash: CashSession | None = (
            self.db.query(CashSession)
            .filter(CashSession.status == CashStatus.open)
            .first()
        )

        cash = CashSummary(
            is_open=open_cash is not None,
            opening_mxn=open_cash.opening_amount_mxn if open_cash else Decimal("0"),
            opening_gtq=open_cash.opening_amount_gtq if open_cash else Decimal("0"),
        )

        recent_rows = (
            self.db.query(Transaction, Client.full_name)
            .join(Client, Transaction.client_id == Client.id)
            .filter(Transaction.status == TransactionStatus.ACTIVE)
            .order_by(Transaction.created_at.desc())
            .limit(5)
            .all()
        )

        recent_transactions = [
            RecentTransactionOut(
                id=txn.id,
                code=txn.code,
                client_name=client_name,
                transaction_type=txn.transaction_type.value,
                amount_mxn=txn.amount_mxn,
                amount_gtq=txn.amount_gtq,
                commission=txn.commission,
                status=txn.status.value,
            )
            for txn, client_name in recent_rows
        ]

        return DashboardSummary(
            active_clients=active_clients,
            transactions_today=transactions_today,
            commission_today=commission_today,
            cash=cash,
            recent_transactions=recent_transactions,
        )
