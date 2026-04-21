"""
Unit tests for LedgerService.build_entries_for_transaction.
Uses a mock repository — no DB required.
Run: pytest backend/tests/test_ledger_service.py -v
"""
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.models.ledger_entry import Currency, EntryDirection
from app.models.transaction import TransactionType
from app.services.ledger_service import LedgerService


def _make_txn(t: TransactionType, mxn="100", gtq="750"):
    return SimpleNamespace(
        id=uuid4(),
        client_id=uuid4(),
        transaction_type=t,
        amount_mxn=Decimal(mxn),
        amount_gtq=Decimal(gtq),
    )


def _service_with_zero_balance() -> LedgerService:
    """Returns a LedgerService whose repo always reports 0 balance."""
    svc = LedgerService.__new__(LedgerService)
    repo = MagicMock()
    repo.get_balance.return_value = Decimal("0")
    svc.repo = repo
    return svc


# ------------------------------------------------------------------ helpers --

def _entries_map(entries):
    """Returns dict keyed by (currency, direction)."""
    return {(e.currency, e.direction): e for e in entries}


# ------------------------------------------------------------------ SELL_MXN -

def test_sell_mxn_produces_credit_mxn_debit_gtq():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.SELL_MXN, mxn="100", gtq="750")
    entries = svc.build_entries_for_transaction(txn)
    assert len(entries) == 2
    m = _entries_map(entries)
    assert m[(Currency.MXN, EntryDirection.CREDIT)].amount == Decimal("100")
    assert m[(Currency.GTQ, EntryDirection.DEBIT)].amount == Decimal("750")


# ------------------------------------------------------------------ BUY_MXN --

def test_buy_mxn_produces_debit_mxn_credit_gtq():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.BUY_MXN, mxn="100", gtq="750")
    entries = svc.build_entries_for_transaction(txn)
    m = _entries_map(entries)
    assert m[(Currency.MXN, EntryDirection.DEBIT)].amount == Decimal("100")
    assert m[(Currency.GTQ, EntryDirection.CREDIT)].amount == Decimal("750")


# ------------------------------------------------------------------ SELL_GTQ -

def test_sell_gtq_produces_credit_gtq_debit_mxn():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.SELL_GTQ, mxn="100", gtq="750")
    entries = svc.build_entries_for_transaction(txn)
    m = _entries_map(entries)
    assert m[(Currency.GTQ, EntryDirection.CREDIT)].amount == Decimal("750")
    assert m[(Currency.MXN, EntryDirection.DEBIT)].amount == Decimal("100")


# ------------------------------------------------------------------ BUY_GTQ --

def test_buy_gtq_produces_debit_gtq_credit_mxn():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.BUY_GTQ, mxn="100", gtq="750")
    entries = svc.build_entries_for_transaction(txn)
    m = _entries_map(entries)
    assert m[(Currency.GTQ, EntryDirection.DEBIT)].amount == Decimal("750")
    assert m[(Currency.MXN, EntryDirection.CREDIT)].amount == Decimal("100")


# ------------------------------------------------------------------ PAYMENT --

def test_payment_mxn_produces_single_credit_mxn():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.PAYMENT, mxn="500", gtq="0")
    entries = svc.build_entries_for_transaction(txn)
    assert len(entries) == 1
    assert entries[0].currency == Currency.MXN
    assert entries[0].direction == EntryDirection.CREDIT
    assert entries[0].amount == Decimal("500")


def test_payment_gtq_produces_single_credit_gtq():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.PAYMENT, mxn="0", gtq="3750")
    entries = svc.build_entries_for_transaction(txn)
    assert len(entries) == 1
    assert entries[0].currency == Currency.GTQ
    assert entries[0].direction == EntryDirection.CREDIT


# --------------------------------------------------------------- WITHDRAWAL --

def test_withdrawal_mxn_produces_single_debit_mxn():
    svc = _service_with_zero_balance()
    txn = _make_txn(TransactionType.WITHDRAWAL, mxn="200", gtq="0")
    entries = svc.build_entries_for_transaction(txn)
    assert len(entries) == 1
    assert entries[0].currency == Currency.MXN
    assert entries[0].direction == EntryDirection.DEBIT


# --------------------------------------------------------- balance_after -----

def test_balance_after_reflects_prior_balance():
    svc = _service_with_zero_balance()
    svc.repo.get_balance.side_effect = lambda cid, currency: (
        Decimal("1000") if currency == Currency.MXN else Decimal("7500")
    )
    txn = _make_txn(TransactionType.SELL_MXN, mxn="100", gtq="750")
    entries = svc.build_entries_for_transaction(txn)
    m = _entries_map(entries)
    # MXN credit: 1000 + 100 = 1100
    assert m[(Currency.MXN, EntryDirection.CREDIT)].balance_after == Decimal("1100")
    # GTQ debit: 7500 - 750 = 6750
    assert m[(Currency.GTQ, EntryDirection.DEBIT)].balance_after == Decimal("6750")
