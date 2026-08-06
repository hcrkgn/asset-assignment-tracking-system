import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

from app.models.user_model import get_user_by_email
from app.utils.security import check_password

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return f"Welcome, {session['user_name']}!"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password(password, user["Password"]):
            session["user_id"] = user["UserID"]
            session["user_name"] = user["Name"]
            session["role_id"] = user["RoleID"]

            return redirect(url_for("home"))

        flash("E-posta veya şifre hatalı.")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)