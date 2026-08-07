from app.database.db import db


class Department(db.Model):
    __tablename__ = "departments"

    DepartmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DepartmentName = db.Column(db.String(100), nullable=False, unique=True)