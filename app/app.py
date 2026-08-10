import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from app.utils.security import check_password
from flask_migrate import Migrate
from app.database.db import db
from app.utils.auth import require_roles


from app.models.login_attempt_model import (
    clear_login_attempts,
    is_login_locked,
    record_failed_login,
)
from app.models.user_model import User, get_user_by_email
from app.models.location_model import Location
from app.models.category_model import Category
from app.models.asset_model import Asset
from app.models.assignment_model import Assignment


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+mysqlconnector://"
    f"{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}:3306/"
    f"{os.getenv('MYSQL_DATABASE')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)



@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")


@app.route("/assets")
@require_roles(1, 2)
def assets():
    search = request.args.get("search", "").strip()
    category_id = request.args.get("category", "").strip()
    location_id = request.args.get("location", "").strip()
    status = request.args.get("status", "").strip()

    page = request.args.get("page", 1, type=int)
    per_page = 10

    sort = request.args.get("sort", "AssetID")
    direction = request.args.get("direction", "desc")

    query = Asset.query

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                Asset.Code.like(search_pattern),
                Asset.AssetName.like(search_pattern),
                Asset.Brand.like(search_pattern),
                Asset.Model.like(search_pattern),
                Asset.SerialNumber.like(search_pattern),
            )
        )

    if category_id:
        query = query.filter(Asset.CategoryID == category_id)

    if location_id:
        query = query.filter(Asset.LocationID == location_id)

    if status:
        query = query.filter(Asset.Status == status)

    sort_columns = {
        "Code": Asset.Code,
        "AssetName": Asset.AssetName,
        "PurchaseDate": Asset.PurchaseDate,
        "Status": Asset.Status,
    }

    sort_column = sort_columns.get(sort, Asset.AssetID)

    if direction == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    categories = Category.query.all()
    locations = Location.query.all()

    return render_template(
        "assets.html",
        assets=pagination.items,
        pagination=pagination,
        categories=categories,
        locations=locations,
        search=search,
        selected_category=category_id,
        selected_location=location_id,
        selected_status=status,
        sort=sort,
        direction=direction,
    )



@app.route("/assets/create", methods=["GET", "POST"])
@require_roles(1, 2)
def create_asset():
    if request.method == "POST":
        asset = Asset(
            Code=request.form["Code"].strip(),
            AssetName=request.form["AssetName"].strip(),
            CategoryID=request.form["CategoryID"],
            LocationID=request.form["LocationID"],
            Brand=request.form.get("Brand", "").strip() or None,
            Model=request.form.get("Model", "").strip() or None,
            SerialNumber=request.form.get("SerialNumber", "").strip() or None,
            Quantity=request.form.get("Quantity", 1),
            AssetType=request.form["AssetType"].strip(),
            PurchaseDate=request.form.get("PurchaseDate") or None,
            PurchasePrice=request.form.get("PurchasePrice") or None,
            WarrantyEnd=request.form.get("WarrantyEnd") or None,
            Status=request.form["Status"].strip(),
            Notes=request.form.get("Notes", "").strip() or None,
        )

        db.session.add(asset)
        db.session.commit()

        flash("Asset successfully added.")
        return redirect(url_for("assets"))

    categories = Category.query.all()
    locations = Location.query.all()

    return render_template(
        "asset_create.html",
        categories=categories,
        locations=locations
    )



@app.route("/assignments")
@require_roles(1, 2)
def assignments():
    assignments = Assignment.query.all()
    return render_template("assignments.html", assignments=assignments)


@app.route("/assignments/create", methods=["GET", "POST"])
@require_roles(1, 2)
def create_assignment():
    if request.method == "POST":
        assignment = Assignment(
            AssetID=request.form["AssetID"],
            UserID=request.form["UserID"],
            AssignedDate=request.form["AssignedDate"]
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Asset successfully assigned.")
        return redirect(url_for("assignments"))

    assets = Asset.query.filter_by(Status="IN STOCK").all()
    users = User.query.all()

    return render_template(
        "assignment_create.html",
        assets=assets,
        users=users
    )



@app.route("/assignments/<int:assignment_id>")
@require_roles(1, 2)
def assignment_detail(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        flash("Assignment not found.")
        return redirect(url_for("assignments"))

    return render_template(
        "assignment_detail.html",
        assignment=assignment
    )

@app.route("/assignments/<int:assignment_id>/edit", methods=["GET", "POST"])
@require_roles(1, 2)
def edit_assignment(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        flash("Assignment not found.")
        return redirect(url_for("assignments"))

    if request.method == "POST":
        assignment.AssetID = request.form["AssetID"]
        assignment.UserID = request.form["UserID"]
        assignment.AssignedDate = request.form["AssignedDate"]
        assignment.ReturnedDate = request.form.get("ReturnedDate") or None

        db.session.commit()

        flash("Assignment successfully updated.")
        return redirect(url_for("assignments"))

    assets = Asset.query.all()
    users = User.query.all()

    return render_template(
        "assignment_edit.html",
        assignment=assignment,
        assets=assets,
        users=users
    )



@app.route("/assignments/<int:assignment_id>/return", methods=["POST"])
@require_roles(1, 2)
def return_assignment(assignment_id):
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        flash("Assignment not found.")
        return redirect(url_for("assignments"))

    if assignment.ReturnedDate:
        flash("This assignment has already been returned.")
        return redirect(url_for("assignments"))

    asset = db.session.get(Asset, assignment.AssetID)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assignments"))

    from datetime import date

    assignment.ReturnedDate = date.today()
    asset.Status = "IN STOCK"

    db.session.commit()

    flash("Asset successfully returned.")
    return redirect(url_for("assignments"))




@app.route("/assets/<int:asset_id>/edit", methods=["GET", "POST"])
@require_roles(1, 2)
def edit_asset(asset_id):
    asset = db.session.get(Asset, asset_id)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assets"))

    if request.method == "POST":
        asset.Code = request.form["Code"].strip()
        asset.AssetName = request.form["AssetName"].strip()
        asset.CategoryID = request.form["CategoryID"]
        asset.LocationID = request.form["LocationID"]
        asset.Brand = request.form.get("Brand", "").strip() or None
        asset.Model = request.form.get("Model", "").strip() or None
        asset.SerialNumber = request.form.get("SerialNumber", "").strip() or None
        asset.Quantity = request.form.get("Quantity", 1)
        asset.AssetType = request.form["AssetType"].strip()
        asset.PurchaseDate = request.form.get("PurchaseDate") or None
        asset.PurchasePrice = request.form.get("PurchasePrice") or None
        asset.WarrantyEnd = request.form.get("WarrantyEnd") or None
        asset.Status = request.form["Status"].strip()
        asset.Notes = request.form.get("Notes", "").strip() or None

        db.session.commit()

        flash("Asset successfully updated.")
        return redirect(url_for("assets"))

    categories = Category.query.all()
    locations = Location.query.all()

    return render_template(
        "asset_edit.html",
        asset=asset,
        categories=categories,
        locations=locations
    )


@app.route("/assets/<int:asset_id>/delete", methods=["POST"])
@require_roles(1, 2)
def delete_asset(asset_id):
    asset = db.session.get(Asset, asset_id)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assets"))

    db.session.delete(asset)
    db.session.commit()

    flash("Asset successfully deleted.")
    return redirect(url_for("assets"))



@app.route("/assets/<int:asset_id>")
@require_roles(1, 2)
def asset_detail(asset_id):
    asset = db.session.get(Asset, asset_id)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assets"))

    return render_template("asset_detail.html", asset=asset)




@app.route("/admin")
@require_roles(1)
def admin_dashboard():
    return "<h1>Admin Panel</h1><p>Only the Admin can see this page..</p>"


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
            flash("You have made too many failed login attempts. Please try again in 15 minutes.")
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
            flash("Your account has been locked for 15 minutes due to 20 failed login attempts.")
            return render_template("login.html"), 429

        flash("Incorrect email or password.")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have successfully logged out.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
