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


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("user_id", sa.NotNullable(sa.Integer)),
        sa.Column("github_access_token", sa.NotNullable(sa.String)),
        sa.Column("master_password", sa.NotNullable(sa.String)),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
