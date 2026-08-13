from app.database.db import db


class Assignment(db.Model):
    __tablename__ = "assignments"

    AssignmentID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    AssetID = db.Column(
        db.Integer,
        db.ForeignKey("assets.AssetID"),
        nullable=False
    )

    UserID = db.Column(
        db.Integer,
        db.ForeignKey("users.UserID"),
        nullable=False
    )

    AssignedDate = db.Column(db.Date, nullable=False)

    Quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    Note = db.Column(
        db.Text,
        nullable=True
    )

    ReturnedDate = db.Column(
        db.Date,
        nullable=True
    )

    ReturnCondition = db.Column(
        db.String(20),
        nullable=True
    )

    __table_args__ = (
        db.Index(
            "idx_active_asset_assignment",
            "AssetID",
            "ReturnedDate"
        ),
    )