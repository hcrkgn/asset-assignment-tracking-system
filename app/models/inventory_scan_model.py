from datetime import datetime

from app.database.db import db


class InventoryScan(db.Model):
    __tablename__ = "inventory_scans"

    ScanID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    CampaignID = db.Column(
        db.Integer,
        db.ForeignKey("inventory_campaigns.CampaignID"),
        nullable=False
    )

    AssetID = db.Column(
        db.Integer,
        db.ForeignKey("assets.AssetID"),
        nullable=False
    )

    ScanStatus = db.Column(
        db.String(30),
        nullable=False
    )

    ScannedAt = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )