"""create account table

Revision ID: a58a6db4855e
Revises: 
Create Date: 2021-01-05 15:59:58.154061

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "a58a6db4855e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "account",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("start_cash", sa.Integer(), nullable=True),
        sa.Column("total_purchase", sa.Float(), nullable=True),
        sa.Column("cash", sa.Integer(), nullable=True),
        sa.Column("stock_count", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "order",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("account_id", postgresql.UUID(), nullable=True),
        sa.Column("code", sa.String(length=6), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("side", sa.String(), nullable=True),
        sa.Column("unfilled", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("order")
    op.drop_table("account")
