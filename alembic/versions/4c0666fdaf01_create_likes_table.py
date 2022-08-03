"""create likes table

Revision ID: 4c0666fdaf01
Revises: b3782487d6cf
Create Date: 2022-08-03 10:34:18.168242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c0666fdaf01'
down_revision = 'b3782487d6cf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "likes",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True,nullable=False),
        sa.Column("upvote", sa.Boolean(), server_default="TRUE", nullable=False)
    )

def downgrade() -> None:
    op.drop_table("likes")
