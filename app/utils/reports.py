from sqlalchemy import func
from datetime import date

from app.models.asset_model import Asset 
from app.models.category_model import Category 
from app.database.db import db
from app.models.assignment_model import Assignment
from app.models.department_model import Department
from app.models.user_model import User


def get_assignments_by_department():
    results = (
        db.session.query(
            Department.DepartmentName,
            func.sum(Assignment.Quantity).label("TotalQuantity")
        )
        .join(User, User.DepartmentID == Department.DepartmentID)
        .join(Assignment, Assignment.UserID == User.UserID)
        .group_by(
            Department.DepartmentID,
            Department.DepartmentName
        )
        .order_by(Department.DepartmentName)
        .all()
    )

    return results

def get_value_by_category():
    results = (
        db.session.query(
            Category.CategoryName,
            func.sum(
                Asset.PurchasePrice * Asset.Quantity
            ).label("TotalValue")
        )
        .join(
            Asset,
            Asset.CategoryID == Category.CategoryID
        )
        .group_by(
            Category.CategoryID,
            Category.CategoryName
        )
        .order_by(Category.CategoryName)
        .all()
    )

    return results

def get_asset_ageing():
    today = date.today()

    assets = (
        Asset.query
        .filter(Asset.PurchaseDate.isnot(None))
        .all()
    )

    ageing = {
        "0-1 year": 0,
        "1-3 years": 0,
        "3+ years": 0,
    }

    for asset in assets:
        if asset.PurchaseDate > today:
            ageing["0-1 year"] += 1
            continue

        age_days = (today - asset.PurchaseDate).days
        age_years = age_days / 365.25

        if age_years < 1:
            ageing["0-1 year"] += 1
        elif age_years < 3:
            ageing["1-3 years"] += 1
        else:
            ageing["3+ years"] += 1

    return ageing

def get_maintenance_history():
    results = (
        db.session.query(
            Asset.AssetID,
            Asset.Code,
            Asset.AssetName,
            Asset.LastMaintenanceDate,
            Asset.NextMaintenanceDate,
            Asset.Status
        )
        .filter(
            Asset.LastMaintenanceDate.isnot(None)
        )
        .order_by(
            Asset.LastMaintenanceDate.desc()
        )
        .all()
    )

    return results