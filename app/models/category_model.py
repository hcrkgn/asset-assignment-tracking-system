from app.database.db import db


class Category(db.Model):
    __tablename__ = "categories"

    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String(100), nullable=False, unique=True)