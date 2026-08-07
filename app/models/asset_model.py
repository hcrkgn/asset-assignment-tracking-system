from app.database.db import db


class Asset(db.Model):
    __tablename__ = "assets"

    AssetID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssetName = db.Column(db.String(100), nullable=False)

    CategoryID = db.Column(
        db.Integer,
        db.ForeignKey("categories.CategoryID"),
        nullable=False
    )

    LocationID = db.Column(
    db.Integer,
    db.ForeignKey("locations.LocationID"),
    nullable=False
)

    SerialNumber = db.Column(db.String(100), unique=True)
    Quantity = db.Column(db.Integer, default=1)
    AssetType = db.Column(db.String(50))
    Status = db.Column(db.String(50), nullable=False)
    PurchaseDate = db.Column(db.Date)