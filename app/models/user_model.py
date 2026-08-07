from app.database.db import db, get_db_connection


class User(db.Model):
    __tablename__ = "users"

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)

    RoleID = db.Column(
        db.Integer,
        db.ForeignKey("roles.RoleID"),
        nullable=False
    )

    DepartmentID = db.Column(
        db.Integer,
        db.ForeignKey("departments.DepartmentID"),
        nullable=True
    )


def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE Email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user