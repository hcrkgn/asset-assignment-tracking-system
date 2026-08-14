from datetime import date

from app.database.db import db


class Request(db.Model):
    __tablename__ = "requests"

    RequestID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    RequesterID = db.Column(
        db.Integer,
        db.ForeignKey("users.UserID"),
        nullable=False
    )

    requester = db.relationship(
    "User",
    foreign_keys=[RequesterID]
)

    CategoryID = db.Column(
        db.Integer,
        db.ForeignKey("categories.CategoryID"),
        nullable=False
    )

    AssetID = db.Column(
        db.Integer,
        db.ForeignKey("assets.AssetID"),
        nullable=True
    )

    RequestDate = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    Quantity = db.Column(
        db.Integer,
        nullable=False
    )

    Status = db.Column(
        db.String(50),
        nullable=False,
        default="PENDING"
    )

    Description = db.Column(db.Text)

    RejectionReason = db.Column(
        db.Text,
        nullable=True
    )