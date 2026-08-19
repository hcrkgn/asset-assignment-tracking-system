from app.database.db import db


class Asset(db.Model):
    __tablename__ = "assets"

    AssetID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Code = db.Column(db.String(50), nullable=False, unique=True)
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

    Brand = db.Column(db.String(100))
    Model = db.Column(db.String(100))

    SerialNumber = db.Column(db.String(100), unique=True)
    Quantity = db.Column(db.Integer, default=1)
    AssetType = db.Column(db.String(50), nullable=False)

    PurchaseDate = db.Column(db.Date)
    PurchasePrice = db.Column(db.Numeric(10, 2))
    WarrantyEnd = db.Column(db.Date)

    MaintenancePeriodMonths = db.Column(db.Integer)
    LastMaintenanceDate = db.Column(db.Date)
    NextMaintenanceDate = db.Column(db.Date)

    Status = db.Column(db.String(50), nullable=False)
    Notes = db.Column(db.Text)

    InvoiceFile = db.Column(db.String(255))
    WarrantyFile = db.Column(db.String(255))