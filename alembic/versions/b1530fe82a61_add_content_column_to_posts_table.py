"""add content column to posts table

Revision ID: b1530fe82a61
Revises: 6666ead3160a
Create Date: 2022-08-03 09:55:50.558160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1530fe82a61'
down_revision = '6666ead3160a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts", # table name 
        sa.Column( # column
            "content", # column name
            sa.String(), # column data type
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column("posts", "user_id")
