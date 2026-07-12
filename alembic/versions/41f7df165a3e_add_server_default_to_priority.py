"""add server default to priority

Revision ID: 41f7df165a3e
Revises: e0bc2c076a6d
Create Date: 2026-07-11 20:40:32.068125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41f7df165a3e'
down_revision: Union[str, Sequence[str], None] = 'e0bc2c076a6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column('tasks', 'priority', server_default='medium')

def downgrade() -> None:
    op.alter_column('tasks', 'priority', server_default=None)
