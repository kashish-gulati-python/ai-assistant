"""merge multiple heads

Revision ID: f832b5914cc3
Revises: 10509670dbc4, 1f43bf61fd62, 42b52655bda2
Create Date: 2026-09-23 22:26:05.997407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f832b5914cc3'
down_revision: Union[str, Sequence[str], None] = ('10509670dbc4', '1f43bf61fd62', '42b52655bda2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
