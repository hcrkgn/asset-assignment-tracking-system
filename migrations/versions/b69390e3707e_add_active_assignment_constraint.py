"""add active assignment constraint

Revision ID: b69390e3707e
Revises: b66e2ef9fec2
Create Date: 2026-08-13 10:03:55.771072
"""

from alembic import op
import sqlalchemy as sa


revision = "b69390e3707e"
down_revision = "b66e2ef9fec2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "assignments",
        sa.Column(
            "ActiveAssetID",
            sa.Integer(),
            sa.Computed(
                "CASE WHEN ReturnedDate IS NULL THEN AssetID ELSE NULL END",
                persisted=True,
            ),
            nullable=True,
        ),
    )

    op.create_index(
        "uq_active_asset_assignment",
        "assignments",
        ["ActiveAssetID"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        "uq_active_asset_assignment",
        table_name="assignments",
    )

    op.drop_column(
        "assignments",
        "ActiveAssetID",
    )