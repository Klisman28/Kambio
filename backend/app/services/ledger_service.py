from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ledger_entry import Currency, EntryDirection, LedgerEntry
from app.models.transaction import Transaction
from app.repositories.ledger_repo import LedgerRepository
from app.schemas.ledger import (
    BalanceOut,
    BalancePosition,
    CurrencyBalance,
    LedgerEntryOut,
    LedgerGroupedResponse,
    LedgerGroupedRow,
    LedgerGroupedSummary,
    LedgerResponse,
)


class LedgerService:
    def __init__(self, db: Session):
        self.repo = LedgerRepository(db)

    # ── Interpretación financiera ────────────────────────────────────────────

    @staticmethod
    def _interpret_balance(raw: Decimal) -> CurrencyBalance:
        """
        Convierte un saldo bruto con signo en una CurrencyBalance semántica.

        Convención (perspectiva empresa — accounts receivable):
          raw > 0  → CLIENT_OWES   el cliente nos debe
          raw < 0  → COMPANY_OWES  nosotros le debemos al cliente
          raw == 0 → SETTLED       saldado
        """
        if raw > 0:
            position = BalancePosition.CLIENT_OWES
            label = "El cliente debe"
        elif raw < 0:
            position = BalancePosition.COMPANY_OWES
            label = "A favor del cliente"
        else:
            position = BalancePosition.SETTLED
            label = "Saldado"

        return CurrencyBalance(
            raw_balance=raw,
            absolute_balance=abs(raw),
            position=position,
            display_label=label,
        )

    # ── API pública ──────────────────────────────────────────────────────────

    def get_balance(
        self,
        client_id: UUID,
        reference_exchange_rate: Optional[Decimal] = None,
    ) -> BalanceOut:
        """
        Retorna la posición financiera del cliente con interpretación semántica.

        Si se provee reference_exchange_rate (MXN por 1 GTQ), se calculan
        equivalent_in_mxn y equivalent_in_gtq con fines referenciales únicamente.
        Esos campos NO son saldo oficial y no alteran raw_balance ni position.
        """
        raw_mxn = self.repo.get_balance(client_id, Currency.MXN)
        raw_gtq = self.repo.get_balance(client_id, Currency.GTQ)

        mxn_balance = self._interpret_balance(raw_mxn)
        gtq_balance = self._interpret_balance(raw_gtq)

        equivalent_in_mxn: Optional[Decimal] = None
        equivalent_in_gtq: Optional[Decimal] = None

        if reference_exchange_rate and reference_exchange_rate > 0:
            # GTQ → MXN: saldo GTQ × tasa (tasa = MXN/GTQ)
            equivalent_in_mxn = (raw_gtq * reference_exchange_rate).quantize(Decimal("0.01"))
            # MXN → GTQ: saldo MXN / tasa
            equivalent_in_gtq = (raw_mxn / reference_exchange_rate).quantize(Decimal("0.01"))

        return BalanceOut(
            client_id=client_id,
            mxn=mxn_balance,
            gtq=gtq_balance,
            equivalent_in_mxn=equivalent_in_mxn,
            equivalent_in_gtq=equivalent_in_gtq,
            reference_exchange_rate=reference_exchange_rate,
        )

    def get_ledger(
        self,
        client_id: UUID,
        currency: Optional[Currency] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        skip: int = 0,
        limit: int = 50,
        reference_exchange_rate: Optional[Decimal] = None,
    ) -> LedgerResponse:
        total = self.repo.count_entries(
            client_id, currency=currency, date_from=date_from, date_to=date_to
        )
        rows = self.repo.get_entries(
            client_id,
            currency=currency,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit,
        )
        balance = self.get_balance(client_id, reference_exchange_rate=reference_exchange_rate)

        entries = [
            LedgerEntryOut(
                id=row.entry.id,
                transaction_id=row.entry.transaction_id,
                transaction_code=row.transaction_code,
                transaction_type=row.transaction_type,
                currency=row.entry.currency,
                direction=row.entry.direction,
                amount=row.entry.amount,
                balance_after=row.entry.balance_after,
                created_at=row.entry.created_at,
                notes=row.transaction_notes,
            )
            for row in rows
        ]

        return LedgerResponse(
            client_id=client_id,
            total=total,
            skip=skip,
            limit=limit,
            entries=entries,
            balance=balance,
        )

    @staticmethod
    def _net_label(net: Decimal) -> str:
        if net > 0:
            return "CLIENT_OWES"
        if net < 0:
            return "COMPANY_OWES"
        return "SETTLED"

    def get_grouped_ledger(
        self,
        client_id: UUID,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> LedgerGroupedResponse:
        """
        Vista agrupada del libro mayor: una fila por transacción.

        egreso  = CREDIT en ledger (empresa dio al cliente).
        ingreso = DEBIT  en ledger (empresa recibió del cliente).
        net     = ingreso - egreso por divisa.

        El summary siempre refleja el rango completo (no la página actual).
        Solo transacciones ACTIVE.
        """
        total = self.repo.count_grouped(client_id, date_from=date_from, date_to=date_to)
        rows = self.repo.get_grouped(
            client_id, date_from=date_from, date_to=date_to, skip=skip, limit=limit
        )
        totals = self.repo.get_grouped_totals(client_id, date_from=date_from, date_to=date_to)

        net_mxn = totals.ingreso_mxn - totals.egreso_mxn
        net_gtq = totals.ingreso_gtq - totals.egreso_gtq

        summary = LedgerGroupedSummary(
            total_egreso_mxn=totals.egreso_mxn,
            total_ingreso_mxn=totals.ingreso_mxn,
            total_egreso_gtq=totals.egreso_gtq,
            total_ingreso_gtq=totals.ingreso_gtq,
            net_mxn=net_mxn,
            net_gtq=net_gtq,
            net_mxn_label=self._net_label(net_mxn),
            net_gtq_label=self._net_label(net_gtq),
        )

        grouped_rows = [
            LedgerGroupedRow(
                transaction_id=r.transaction_id,
                date=r.created_at,
                reference=r.code,
                operation=r.transaction_type,
                egreso_mxn=r.egreso_mxn,
                egreso_gtq=r.egreso_gtq,
                ingreso_mxn=r.ingreso_mxn,
                ingreso_gtq=r.ingreso_gtq,
                notes=r.notes,
                status=r.status,
            )
            for r in rows
        ]

        return LedgerGroupedResponse(
            client_id=client_id,
            total=total,
            skip=skip,
            limit=limit,
            summary=summary,
            rows=grouped_rows,
        )

    def build_entries_for_transaction(
        self,
        txn: Transaction,
    ) -> List[LedgerEntry]:
        """
        Construye las LedgerEntry para una transacción recién flusheada (sin commit).
        El balance_after se calcula desde el estado actual del DB (antes de este txn).
        """
        from app.models.transaction import TransactionType

        entries: List[LedgerEntry] = []
        client_id = txn.client_id

        def _make_entry(currency: Currency, direction: EntryDirection, amount: Decimal) -> LedgerEntry:
            prev = self.repo.get_balance(client_id, currency)
            if direction == EntryDirection.CREDIT:
                balance_after = prev + amount
            else:
                balance_after = prev - amount
            return LedgerEntry(
                transaction_id=txn.id,
                client_id=client_id,
                currency=currency,
                direction=direction,
                amount=amount,
                balance_after=balance_after,
            )

        t = txn.transaction_type

        if t == TransactionType.SELL_MXN:
            # Empresa vende MXN: cliente recibe MXN (+), entrega GTQ (-)
            entries.append(_make_entry(Currency.MXN, EntryDirection.CREDIT, txn.amount_mxn))
            entries.append(_make_entry(Currency.GTQ, EntryDirection.DEBIT, txn.amount_gtq))

        elif t == TransactionType.BUY_MXN:
            # Empresa compra MXN: cliente entrega MXN (-), recibe GTQ (+)
            entries.append(_make_entry(Currency.MXN, EntryDirection.DEBIT, txn.amount_mxn))
            entries.append(_make_entry(Currency.GTQ, EntryDirection.CREDIT, txn.amount_gtq))

        elif t == TransactionType.SELL_GTQ:
            # Empresa vende GTQ: cliente recibe GTQ (+), entrega MXN (-)
            entries.append(_make_entry(Currency.GTQ, EntryDirection.CREDIT, txn.amount_gtq))
            entries.append(_make_entry(Currency.MXN, EntryDirection.DEBIT, txn.amount_mxn))

        elif t == TransactionType.BUY_GTQ:
            # Empresa compra GTQ: cliente entrega GTQ (-), recibe MXN (+)
            entries.append(_make_entry(Currency.GTQ, EntryDirection.DEBIT, txn.amount_gtq))
            entries.append(_make_entry(Currency.MXN, EntryDirection.CREDIT, txn.amount_mxn))

        elif t == TransactionType.PAYMENT:
            # Abono: solo una divisa al cliente
            if txn.amount_mxn > 0:
                entries.append(_make_entry(Currency.MXN, EntryDirection.CREDIT, txn.amount_mxn))
            elif txn.amount_gtq > 0:
                entries.append(_make_entry(Currency.GTQ, EntryDirection.CREDIT, txn.amount_gtq))

        elif t == TransactionType.WITHDRAWAL:
            # Retiro: solo una divisa del cliente
            if txn.amount_mxn > 0:
                entries.append(_make_entry(Currency.MXN, EntryDirection.DEBIT, txn.amount_mxn))
            elif txn.amount_gtq > 0:
                entries.append(_make_entry(Currency.GTQ, EntryDirection.DEBIT, txn.amount_gtq))

        return entries
