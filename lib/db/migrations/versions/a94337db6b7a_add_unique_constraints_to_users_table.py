"""Add unique constraints to users table

Revision ID: a94337db6b7a
Revises: ca4810b6f5d1
Create Date: 2023-05-17 12:45:41.054497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a94337db6b7a"
down_revision = "ca4810b6f5d1"
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add unique constraints
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_unique_constraint("uq_username", ["username"])
        batch_op.create_unique_constraint("uq_email", ["email"])


def downgrade():
    # Remove unique constraints
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_username", type_="unique")
        batch_op.drop_constraint("uq_email", type_="unique")
