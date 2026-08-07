from app.database.db import db


class Location(db.Model):
    __tablename__ = "locations"

    LocationID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    LocationName = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )