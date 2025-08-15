"""Add category enums to Badge and Question

Revision ID: e413ab04bbad
Revises: 9aa32792d616
Create Date: 2025-08-14 22:46:16.562274
"""
from alembic import op
import sqlalchemy as sa
from app.categories import CategoryKey

# revision identifiers, used by Alembic.
revision = 'e413ab04bbad'
down_revision = '9aa32792d616'
branch_labels = None
depends_on = None


def _col_exists(table: str, column: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    return any(col["name"] == column for col in insp.get_columns(table))


def upgrade():
    # badge.category (nullable) + threshold (nullable)
    if not _col_exists("badge", "category"):
        with op.batch_alter_table("badge", schema=None) as batch_op:
            batch_op.add_column(sa.Column(
                "category",
                sa.Enum(
                    CategoryKey,
                    native_enum=False,
                    values_callable=lambda x: [e.value for e in x],
                ),
                nullable=True,
            ))
    if not _col_exists("badge", "threshold"):
        with op.batch_alter_table("badge", schema=None) as batch_op:
            batch_op.add_column(sa.Column("threshold", sa.Integer(), nullable=True))

    # questions.category (NOT NULL)
    if not _col_exists("questions", "category"):
        with op.batch_alter_table("questions", schema=None) as batch_op:
            batch_op.add_column(sa.Column(
                "category",
                sa.Enum(
                    CategoryKey,
                    native_enum=False,
                    values_callable=lambda x: [e.value for e in x],
                ),
                nullable=False,
            ))


def downgrade():
    # Drop only if they exist (safe rollback)
    if _col_exists("questions", "category"):
        with op.batch_alter_table("questions", schema=None) as batch_op:
            batch_op.drop_column("category")

    if _col_exists("badge", "threshold"):
        with op.batch_alter_table("badge", schema=None) as batch_op:
            batch_op.drop_column("threshold")

    if _col_exists("badge", "category"):
        with op.batch_alter_table("badge", schema=None) as batch_op:
            batch_op.drop_column("category")
