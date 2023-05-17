"""Remove all tables

Revision ID: e67d43cb4d1f
Revises: a75bc4055cc3
Create Date: 2023-05-17 15:57:31.454727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e67d43cb4d1f'
down_revision = 'a75bc4055cc3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bikes')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', name='uq_email'),
    sa.UniqueConstraint('username', name='uq_username')
    )
    op.create_table('bikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('brand', sa.VARCHAR(), nullable=True),
    sa.Column('model', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('serial_number', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('serial_number', name='uq_serial_number')
    )
    # ### end Alembic commands ###