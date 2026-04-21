import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.cash_session import CashSession, CashStatus
from app.models.client import Client
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.report import (
    CashReport,
    CashReportSummary,
    DailyDataPoint,
    TransactionAnalytics,
    TransactionReport,
    TransactionReportSummary,
    TypeDistributionItem,
)
from app.schemas.transaction import TransactionOut


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_transaction_report(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ) -> TransactionReport:
        rows = (
            self.db.query(Transaction, Client.full_name)
            .join(Client, Transaction.client_id == Client.id)
            .filter(
                Transaction.status == TransactionStatus.ACTIVE,
                Transaction.created_at >= start_date,
                Transaction.created_at <= end_date,
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

        total_tx = len(rows)
        total_comm = Decimal("0")
        total_mxn = Decimal("0")
        total_gtq = Decimal("0")
        tx_out_list: list[TransactionOut] = []

        for txn, client_name in rows:
            total_comm += txn.commission
            total_mxn += txn.amount_mxn
            total_gtq += txn.amount_gtq
            out = TransactionOut.model_validate(txn)
            out.client_name = client_name
            tx_out_list.append(out)

        summary = TransactionReportSummary(
            total_transactions=total_tx,
            total_commission=total_comm,
            total_amount_mxn=total_mxn,
            total_amount_gtq=total_gtq,
        )

        return TransactionReport(
            summary=summary,
            transactions=tx_out_list,
        )

    def get_cash_summary_report(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ) -> CashReport:
        # Fetch closed cash sessions within range
        sessions_query = self.db.query(CashSession).filter(
            CashSession.status == CashStatus.closed,
            CashSession.opened_at >= start_date,
            CashSession.opened_at <= end_date,
        )

        sessions = sessions_query.order_by(CashSession.opened_at.desc()).all()

        total_sessions = len(sessions)
        diff_mxn = Decimal("0")
        diff_gtq = Decimal("0")

        for s in sessions:
            if s.difference_mxn:
                diff_mxn += s.difference_mxn
            if s.difference_gtq:
                diff_gtq += s.difference_gtq

        summary = CashReportSummary(
            total_sessions=total_sessions,
            total_difference_mxn=diff_mxn,
            total_difference_gtq=diff_gtq,
        )

        return CashReport(
            summary=summary,
            sessions=sessions,
        )

    def get_transaction_analytics(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> TransactionAnalytics:
        """
        Devuelve dos agregaciones DB-side para alimentar gráficas:
        - daily_series: una fila por día con count, MXN, GTQ y comisión.
        - type_distribution: una fila por tipo de transacción con los mismos campos.
        Solo transacciones ACTIVE dentro del rango [start_date, end_date].
        """
        base_filter = [
            Transaction.status == TransactionStatus.ACTIVE,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
        ]

        # ── 1. Serie diaria (GROUP BY DATE(created_at)) ───────────────────────
        daily_rows = (
            self.db.query(
                func.date(Transaction.created_at).label("day"),
                func.count(Transaction.id).label("count"),
                func.coalesce(func.sum(Transaction.amount_mxn), 0).label("amount_mxn"),
                func.coalesce(func.sum(Transaction.amount_gtq), 0).label("amount_gtq"),
                func.coalesce(func.sum(Transaction.commission), 0).label("commission"),
            )
            .filter(*base_filter)
            .group_by(func.date(Transaction.created_at))
            .order_by(func.date(Transaction.created_at))
            .all()
        )

        daily_series = [
            DailyDataPoint(
                date=str(row.day),
                count=row.count,
                amount_mxn=Decimal(str(row.amount_mxn)),
                amount_gtq=Decimal(str(row.amount_gtq)),
                commission=Decimal(str(row.commission)),
            )
            for row in daily_rows
        ]

        # ── 2. Distribución por tipo (GROUP BY transaction_type) ──────────────
        type_rows = (
            self.db.query(
                Transaction.transaction_type,
                func.count(Transaction.id).label("count"),
                func.coalesce(func.sum(Transaction.amount_mxn), 0).label("total_mxn"),
                func.coalesce(func.sum(Transaction.amount_gtq), 0).label("total_gtq"),
                func.coalesce(func.sum(Transaction.commission), 0).label("total_commission"),
            )
            .filter(*base_filter)
            .group_by(Transaction.transaction_type)
            .order_by(func.count(Transaction.id).desc())
            .all()
        )

        type_distribution = [
            TypeDistributionItem(
                transaction_type=row.transaction_type,
                count=row.count,
                total_mxn=Decimal(str(row.total_mxn)),
                total_gtq=Decimal(str(row.total_gtq)),
                total_commission=Decimal(str(row.total_commission)),
            )
            for row in type_rows
        ]

        return TransactionAnalytics(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            daily_series=daily_series,
            type_distribution=type_distribution,
        )
