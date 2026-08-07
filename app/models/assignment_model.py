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
    ReturnedDate = db.Column(db.Date)