from app.database.db import get_db_connection


def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE Email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user