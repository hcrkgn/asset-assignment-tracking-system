"""add asset details

Revision ID: d1a2c35055d4
Revises: 6033ee499a43
Create Date: 2026-08-10 13:40:16.518913
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "d1a2c35055d4"
down_revision = "6033ee499a43"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("assets", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("Code", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(
            sa.Column("Brand", sa.String(length=100), nullable=True)
        )
        batch_op.add_column(
            sa.Column("Model", sa.String(length=100), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "PurchasePrice",
                sa.Numeric(precision=10, scale=2),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column("WarrantyEnd", sa.Date(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("Notes", sa.Text(), nullable=True)
        )

        batch_op.alter_column(
            "AssetType",
            existing_type=mysql.VARCHAR(length=50),
            nullable=False,
        )

    # Existing assets need unique codes before adding NOT NULL + UNIQUE.
    op.execute(
        """
        UPDATE assets
        SET Code = CONCAT('AST-', AssetID)
        WHERE Code IS NULL OR Code = ''
        """
    )

    with op.batch_alter_table("assets", schema=None) as batch_op:
        batch_op.alter_column(
            "Code",
            existing_type=sa.String(length=50),
            nullable=False,
        )
        batch_op.create_unique_constraint(
            "uq_assets_code",
            ["Code"],
        )


def downgrade():
    with op.batch_alter_table("assets", schema=None) as batch_op:
        batch_op.drop_constraint(
            "uq_assets_code",
            type_="unique",
        )
        batch_op.alter_column(
            "AssetType",
            existing_type=mysql.VARCHAR(length=50),
            nullable=True,
        )
        batch_op.drop_column("Notes")
        batch_op.drop_column("WarrantyEnd")
        batch_op.drop_column("PurchasePrice")
        batch_op.drop_column("Model")
        batch_op.drop_column("Brand")
        batch_op.drop_column("Code")