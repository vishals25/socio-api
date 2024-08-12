"""createtables01

Revision ID: fbc27d3ecba1
Revises: 
Create Date: 2024-08-12 18:52:06.539229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbc27d3ecba1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String(50), nullable=False)
        ,sa.Column('email', sa.String(100), nullable=False, unique=True)
        # ,sa.Column('password', sa.String(100), nullable=False),
        # sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        # sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(),
                #   ,onupdate=sa.func.now())
                  )
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
