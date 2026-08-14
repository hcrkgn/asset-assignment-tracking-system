import os
import uuid       
from datetime import timedelta

from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv

from werkzeug.utils import secure_filename

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

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
from app.models.movement_model import Movement  
from app.models.request_model import Request 
from app.models.department_model import Department # noqa: F401

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

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)



app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


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

    sort = request.args.get("sort", "AssetID")
    direction = request.args.get("direction", "desc")

    allowed_sort_fields = {
        "AssetID": Asset.AssetID,
        "Code": Asset.Code,
        "AssetName": Asset.AssetName,
        "Status": Asset.Status,
    }

    sort_column = allowed_sort_fields.get(sort, Asset.AssetID)

    page = request.args.get("page", 1, type=int)
    per_page = 10

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
        purchase_price = request.form.get("PurchasePrice", "").strip()

        if purchase_price:
            purchase_price = purchase_price.replace(",", ".")

            try:
                purchase_price = float(purchase_price)
            except ValueError:
                flash("Invalid purchase price.")
                return redirect(url_for("create_asset"))

            if purchase_price < 0:
                flash("Purchase price cannot be negative.")
                return redirect(url_for("create_asset"))
        else:
            purchase_price = None

        invoice_file = request.files.get("InvoiceFile")
        warranty_file = request.files.get("WarrantyFile")

        invoice_filename = None
        warranty_filename = None

        if invoice_file and invoice_file.filename:
            if not allowed_file(invoice_file.filename):
                flash("Invalid invoice file type.")
                return redirect(url_for("create_asset"))

            invoice_filename = (
                f"{uuid.uuid4().hex}_{secure_filename(invoice_file.filename)}"
            )
            invoice_file.save(
                os.path.join(UPLOAD_FOLDER, invoice_filename)
            )

        if warranty_file and warranty_file.filename:
            if not allowed_file(warranty_file.filename):
                flash("Invalid warranty file type.")
                return redirect(url_for("create_asset"))

            warranty_filename = (
                f"{uuid.uuid4().hex}_{secure_filename(warranty_file.filename)}"
            )
            warranty_file.save(
                os.path.join(UPLOAD_FOLDER, warranty_filename)
            )

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
            PurchasePrice=purchase_price,
            WarrantyEnd=request.form.get("WarrantyEnd") or None,
            Status=request.form["Status"].strip(),
            Notes=request.form.get("Notes", "").strip() or None,
            InvoiceFile=invoice_filename,
            WarrantyFile=warranty_filename,
        )

        try:
            db.session.add(asset)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Serial number already exists.")
            return redirect(url_for("create_asset"))

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
        asset_id = request.form["AssetID"]
        user_id = request.form["UserID"]
        assigned_date = request.form["AssignedDate"]
        quantity = int(request.form.get("Quantity", 1))
        note = request.form.get("Note", "").strip() or None

        asset = db.session.get(Asset, asset_id)

        if not asset:
            flash("Asset not found.")
            return redirect(url_for("create_assignment"))

        if asset.Status in ["IN MAINTENANCE", "SCRAPPED"]:
            flash("This asset cannot be assigned.")
            return redirect(url_for("create_assignment"))

        if quantity < 1:
            flash("Quantity must be at least 1.")
            return redirect(url_for("create_assignment"))

        if asset.AssetType == "Individual" and quantity != 1:
            flash("An individual asset can only be assigned as 1.")
            return redirect(url_for("create_assignment"))

        if asset.AssetType == "Quantity" and quantity > asset.Quantity:
            flash("Assignment quantity cannot exceed available quantity.")
            return redirect(url_for("create_assignment"))

        if asset.AssetType == "Individual":
            existing_assignment = Assignment.query.filter_by(
                AssetID=asset.AssetID,
                ReturnedDate=None
            ).first()

            if existing_assignment:
                flash("This asset is already assigned.")
                return redirect(url_for("create_assignment"))

        try:
            assignment = Assignment(
                AssetID=asset.AssetID,
                UserID=user_id,
                AssignedDate=assigned_date,
                Quantity=quantity,
                Note=note
            )

            db.session.add(assignment)
            db.session.flush()

            movement = Movement(
                AssetID=asset.AssetID,
                AssignmentID=assignment.AssignmentID,
                UserID=user_id,
                MovementType="ASSIGN",
                Quantity=quantity,
                MovementDate=assigned_date,
                Note=note
            )

            db.session.add(movement)

            if asset.AssetType == "Individual":
                 asset.Status = "ASSIGNED"
            else:
                 asset.Quantity -= quantity
                

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Assignment error: {e}")
            flash("Assignment could not be completed.")
            return redirect(url_for("create_assignment"))

        flash("Asset successfully assigned.")
        return redirect(url_for("assignments"))

    assets = Asset.query.filter(
        Asset.Status.notin_(["IN MAINTENANCE", "SCRAPPED"])
    ).all()

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



@app.route(
    "/assignments/<int:assignment_id>/return",
    methods=["GET", "POST"]
)
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

    if request.method == "POST":
        try:
            return_quantity = int(request.form.get("Quantity", 0))
        except ValueError:
            flash("Invalid return quantity.")
            return redirect(
                url_for(
                    "return_assignment",
                    assignment_id=assignment_id
                )
            )

        return_condition = request.form.get(
            "ReturnCondition",
            ""
        ).strip()

        if return_quantity < 1:
            flash("Return quantity must be at least 1.")
            return redirect(
                url_for(
                    "return_assignment",
                    assignment_id=assignment_id
                )
            )

        if return_quantity > assignment.Quantity:
            flash("Return quantity cannot exceed assigned quantity.")
            return redirect(
                url_for(
                    "return_assignment",
                    assignment_id=assignment_id
                )
            )

        if return_condition not in ["INTACT", "FAULTY"]:
            flash("Please select a valid return condition.")
            return redirect(
                url_for(
                    "return_assignment",
                    assignment_id=assignment_id
                )
            )

        from datetime import date

        try:
            movement = Movement(
                AssetID=asset.AssetID,
                AssignmentID=assignment.AssignmentID,
                UserID=assignment.UserID,
                MovementType="RETURN",
                Quantity=return_quantity,
                MovementDate=date.today(),
                Note=f"Return condition: {return_condition}"
            )

            db.session.add(movement)

            assignment.Quantity -= return_quantity
            assignment.ReturnCondition = return_condition

            if asset.AssetType == "Quantity":
                if return_condition == "INTACT":
                    asset.Quantity += return_quantity

            if assignment.Quantity == 0:
                assignment.ReturnedDate = date.today()

                if return_condition == "FAULTY":
                    asset.Status = "FAULTY"
                else:
                    asset.Status = "IN STOCK"

            db.session.commit()

        except Exception:
            db.session.rollback()
            flash("Asset return could not be completed.")
            return redirect(url_for("assignments"))

        flash("Asset successfully returned.")
        return redirect(url_for("assignments"))

    return render_template(
        "assignment_return.html",
        assignment=assignment,
        asset=asset
    )


@app.route("/users/<int:user_id>/assignment-history")
@require_roles(1, 2)
def user_assignment_history(user_id):
    user = db.session.get(User, user_id)

    if not user:
        flash("User not found.")
        return redirect(url_for("assignments"))

    assignments = (
        Assignment.query
        .filter_by(UserID=user_id)
        .order_by(Assignment.AssignedDate.desc())
        .all()
    )

    return render_template(
        "user_assignment_history.html",
        user=user,
        assignments=assignments
    )


@app.route("/assets/<int:asset_id>/ownership-history")
@require_roles(1, 2)
def asset_ownership_history(asset_id):
    asset = db.session.get(Asset, asset_id)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assets"))

    assignments = (
        Assignment.query
        .filter_by(AssetID=asset_id)
        .order_by(Assignment.AssignedDate.desc())
        .all()
    )

    return render_template(
        "asset_ownership_history.html",
        asset=asset,
        assignments=assignments
    )


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


@app.route("/requests/create", methods=["GET", "POST"])
@require_roles(3, 4)
def create_request():
    if request.method == "POST":
        category_id = request.form.get("CategoryID")
        asset_id = request.form.get("AssetID") or None
        quantity = request.form.get("Quantity", type=int)
        description = request.form.get("Description", "").strip()

        if not category_id:
            flash("Category is required.")
            return redirect(url_for("create_request"))

        if not quantity or quantity < 1:
            flash("Quantity must be at least 1.")
            return redirect(url_for("create_request"))

        new_request = Request(
            RequesterID=session["user_id"],
            CategoryID=category_id,
            AssetID=asset_id,
            Quantity=quantity,
            Description=description or None,
            Status="PENDING"
        )

        db.session.add(new_request)
        db.session.commit()

        flash("Request successfully created.")
        return redirect(url_for("requests_page"))

    categories = Category.query.all()
    assets = Asset.query.all()

    return render_template(
        "request_create.html",
        categories=categories,
        assets=assets
    )


@app.route("/requests")
@require_roles(3, 4)
def requests_page():
    requests = (
        Request.query
        .filter_by(RequesterID=session["user_id"])
        .order_by(Request.RequestDate.desc())
        .all()
    )

    return render_template(
        "requests.html",
        requests=requests
    )


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(413)
def request_entity_too_large(error):
    flash("File size must not exceed 50 MB.")
    return redirect(url_for("create_asset"))


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





@app.route("/manager/requests")
@require_roles(3)
def manager_requests():
    pending_requests = (
        Request.query
        .filter(Request.Status == "PENDING")
        .order_by(Request.RequestDate.desc())
        .all()
    )

    processed_requests = (
        Request.query
        .filter(
            Request.Status.in_(["APPROVED", "REJECTED"])
        )
        .order_by(Request.RequestDate.desc())
        .all()
    )

    return render_template(
        "manager_requests.html",
        pending_requests=pending_requests,
        processed_requests=processed_requests,
    )



    

@app.route("/manager/requests/<int:request_id>/approve", methods=["POST"])
@require_roles(3)
def approve_request(request_id):
    manager = db.session.get(User, session["user_id"])
    req = db.session.get(Request, request_id)

    if not req or not manager:
        return render_template("403.html"), 403

    requester = db.session.get(User, req.RequesterID)

    if not requester or requester.DepartmentID != manager.DepartmentID:
        return render_template("403.html"), 403

    if req.Status != "PENDING":
        flash("This request has already been processed.")
        return redirect(url_for("manager_requests"))

    req.Status = "APPROVED"
    db.session.commit()

    flash("Request approved.")
    return redirect(url_for("manager_requests"))



@app.route("/manager/requests/<int:request_id>/reject", methods=["POST"])
@require_roles(3)
def reject_request(request_id):
    manager = db.session.get(User, session["user_id"])
    req = db.session.get(Request, request_id)

    if not req or not manager:
        return render_template("403.html"), 403

    requester = db.session.get(User, req.RequesterID)

    if not requester or requester.DepartmentID != manager.DepartmentID:
        return render_template("403.html"), 403

    if req.Status != "PENDING":
        flash("This request has already been processed.")
        return redirect(url_for("manager_requests"))

    rejection_reason = request.form.get("RejectionReason", "").strip()

    if not rejection_reason:
        flash("Rejection reason is required.")
        return redirect(url_for("manager_requests"))

    req.Status = "REJECTED"
    req.RejectionReason = rejection_reason

    db.session.commit()

    flash("Request rejected.")
    return redirect(url_for("manager_requests"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
