"""tambah indeks kolom produk pada orders

Revision ID: b4df76f43abc
Revises: bd20817c113c
Create Date: 2026-10-21 13:31:44.757397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4df76f43abc'
down_revision: Union[str, Sequence[str], None] = 'bd20817c113c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        'ix_orders_produk',
        'orders',
        ['produk']
    )

def downgrade():
    op.drop_index('ix_orders_produk', table_name='orders')