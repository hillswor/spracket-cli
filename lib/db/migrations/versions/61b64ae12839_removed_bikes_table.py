"""Removed bikes table

Revision ID: 61b64ae12839
Revises: a94337db6b7a
Create Date: 2023-05-17 15:14:24.949363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61b64ae12839'
down_revision = 'a94337db6b7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bikes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('manufacturer', sa.VARCHAR(), nullable=True),
    sa.Column('model', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('brand', sa.VARCHAR(), nullable=True),
    sa.Column('serial_number', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###