from datetime import datetime

from app.database.db import db


class Notification(db.Model):
    __tablename__ = "notifications"

    NotificationID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    UserID = db.Column(
        db.Integer,
        db.ForeignKey("users.UserID"),
        nullable=False
    )

    Message = db.Column(
        db.Text,
        nullable=False
    )

    IsRead = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    CreatedAt = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )