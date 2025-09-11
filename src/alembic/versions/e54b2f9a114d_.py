"""empty message

Revision ID: e54b2f9a114d
Revises: 5010d816a4a7
Create Date: 2025-09-11 12:10:39.295476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e54b2f9a114d'
down_revision: Union[str, Sequence[str], None] = '5010d816a4a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "fk_transactions_users",
            "users",
            ["user_id"],
            ["id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_constraint("fk_transactions_users", type_="foreignkey")
        batch_op.drop_column("user_id")
