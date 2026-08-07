from app.database.db import db


class Role(db.Model):
    __tablename__ = "roles"

    RoleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoleName = db.Column(db.String(50), nullable=False, unique=True)