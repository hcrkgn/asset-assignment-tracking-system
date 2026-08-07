from app.database.db import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    InventoryID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    AssetID = db.Column(
        db.Integer,
        db.ForeignKey("assets.AssetID"),
        nullable=False
    )

    CountedQuantity = db.Column(db.Integer, nullable=False)
    CountDate = db.Column(db.Date, nullable=False)