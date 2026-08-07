from app.database.db import db


class Maintenance(db.Model):
    __tablename__ = "maintenance"

    MaintenanceID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    AssetID = db.Column(
        db.Integer,
        db.ForeignKey("assets.AssetID"),
        nullable=False
    )

    Description = db.Column(db.Text)
    MaintenanceDate = db.Column(db.Date)
    Status = db.Column(db.String(50))