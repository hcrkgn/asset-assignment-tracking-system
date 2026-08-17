from datetime import datetime

from app.database.db import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    AuditID = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    UserID = db.Column(
        db.Integer,
        db.ForeignKey("users.UserID"),
        nullable=False
    )

    Action = db.Column(
        db.String(50),
        nullable=False
    )

    RecordType = db.Column(
        db.String(50),
        nullable=False
    )

    RecordID = db.Column(
        db.Integer,
        nullable=False
    )

    FieldName = db.Column(
        db.String(100),
        nullable=False
    )

    OldValue = db.Column(
        db.Text,
        nullable=True
    )

    NewValue = db.Column(
        db.Text,
        nullable=True
    )

    CreatedAt = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )