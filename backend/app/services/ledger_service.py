from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ledger_entry import Currency, EntryDirection, LedgerEntry
from app.models.transaction import Transaction
from app.repositories.ledger_repo import LedgerRepository
from app.schemas.ledger import BalanceOut, LedgerResponse


class LedgerService:
    def __init__(self, db: Session):
        self.repo = LedgerRepository(db)

    def get_balance(self, client_id: UUID) -> BalanceOut:
        mxn = self.repo.get_balance(client_id, Currency.MXN)
        gtq = self.repo.get_balance(client_id, Currency.GTQ)
        return BalanceOut(client_id=client_id, mxn=mxn, gtq=gtq)

    def get_ledger(
        self,
        client_id: UUID,
        currency: Optional[Currency] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> LedgerResponse:
        entries = self.repo.get_entries(client_id, currency=currency, skip=skip, limit=limit)
        balance = self.get_balance(client_id)
        return LedgerResponse(client_id=client_id, entries=entries, balance=balance)

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
