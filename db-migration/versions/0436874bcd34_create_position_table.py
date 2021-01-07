"""create position table

Revision ID: 0436874bcd34
Revises: a58a6db4855e
Create Date: 2021-01-07 09:48:50.729439

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0436874bcd34"
down_revision = "a58a6db4855e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "position",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("account_id", postgresql.UUID(), nullable=True),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("closed", sa.Boolean(), nullable=True),
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
        sa.UniqueConstraint("id", "code"),
    )


def downgrade():
    op.drop_table("position")
