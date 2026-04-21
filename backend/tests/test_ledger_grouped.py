"""
Unit tests for LedgerService.get_grouped_ledger — net position logic.
No DB required: repo is fully mocked.
Run: pytest backend/tests/test_ledger_grouped.py -v
"""
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.models.transaction import TransactionType
from app.repositories.ledger_repo import GroupedLedgerRow
from app.services.ledger_service import LedgerService


# ── helpers ──────────────────────────────────────────────────────────────────

def _make_totals(egreso_mxn, egreso_gtq, ingreso_mxn, ingreso_gtq) -> GroupedLedgerRow:
    return GroupedLedgerRow(
        transaction_id=None,  # type: ignore[arg-type]
        code="",
        transaction_type=None,  # type: ignore[arg-type]
        created_at=None,  # type: ignore[arg-type]
        notes=None,
        status="",
        egreso_mxn=Decimal(str(egreso_mxn)),
        egreso_gtq=Decimal(str(egreso_gtq)),
        ingreso_mxn=Decimal(str(ingreso_mxn)),
        ingreso_gtq=Decimal(str(ingreso_gtq)),
    )


def _service_with_mock_repo(totals: GroupedLedgerRow, rows=None) -> LedgerService:
    svc = LedgerService.__new__(LedgerService)
    repo = MagicMock()
    repo.count_grouped.return_value = len(rows) if rows else 0
    repo.get_grouped.return_value = rows or []
    repo.get_grouped_totals.return_value = totals
    repo.get_balance.return_value = Decimal("0")
    svc.repo = repo
    return svc


# ── net_mxn = ingreso_mxn - egreso_mxn ───────────────────────────────────────

def test_net_mxn_is_ingreso_minus_egreso():
    totals = _make_totals(egreso_mxn="500", egreso_gtq="0", ingreso_mxn="200", ingreso_gtq="0")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    assert result.summary.net_mxn == Decimal("200") - Decimal("500")
    assert result.summary.net_mxn == Decimal("-300")


def test_net_gtq_is_ingreso_minus_egreso():
    totals = _make_totals(egreso_mxn="0", egreso_gtq="800", ingreso_mxn="0", ingreso_gtq="1000")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    assert result.summary.net_gtq == Decimal("1000") - Decimal("800")
    assert result.summary.net_gtq == Decimal("200")


def test_totals_preserved_in_summary():
    totals = _make_totals(egreso_mxn="1500", egreso_gtq="800", ingreso_mxn="200", ingreso_gtq="600")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    s = result.summary
    assert s.total_egreso_mxn == Decimal("1500")
    assert s.total_ingreso_mxn == Decimal("200")
    assert s.total_egreso_gtq == Decimal("800")
    assert s.total_ingreso_gtq == Decimal("600")


# ── labels ────────────────────────────────────────────────────────────────────

def test_label_client_owes_when_net_positive():
    # ingreso > egreso → empresa recibió más → cliente debe
    totals = _make_totals(egreso_mxn="100", egreso_gtq="0", ingreso_mxn="500", ingreso_gtq="0")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    assert result.summary.net_mxn > 0
    assert result.summary.net_mxn_label == "CLIENT_OWES"


def test_label_company_owes_when_net_negative():
    # egreso > ingreso → empresa dio más → le debemos al cliente
    totals = _make_totals(egreso_mxn="500", egreso_gtq="0", ingreso_mxn="100", ingreso_gtq="0")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    assert result.summary.net_mxn < 0
    assert result.summary.net_mxn_label == "COMPANY_OWES"


def test_label_settled_when_net_zero():
    totals = _make_totals(egreso_mxn="300", egreso_gtq="0", ingreso_mxn="300", ingreso_gtq="0")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    assert result.summary.net_mxn == Decimal("0")
    assert result.summary.net_mxn_label == "SETTLED"


def test_gtq_label_independent_of_mxn():
    totals = _make_totals(egreso_mxn="100", egreso_gtq="200", ingreso_mxn="500", ingreso_gtq="50")
    svc = _service_with_mock_repo(totals)
    result = svc.get_grouped_ledger(uuid4())
    assert result.summary.net_mxn_label == "CLIENT_OWES"   # 500-100=400 > 0
    assert result.summary.net_gtq_label == "COMPANY_OWES"  # 50-200=-150 < 0


# ── rows passthrough ──────────────────────────────────────────────────────────

def test_rows_are_passed_through():
    from datetime import datetime
    totals = _make_totals("0", "0", "0", "0")
    txn_id = uuid4()
    mock_row = GroupedLedgerRow(
        transaction_id=txn_id,
        code="TXN-20260421-00001",
        transaction_type=TransactionType.SELL_MXN,
        created_at=datetime(2026, 4, 21, 10, 0, 0),
        notes=None,
        status="ACTIVE",
        egreso_mxn=Decimal("500"),
        egreso_gtq=Decimal("0"),
        ingreso_mxn=Decimal("0"),
        ingreso_gtq=Decimal("750"),
    )
    svc = _service_with_mock_repo(totals, rows=[mock_row])
    result = svc.get_grouped_ledger(uuid4())
    assert len(result.rows) == 1
    assert result.rows[0].reference == "TXN-20260421-00001"
    assert result.rows[0].egreso_mxn == Decimal("500")
    assert result.rows[0].ingreso_gtq == Decimal("750")
