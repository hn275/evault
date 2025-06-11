"""empty message

Revision ID: dbba5d52c8d9
Revises:
Create Date: 2025-06-07 00:14:39.334329

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dbba5d52c8d9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "repositories"


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        table_name,
        sa.Column(
            "id",
            sa.NotNullable(sa.Integer),
            primary_key=True,
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "owner_id",
            sa.NotNullable(sa.Integer),
            nullable=False,
        ),
        sa.Column(
            "password",
            sa.NotNullable(sa.String),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(table_name)
