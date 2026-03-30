"""Initial schema — users, clients, cash_sessions, transactions, ledger_entries, audit_events

Revision ID: 0001
Revises:
Create Date: 2026-03-29

Target DB: MySQL 8.0+ via pymysql
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── users ────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin", "operator", "viewer", name="user_role"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("last_login_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── clients ──────────────────────────────────────────────────────────────
    op.create_table(
        "clients",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("phone", sa.String(30)),
        sa.Column("email", sa.String(255)),
        sa.Column("address", sa.Text()),
        sa.Column(
            "id_type",
            sa.Enum("passport", "national_id", "tax_id", "other", name="id_type"),
        ),
        sa.Column("id_number", sa.String(50)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("notes", sa.Text()),
        sa.Column(
            "created_by",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_clients_code", "clients", ["code"], unique=True)
    op.create_index("ix_clients_full_name", "clients", ["full_name"])

    # ── cash_sessions ────────────────────────────────────────────────────────
    # Estrategia de caja única:
    #   unique_open = 1  cuando status='open'
    #   unique_open = NULL cuando status='closed'
    #   MySQL ignora NULL en UNIQUE indexes → permite múltiples cajas cerradas
    #   Solo puede existir 1 fila con unique_open=1 → garantiza una sola caja abierta
    op.create_table(
        "cash_sessions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "status",
            sa.Enum("open", "closed", name="cash_status"),
            nullable=False,
            server_default="open",
        ),
        sa.Column("unique_open", sa.SmallInteger(), nullable=True),
        sa.Column("opening_amount_mxn", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("opening_amount_gtq", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("closing_amount_mxn", sa.Numeric(15, 2)),
        sa.Column("closing_amount_gtq", sa.Numeric(15, 2)),
        sa.Column("difference_mxn", sa.Numeric(15, 2)),
        sa.Column("difference_gtq", sa.Numeric(15, 2)),
        sa.Column(
            "opened_by",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("closed_by", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("opened_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime()),
        sa.Column("notes", sa.Text()),
        sa.CheckConstraint("opening_amount_mxn >= 0", name="ck_cash_opening_mxn_positive"),
        sa.CheckConstraint("opening_amount_gtq >= 0", name="ck_cash_opening_gtq_positive"),
    )
    op.create_index("uq_one_open_cash_session", "cash_sessions", ["unique_open"], unique=True)

    # ── transactions ─────────────────────────────────────────────────────────
    op.create_table(
        "transactions",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column(
            "client_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("clients.id"),
            nullable=False,
        ),
        sa.Column(
            "cash_session_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("cash_sessions.id"),
            nullable=False,
        ),
        sa.Column(
            "transaction_type",
            sa.Enum("SELL_MXN", "BUY_MXN", "PAYMENT", "WITHDRAWAL", name="transaction_type"),
            nullable=False,
        ),
        sa.Column("amount_mxn", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("amount_gtq", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("commission", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("exchange_rate", sa.Numeric(10, 6)),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "VOIDED", name="transaction_status"),
            nullable=False,
            server_default="ACTIVE",
        ),
        sa.Column("voided_by", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("voided_at", sa.DateTime()),
        sa.Column("void_reason", sa.Text()),
        sa.Column("void_of_id", sa.Uuid(as_uuid=True), sa.ForeignKey("transactions.id")),
        sa.Column(
            "created_by",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("notes", sa.Text()),
        sa.CheckConstraint("amount_mxn >= 0", name="ck_txn_amount_mxn_positive"),
        sa.CheckConstraint("amount_gtq >= 0", name="ck_txn_amount_gtq_positive"),
        sa.CheckConstraint("amount_mxn > 0 OR amount_gtq > 0", name="ck_txn_at_least_one_amount"),
        sa.CheckConstraint("commission >= 0", name="ck_txn_commission_positive"),
    )
    op.create_index("ix_transactions_code", "transactions", ["code"], unique=True)
    op.create_index("ix_transactions_client_status", "transactions", ["client_id", "status"])

    # ── ledger_entries ───────────────────────────────────────────────────────
    op.create_table(
        "ledger_entries",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "transaction_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("transactions.id"),
            nullable=False,
        ),
        sa.Column(
            "client_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("clients.id"),
            nullable=False,
        ),
        sa.Column("currency", sa.Enum("MXN", "GTQ", name="currency"), nullable=False),
        sa.Column(
            "direction",
            sa.Enum("DEBIT", "CREDIT", name="entry_direction"),
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(15, 2), nullable=False),
        sa.Column("balance_after", sa.Numeric(15, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("amount > 0", name="ck_ledger_amount_positive"),
    )
    op.create_index("ix_ledger_transaction", "ledger_entries", ["transaction_id"])
    op.create_index("ix_ledger_client_currency", "ledger_entries", ["client_id", "currency"])
    op.create_index(
        "ix_ledger_client_currency_created",
        "ledger_entries",
        ["client_id", "currency", "created_at"],
    )

    # ── audit_events ─────────────────────────────────────────────────────────
    op.create_table(
        "audit_events",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
        ),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("resource_id", sa.Uuid(as_uuid=True)),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("payload", sa.JSON()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_audit_user", "audit_events", ["user_id"])
    op.create_index("ix_audit_resource", "audit_events", ["resource_type", "resource_id"])
    op.create_index("ix_audit_created_at", "audit_events", ["created_at"])


def downgrade() -> None:
    # Solo para entorno de desarrollo — no ejecutar en producción.
    op.drop_table("audit_events")
    op.drop_table("ledger_entries")
    op.drop_table("transactions")
    op.drop_table("cash_sessions")
    op.drop_table("clients")
    op.drop_table("users")
