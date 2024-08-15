"""Drop email column from posts table

Revision ID: 84da2c43c1f8
Revises: d89452d01fdb
Create Date: 2024-08-15 07:55:58.307630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84da2c43c1f8'
down_revision: Union[str, None] = 'd89452d01fdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the 'email' column from the 'posts' table
    op.drop_column('posts', 'email')

def downgrade():
    # Add the 'email' column back to the 'posts' table (if needed for rollback)
    op.add_column('posts', sa.Column('email', sa.String(100), nullable=False, unique=True))
