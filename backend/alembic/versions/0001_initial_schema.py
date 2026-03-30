"""Initial schema — users, clients, cash_sessions, transactions, ledger_entries, audit_events

Revision ID: 0001
Revises:
Create Date: 2026-03-29

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Enums ────────────────────────────────────────────────────────────────
    op.execute("CREATE TYPE user_role AS ENUM ('admin', 'operator', 'viewer')")
    op.execute("CREATE TYPE id_type AS ENUM ('passport', 'national_id', 'tax_id', 'other')")
    op.execute("CREATE TYPE cash_status AS ENUM ('open', 'closed')")
    op.execute("CREATE TYPE transaction_type AS ENUM ('SELL_MXN', 'BUY_MXN', 'PAYMENT', 'WITHDRAWAL')")
    op.execute("CREATE TYPE transaction_status AS ENUM ('ACTIVE', 'VOIDED')")
    op.execute("CREATE TYPE currency AS ENUM ('MXN', 'GTQ')")
    op.execute("CREATE TYPE entry_direction AS ENUM ('DEBIT', 'CREDIT')")

    # ── users ────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin", "operator", "viewer", name="user_role", create_type=False),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── clients ──────────────────────────────────────────────────────────────
    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("phone", sa.String(30)),
        sa.Column("email", sa.String(255)),
        sa.Column("address", sa.Text()),
        sa.Column("id_type", sa.Enum("passport", "national_id", "tax_id", "other", name="id_type", create_type=False)),
        sa.Column("id_number", sa.String(50)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_clients_code", "clients", ["code"], unique=True)
    op.create_index("ix_clients_full_name", "clients", ["full_name"])

    # ── cash_sessions ────────────────────────────────────────────────────────
    op.create_table(
        "cash_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "status",
            sa.Enum("open", "closed", name="cash_status", create_type=False),
            nullable=False,
            server_default="open",
        ),
        sa.Column("opening_amount_mxn", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("opening_amount_gtq", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("closing_amount_mxn", sa.Numeric(15, 2)),
        sa.Column("closing_amount_gtq", sa.Numeric(15, 2)),
        sa.Column("difference_mxn", sa.Numeric(15, 2)),
        sa.Column("difference_gtq", sa.Numeric(15, 2)),
        sa.Column("opened_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("closed_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime(timezone=True)),
        sa.Column("notes", sa.Text()),
        sa.CheckConstraint("opening_amount_mxn >= 0", name="ck_cash_opening_mxn_positive"),
        sa.CheckConstraint("opening_amount_gtq >= 0", name="ck_cash_opening_gtq_positive"),
    )
    # Partial unique index: solo una caja abierta a la vez (PostgreSQL)
    op.execute(
        "CREATE UNIQUE INDEX uq_one_open_cash_session "
        "ON cash_sessions (status) WHERE status = 'open'"
    )

    # ── transactions ─────────────────────────────────────────────────────────
    op.create_table(
        "transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("cash_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cash_sessions.id"), nullable=False),
        sa.Column(
            "transaction_type",
            sa.Enum("SELL_MXN", "BUY_MXN", "PAYMENT", "WITHDRAWAL", name="transaction_type", create_type=False),
            nullable=False,
        ),
        sa.Column("amount_mxn", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("amount_gtq", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("commission", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("exchange_rate", sa.Numeric(10, 6)),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "VOIDED", name="transaction_status", create_type=False),
            nullable=False,
            server_default="ACTIVE",
        ),
        sa.Column("voided_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("voided_at", sa.DateTime(timezone=True)),
        sa.Column("void_reason", sa.Text()),
        sa.Column("void_of_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transactions.id")),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
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
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("transaction_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transactions.id"), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("currency", sa.Enum("MXN", "GTQ", name="currency", create_type=False), nullable=False),
        sa.Column(
            "direction",
            sa.Enum("DEBIT", "CREDIT", name="entry_direction", create_type=False),
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(15, 2), nullable=False),
        sa.Column("balance_after", sa.Numeric(15, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
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
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True)),
        sa.Column("ip_address", postgresql.INET()),
        sa.Column("payload", postgresql.JSONB()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_audit_user", "audit_events", ["user_id"])
    op.create_index("ix_audit_resource", "audit_events", ["resource_type", "resource_id"])
    op.create_index("ix_audit_created_at", "audit_events", ["created_at"])


def downgrade() -> None:
    # Tablas financieras: en producción el downgrade está deshabilitado.
    # Solo se ejecuta en entorno de desarrollo para resetear el esquema.
    op.drop_table("audit_events")
    op.drop_table("ledger_entries")
    op.drop_table("transactions")
    op.drop_index("uq_one_open_cash_session", table_name="cash_sessions")
    op.drop_table("cash_sessions")
    op.drop_table("clients")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS entry_direction")
    op.execute("DROP TYPE IF EXISTS currency")
    op.execute("DROP TYPE IF EXISTS transaction_status")
    op.execute("DROP TYPE IF EXISTS transaction_type")
    op.execute("DROP TYPE IF EXISTS cash_status")
    op.execute("DROP TYPE IF EXISTS id_type")
    op.execute("DROP TYPE IF EXISTS user_role")
