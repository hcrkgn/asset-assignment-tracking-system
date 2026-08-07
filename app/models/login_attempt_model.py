from app.database.db import db, get_db_connection

from app.database.db import get_db_connection


MAX_FAILED_ATTEMPTS = 20
LOCK_DURATION_MINUTES = 15

class LoginAttempt(db.Model):
    __tablename__ = "login_attempts"

    Email = db.Column(
        db.String(100),
        primary_key=True
    )

    FailedAttempts = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    LockedUntil = db.Column(db.DateTime)

    UpdatedAt = db.Column(
    db.DateTime,
    nullable=False,
    server_default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp()
    )

def is_login_locked(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT LockedUntil FROM login_attempts WHERE Email = %s",
        (email,),
    )
    attempt = cursor.fetchone()

    cursor.close()
    connection.close()

    if not attempt or not attempt["LockedUntil"]:
        return False

    return attempt["LockedUntil"] > datetime.now()


def record_failed_login(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT FailedAttempts, LockedUntil
        FROM login_attempts
        WHERE Email = %s
        """,
        (email,),
    )
    attempt = cursor.fetchone()
    now = datetime.now()

    if attempt and attempt["LockedUntil"] and attempt["LockedUntil"] > now:
        cursor.close()
        connection.close()
        return True

    if not attempt or (
        attempt["LockedUntil"] and attempt["LockedUntil"] <= now
    ):
        failed_attempts = 1
    else:
        failed_attempts = attempt["FailedAttempts"] + 1

    locked_until = None
    if failed_attempts >= MAX_FAILED_ATTEMPTS:
        locked_until = now + timedelta(minutes=LOCK_DURATION_MINUTES)

    if attempt:
        cursor.execute(
            """
            UPDATE login_attempts
            SET FailedAttempts = %s, LockedUntil = %s
            WHERE Email = %s
            """,
            (failed_attempts, locked_until, email),
        )
    else:
        cursor.execute(
            """
            INSERT INTO login_attempts (Email, FailedAttempts, LockedUntil)
            VALUES (%s, %s, %s)
            """,
            (email, failed_attempts, locked_until),
        )

    connection.commit()
    cursor.close()
    connection.close()

    return locked_until is not None


def clear_login_attempts(email):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM login_attempts WHERE Email = %s",
        (email,),
    )

    connection.commit()
    cursor.close()
    connection.close()
