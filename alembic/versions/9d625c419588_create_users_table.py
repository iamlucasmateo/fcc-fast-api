"""create users table

Revision ID: 9d625c419588
Revises: b1530fe82a61
Create Date: 2022-08-03 10:08:54.720631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d625c419588'
down_revision = 'b1530fe82a61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False),
            server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"), # declare constraint here instead of in the column
        sa.UniqueConstraint("email")
    )


def downgrade() -> None:
    op.drop_table("users")
