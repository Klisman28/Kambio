"""
Unit tests for TransactionCreate schema validation.
No DB required — pure Pydantic validation.
Run: pytest backend/tests/test_transaction_schemas.py -v
"""
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate

_CLIENT_ID = "00000000-0000-0000-0000-000000000001"

# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #

def _make(t: TransactionType, mxn="100", gtq="750", rate="7.5", **kwargs):
    return TransactionCreate(
        client_id=_CLIENT_ID,
        transaction_type=t,
        amount_mxn=Decimal(mxn),
        amount_gtq=Decimal(gtq),
        exchange_rate=Decimal(rate),
        **kwargs,
    )


def _make_single(t: TransactionType, mxn="0", gtq="0"):
    """For PAYMENT / WITHDRAWAL — only one currency."""
    return TransactionCreate(
        client_id=_CLIENT_ID,
        transaction_type=t,
        amount_mxn=Decimal(mxn),
        amount_gtq=Decimal(gtq),
    )


# --------------------------------------------------------------------------- #
# FX types (SELL_MXN, BUY_MXN, SELL_GTQ, BUY_GTQ)                            #
# --------------------------------------------------------------------------- #

FX_TYPES = [
    TransactionType.SELL_MXN,
    TransactionType.BUY_MXN,
    TransactionType.SELL_GTQ,
    TransactionType.BUY_GTQ,
]


@pytest.mark.parametrize("t", FX_TYPES)
def test_fx_type_valid(t):
    obj = _make(t)
    assert obj.transaction_type == t
    assert obj.amount_mxn > 0
    assert obj.amount_gtq > 0
    assert obj.exchange_rate > 0


@pytest.mark.parametrize("t", FX_TYPES)
def test_fx_type_missing_mxn(t):
    with pytest.raises(ValidationError, match="amount_mxn > 0"):
        _make(t, mxn="0")


@pytest.mark.parametrize("t", FX_TYPES)
def test_fx_type_missing_gtq(t):
    with pytest.raises(ValidationError, match="amount_gtq > 0"):
        _make(t, gtq="0")


@pytest.mark.parametrize("t", FX_TYPES)
def test_fx_type_missing_exchange_rate(t):
    with pytest.raises(ValidationError, match="exchange_rate"):
        TransactionCreate(
            client_id=_CLIENT_ID,
            transaction_type=t,
            amount_mxn=Decimal("100"),
            amount_gtq=Decimal("750"),
            exchange_rate=None,
        )


# --------------------------------------------------------------------------- #
# PAYMENT                                                                      #
# --------------------------------------------------------------------------- #

def test_payment_mxn_valid():
    obj = _make_single(TransactionType.PAYMENT, mxn="500")
    assert obj.amount_mxn == Decimal("500")
    assert obj.amount_gtq == Decimal("0")


def test_payment_gtq_valid():
    obj = _make_single(TransactionType.PAYMENT, gtq="3750")
    assert obj.amount_gtq == Decimal("3750")
    assert obj.amount_mxn == Decimal("0")


def test_payment_both_currencies_invalid():
    with pytest.raises(ValidationError, match="exactamente una divisa"):
        _make_single(TransactionType.PAYMENT, mxn="100", gtq="750")


def test_payment_no_currency_invalid():
    with pytest.raises(ValidationError, match="exactamente una divisa"):
        _make_single(TransactionType.PAYMENT, mxn="0", gtq="0")


# --------------------------------------------------------------------------- #
# WITHDRAWAL                                                                   #
# --------------------------------------------------------------------------- #

def test_withdrawal_mxn_valid():
    obj = _make_single(TransactionType.WITHDRAWAL, mxn="200")
    assert obj.amount_mxn == Decimal("200")


def test_withdrawal_both_currencies_invalid():
    with pytest.raises(ValidationError, match="exactamente una divisa"):
        _make_single(TransactionType.WITHDRAWAL, mxn="100", gtq="750")


# --------------------------------------------------------------------------- #
# Negative amounts                                                             #
# --------------------------------------------------------------------------- #

def test_negative_mxn_rejected():
    with pytest.raises(ValidationError, match="negativos"):
        TransactionCreate(
            client_id=_CLIENT_ID,
            transaction_type=TransactionType.SELL_MXN,
            amount_mxn=Decimal("-1"),
            amount_gtq=Decimal("750"),
            exchange_rate=Decimal("7.5"),
        )


def test_negative_commission_rejected():
    with pytest.raises(ValidationError, match="negativos"):
        TransactionCreate(
            client_id=_CLIENT_ID,
            transaction_type=TransactionType.SELL_MXN,
            amount_mxn=Decimal("100"),
            amount_gtq=Decimal("750"),
            exchange_rate=Decimal("7.5"),
            commission=Decimal("-5"),
        )
