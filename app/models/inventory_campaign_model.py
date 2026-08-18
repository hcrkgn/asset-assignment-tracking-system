from datetime import datetime

from app.database.db import db


class InventoryCampaign(db.Model):
    __tablename__ = "inventory_campaigns"

    CampaignID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    LocationID = db.Column(
        db.Integer,
        db.ForeignKey("locations.LocationID"),
        nullable=False
    )

    CreatedBy = db.Column(
        db.Integer,
        db.ForeignKey("users.UserID"),
        nullable=False
    )

    Status = db.Column(
        db.String(20),
        nullable=False,
        default="OPEN"
    )

    CreatedAt = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    ClosedAt = db.Column(
        db.DateTime,
        nullable=True
    )