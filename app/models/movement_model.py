from app.database.db import db


class Movement(db.Model):
    __tablename__ = "movements"

    MovementID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    AssetID = db.Column(
        db.Integer,
        db.ForeignKey("assets.AssetID"),
        nullable=False
    )

    AssignmentID = db.Column(
        db.Integer,
        db.ForeignKey("assignments.AssignmentID"),
        nullable=True
    )

    UserID = db.Column(
        db.Integer,
        db.ForeignKey("users.UserID"),
        nullable=True
    )

    MovementType = db.Column(
        db.String(30),
        nullable=False
    )

    Quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    MovementDate = db.Column(
        db.Date,
        nullable=False
    )

    Note = db.Column(
        db.Text,
        nullable=True
    )