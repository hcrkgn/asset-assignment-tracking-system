import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from app.models.login_attempt_model import (
    clear_login_attempts,
    is_login_locked,
    record_failed_login,
)

from app.models.user_model import get_user_by_email
from app.utils.auth import require_roles
from app.utils.security import check_password

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")


@app.route("/admin")
@require_roles(1)
def admin_dashboard():
    return "<h1>Admin Paneli</h1><p>Bu sayfayı yalnızca Admin görebilir.</p>"


@app.route("/api/session")
@require_roles(1, 2, 3, 4)
def session_info():
    return jsonify({
        "user_name": session["user_name"],
        "role_id": session["role_id"],
    })


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if is_login_locked(email):
            flash("Çok fazla başarısız giriş denemesi yaptınız. Lütfen 15 dakika sonra tekrar deneyin.")
            return render_template("login.html"), 429

        user = get_user_by_email(email)

        if user and check_password(password, user["Password"]):
            clear_login_attempts(email)

            session.permanent = True
            session["user_id"] = user["UserID"]
            session["user_name"] = user["Name"]
            session["role_id"] = user["RoleID"]

            return redirect(url_for("home"))

        account_is_locked = record_failed_login(email)

        if account_is_locked:
            flash("20 hatalı giriş denemesi nedeniyle hesabınız 15 dakika kilitlendi.")
            return render_template("login.html"), 429

        flash("E-posta veya şifre hatalı.")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
