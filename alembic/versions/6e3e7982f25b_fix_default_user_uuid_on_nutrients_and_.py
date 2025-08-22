"""fix default user uuid on nutrients and food

Revision ID: 6e3e7982f25b
Revises: 757845ad060b
Create Date: 2025-08-22 12:18:31.945586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e3e7982f25b'
down_revision: Union[str, Sequence[str], None] = '757845ad060b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # nutrients.created_by
    op.alter_column(
        "nutrients",
        "created_by",
        server_default="00000000-0000-0000-0000-000000000000"
    )
    op.drop_constraint("nutrients_created_by_fkey", "nutrients", type_="foreignkey")
    op.create_foreign_key(
        None, "nutrients", "users", ["created_by"], ["id"], ondelete="SET DEFAULT"
    )

    # food.created_by
    op.alter_column(
        "food",
        "created_by",
        server_default="00000000-0000-0000-0000-000000000000"
    )
    op.drop_constraint("food_created_by_fkey", "food", type_="foreignkey")
    op.create_foreign_key(
        None, "food", "users", ["created_by"], ["id"], ondelete="SET DEFAULT"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # nutrients
    op.drop_constraint(None, "nutrients", type_="foreignkey")
    op.create_foreign_key(
        "nutrients_created_by_fkey", "nutrients", "users", ["created_by"], ["id"]
    )

    # food
    op.drop_constraint(None, "food", type_="foreignkey")
    op.create_foreign_key(
        "food_created_by_fkey", "food", "users", ["created_by"], ["id"]
    )

