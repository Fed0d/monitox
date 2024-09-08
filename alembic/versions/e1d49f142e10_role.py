"""Role

Revision ID: e1d49f142e10
Revises: a24626d0930e
Create Date: 2024-09-08 19:12:11.583957

"""

from typing import Sequence, Union

from sqlalchemy.dialects.postgresql import ENUM

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1d49f142e10"
down_revision: Union[str, None] = "a24626d0930e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the ENUM type for PostgreSQL
user_role_enum = ENUM("ROLE_ADMIN", "ROLE_USER", name="user_role", create_type=True)


def upgrade() -> None:
    # Create the ENUM type in the database if it doesn't exist
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Alter the column type using explicit cast
    op.execute(
        "ALTER TABLE role ALTER COLUMN role TYPE user_role USING role::user_role"
    )


def downgrade() -> None:
    # Revert the column type back to TEXT
    op.execute("ALTER TABLE role ALTER COLUMN role TYPE TEXT USING role::TEXT")

    # Drop the ENUM type in the database if it exists
    user_role_enum.drop(op.get_bind(), checkfirst=True)
