from datetime import date, datetime, time
from decimal import Decimal
from typing import List, NamedTuple, Optional
from uuid import UUID

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.ledger_entry import Currency, EntryDirection, LedgerEntry
from app.models.transaction import Transaction, TransactionStatus, TransactionType


class LedgerEntryRow(NamedTuple):
    """Resultado enriquecido del JOIN ledger_entries + transactions."""
    entry: LedgerEntry
    transaction_code: str
    transaction_type: TransactionType
    transaction_notes: Optional[str]


class GroupedLedgerRow(NamedTuple):
    """Una fila por transacción con egreso/ingreso por divisa agregados."""
    transaction_id: UUID
    code: str
    transaction_type: TransactionType
    created_at: datetime
    notes: Optional[str]
    status: str
    egreso_mxn: Decimal
    egreso_gtq: Decimal
    ingreso_mxn: Decimal
    ingreso_gtq: Decimal


class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_balance(self, client_id: UUID, currency: Currency) -> Decimal:
        """
        Calcula el saldo actual del cliente en la divisa indicada.
        Solo considera transacciones ACTIVE.
        CREDIT = entra al cliente (+), DEBIT = sale del cliente (-).
        """
        result = (
            self.db.query(
                func.coalesce(
                    func.sum(
                        case(
                            (LedgerEntry.direction == EntryDirection.CREDIT, LedgerEntry.amount),
                            else_=-LedgerEntry.amount,
                        )
                    ),
                    Decimal("0"),
                )
            )
            .join(Transaction, LedgerEntry.transaction_id == Transaction.id)
            .filter(
                LedgerEntry.client_id == client_id,
                LedgerEntry.currency == currency,
                Transaction.status == TransactionStatus.ACTIVE,
            )
            .scalar()
        )
        return result or Decimal("0")

    def _base_query(
        self,
        client_id: UUID,
        currency: Currency | None,
        date_from: date | None,
        date_to: date | None,
    ):
        """Query base compartida por get_entries y count_entries."""
        q = (
            self.db.query(
                LedgerEntry,
                Transaction.code,
                Transaction.transaction_type,
                Transaction.notes,
            )
            .join(Transaction, LedgerEntry.transaction_id == Transaction.id)
            .filter(
                LedgerEntry.client_id == client_id,
                Transaction.status == TransactionStatus.ACTIVE,
            )
        )
        if currency:
            q = q.filter(LedgerEntry.currency == currency)
        if date_from:
            start_dt = datetime.combine(date_from, time.min)
            q = q.filter(LedgerEntry.created_at >= start_dt)
        if date_to:
            end_dt = datetime.combine(date_to, time.max)
            q = q.filter(LedgerEntry.created_at <= end_dt)
        return q

    def get_entries(
        self,
        client_id: UUID,
        currency: Currency | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[LedgerEntryRow]:
        """Historial enriquecido del libro mayor, paginado, orden cronológico desc."""
        rows = (
            self._base_query(client_id, currency, date_from, date_to)
            .order_by(LedgerEntry.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            LedgerEntryRow(
                entry=entry,
                transaction_code=code,
                transaction_type=txn_type,
                transaction_notes=notes,
            )
            for entry, code, txn_type, notes in rows
        ]

    def count_entries(
        self,
        client_id: UUID,
        currency: Currency | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> int:
        """Cuenta total de entradas para metadata de paginación."""
        return (
            self._base_query(client_id, currency, date_from, date_to)
            .with_entities(func.count(LedgerEntry.id))
            .scalar()
            or 0
        )

    def create(self, entry: LedgerEntry) -> LedgerEntry:
        self.db.add(entry)
        # No flush aquí; el servicio controla el flush y commit
        return entry

    # ── Grouped ledger ───────────────────────────────────────────────────────

    def _grouped_base_query(
        self,
        client_id: UUID,
        date_from: date | None,
        date_to: date | None,
    ):
        """
        Query base para la vista agrupada: una fila por transacción.
        egreso = CREDIT (empresa → cliente), ingreso = DEBIT (cliente → empresa).
        Solo transacciones ACTIVE con al menos una ledger_entry para este cliente.
        """
        egreso_mxn = func.coalesce(func.sum(
            case(
                ((LedgerEntry.direction == EntryDirection.CREDIT) & (LedgerEntry.currency == Currency.MXN),
                 LedgerEntry.amount),
                else_=Decimal("0"),
            )
        ), Decimal("0")).label("egreso_mxn")

        egreso_gtq = func.coalesce(func.sum(
            case(
                ((LedgerEntry.direction == EntryDirection.CREDIT) & (LedgerEntry.currency == Currency.GTQ),
                 LedgerEntry.amount),
                else_=Decimal("0"),
            )
        ), Decimal("0")).label("egreso_gtq")

        ingreso_mxn = func.coalesce(func.sum(
            case(
                ((LedgerEntry.direction == EntryDirection.DEBIT) & (LedgerEntry.currency == Currency.MXN),
                 LedgerEntry.amount),
                else_=Decimal("0"),
            )
        ), Decimal("0")).label("ingreso_mxn")

        ingreso_gtq = func.coalesce(func.sum(
            case(
                ((LedgerEntry.direction == EntryDirection.DEBIT) & (LedgerEntry.currency == Currency.GTQ),
                 LedgerEntry.amount),
                else_=Decimal("0"),
            )
        ), Decimal("0")).label("ingreso_gtq")

        q = (
            self.db.query(
                Transaction.id,
                Transaction.code,
                Transaction.transaction_type,
                Transaction.created_at,
                Transaction.notes,
                Transaction.status,
                egreso_mxn,
                egreso_gtq,
                ingreso_mxn,
                ingreso_gtq,
            )
            .join(
                LedgerEntry,
                (LedgerEntry.transaction_id == Transaction.id)
                & (LedgerEntry.client_id == client_id),
            )
            .filter(
                Transaction.client_id == client_id,
                Transaction.status == TransactionStatus.ACTIVE,
            )
            .group_by(
                Transaction.id,
                Transaction.code,
                Transaction.transaction_type,
                Transaction.created_at,
                Transaction.notes,
                Transaction.status,
            )
        )
        if date_from:
            q = q.filter(Transaction.created_at >= datetime.combine(date_from, time.min))
        if date_to:
            q = q.filter(Transaction.created_at <= datetime.combine(date_to, time.max))
        return q

    def get_grouped(
        self,
        client_id: UUID,
        date_from: date | None = None,
        date_to: date | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[GroupedLedgerRow]:
        rows = (
            self._grouped_base_query(client_id, date_from, date_to)
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            GroupedLedgerRow(
                transaction_id=r.id,
                code=r.code,
                transaction_type=r.transaction_type,
                created_at=r.created_at,
                notes=r.notes,
                status=r.status,
                egreso_mxn=Decimal(str(r.egreso_mxn)),
                egreso_gtq=Decimal(str(r.egreso_gtq)),
                ingreso_mxn=Decimal(str(r.ingreso_mxn)),
                ingreso_gtq=Decimal(str(r.ingreso_gtq)),
            )
            for r in rows
        ]

    def count_grouped(
        self,
        client_id: UUID,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> int:
        """Cuenta de transacciones distintas en el rango (para metadata de paginación)."""
        return (
            self.db.query(func.count(Transaction.id.distinct()))
            .join(
                LedgerEntry,
                (LedgerEntry.transaction_id == Transaction.id)
                & (LedgerEntry.client_id == client_id),
            )
            .filter(
                Transaction.client_id == client_id,
                Transaction.status == TransactionStatus.ACTIVE,
                *(
                    [Transaction.created_at >= datetime.combine(date_from, time.min)]
                    if date_from else []
                ),
                *(
                    [Transaction.created_at <= datetime.combine(date_to, time.max)]
                    if date_to else []
                ),
            )
            .scalar()
            or 0
        )

    def get_grouped_totals(
        self,
        client_id: UUID,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> GroupedLedgerRow:
        """Totales agregados sin paginar — base del summary."""
        subq = self._grouped_base_query(client_id, date_from, date_to).subquery()
        row = self.db.query(
            func.coalesce(func.sum(subq.c.egreso_mxn), Decimal("0")),
            func.coalesce(func.sum(subq.c.egreso_gtq), Decimal("0")),
            func.coalesce(func.sum(subq.c.ingreso_mxn), Decimal("0")),
            func.coalesce(func.sum(subq.c.ingreso_gtq), Decimal("0")),
        ).one()
        return GroupedLedgerRow(
            transaction_id=None,  # type: ignore[arg-type]
            code="",
            transaction_type=None,  # type: ignore[arg-type]
            created_at=None,  # type: ignore[arg-type]
            notes=None,
            status="",
            egreso_mxn=Decimal(str(row[0])),
            egreso_gtq=Decimal(str(row[1])),
            ingreso_mxn=Decimal(str(row[2])),
            ingreso_gtq=Decimal(str(row[3])),
        )
