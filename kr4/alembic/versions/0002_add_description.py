"""add description to products

Revision ID: 0002_add_description
Revises: 0001_create_products
Create Date: 2026-05-22 12:30:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_add_description"
down_revision: Union[str, None] = "0001_create_products"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Двухшаговое добавление NOT NULL-колонки в SQLite через batch:
    # 1) добавляем nullable
    # 2) заполняем дефолтом для существующих строк
    # 3) делаем NOT NULL
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(sa.Column("description", sa.Text(), nullable=True))

    op.execute("UPDATE products SET description = '' WHERE description IS NULL")

    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("description", existing_type=sa.Text(), nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("description")
