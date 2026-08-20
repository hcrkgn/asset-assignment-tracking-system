import csv
import io

from app.database.db import db
from app.models.asset_model import Asset


REQUIRED_FIELDS = {
    "Code",
    "AssetName",
    "CategoryID",
    "LocationID",
    "AssetType",
    "Status",
}


def import_assets_from_csv(file_content):
    decoded_content = file_content.decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(decoded_content))

    imported_count = 0
    errors = []

    for row_number, row in enumerate(reader, start=2):
        try:
            missing_fields = [
                field
                for field in REQUIRED_FIELDS
                if not row.get(field, "").strip()
            ]

            if missing_fields:
                raise ValueError(
                    f"Missing required fields: {', '.join(missing_fields)}"
                )

            code = row["Code"].strip()

            if Asset.query.filter_by(Code=code).first():
                raise ValueError(f"Code already exists: {code}")

            quantity = int(row.get("Quantity") or 1)

            if quantity < 1:
                raise ValueError("Quantity must be at least 1.")

            purchase_price = row.get("PurchasePrice", "").strip()

            if purchase_price:
                purchase_price = float(
                    purchase_price.replace(",", ".")
                )
            else:
                purchase_price = None

            asset = Asset(
                Code=code,
                AssetName=row["AssetName"].strip(),
                CategoryID=int(row["CategoryID"]),
                LocationID=int(row["LocationID"]),
                Brand=row.get("Brand", "").strip() or None,
                Model=row.get("Model", "").strip() or None,
                SerialNumber=row.get("SerialNumber", "").strip() or None,
                Quantity=quantity,
                AssetType=row["AssetType"].strip(),
                PurchaseDate=row.get("PurchaseDate") or None,
                PurchasePrice=purchase_price,
                WarrantyEnd=row.get("WarrantyEnd") or None,
                MaintenancePeriodMonths=(
                    int(row["MaintenancePeriodMonths"])
                    if row.get("MaintenancePeriodMonths")
                    else None
                ),
                LastMaintenanceDate=(
                    row["LastMaintenanceDate"]
                    if row.get("LastMaintenanceDate")
                    else None
                ),
                NextMaintenanceDate=(
                    row["NextMaintenanceDate"]
                    if row.get("NextMaintenanceDate")
                    else None
                ),
                UsefulLifeMonths=(
                    int(row["UsefulLifeMonths"])
                    if row.get("UsefulLifeMonths")
                    else None
                ),
                SalvageValue=(
                    float(row["SalvageValue"].replace(",", "."))
                    if row.get("SalvageValue")
                    else None
                ),
                Status=row["Status"].strip(),
                Notes=row.get("Notes", "").strip() or None,
            )

            db.session.add(asset)
            db.session.flush()

            imported_count += 1

        except Exception as error:
            db.session.rollback()
            errors.append({
                "row": row_number,
                "error": str(error),
            })

    db.session.commit()

    return imported_count, errors