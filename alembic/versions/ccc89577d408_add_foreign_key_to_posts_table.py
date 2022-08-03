"""add foreign key to posts table

Revision ID: ccc89577d408
Revises: 9d625c419588
Create Date: 2022-08-03 10:16:52.020553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccc89577d408'
down_revision = '9d625c419588'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )
    # can also use
    # op.create_foreign_key("post_users_id_fkey", source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("post_users_id_fkey", table_name="posts")
    op.drop_column("posts", "user_id")
