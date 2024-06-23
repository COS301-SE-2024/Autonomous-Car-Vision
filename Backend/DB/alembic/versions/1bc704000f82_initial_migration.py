"""Initial migration

Revision ID: 1bc704000f82
Revises: 9b5efbd449ba
Create Date: 2024-06-03 03:04:14.457504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc704000f82'
down_revision: Union[str, None] = '9b5efbd449ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('media_id', sa.String(), nullable=False),
    sa.Column('media_name', sa.String(), nullable=False),
    sa.Column('media_url', sa.String(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('media_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media')
    # ### end Alembic commands ###