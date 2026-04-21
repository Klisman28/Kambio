"""add current_amount columns to cash_sessions

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-21
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cash_sessions",
        sa.Column("current_amount_mxn", sa.Numeric(15, 2), nullable=False, server_default="0.00"),
    )
    op.add_column(
        "cash_sessions",
        sa.Column("current_amount_gtq", sa.Numeric(15, 2), nullable=False, server_default="0.00"),
    )
    # Inicializar las sesiones existentes: current = opening
    op.execute(
        "UPDATE cash_sessions SET current_amount_mxn = opening_amount_mxn, current_amount_gtq = opening_amount_gtq"
    )


def downgrade() -> None:
    op.drop_column("cash_sessions", "current_amount_gtq")
    op.drop_column("cash_sessions", "current_amount_mxn")
