"""Add SELL_GTQ and BUY_GTQ to transaction_type enum

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-20

MySQL does not have a standalone ENUM type; values are embedded in the column definition.
To add enum values we MODIFY COLUMN with the full new set of allowed values.

IMPORTANT: downgrade() will FAIL if any row contains SELL_GTQ or BUY_GTQ values.
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Full ordered list — do NOT remove existing values.
_NEW_ENUM = "ENUM('SELL_MXN', 'BUY_MXN', 'SELL_GTQ', 'BUY_GTQ', 'PAYMENT', 'WITHDRAWAL')"
_OLD_ENUM = "ENUM('SELL_MXN', 'BUY_MXN', 'PAYMENT', 'WITHDRAWAL')"


def upgrade() -> None:
    op.execute(
        f"ALTER TABLE transactions MODIFY COLUMN transaction_type {_NEW_ENUM} NOT NULL"
    )


def downgrade() -> None:
    # Will error if any SELL_GTQ / BUY_GTQ rows exist — intentional.
    op.execute(
        f"ALTER TABLE transactions MODIFY COLUMN transaction_type {_OLD_ENUM} NOT NULL"
    )
