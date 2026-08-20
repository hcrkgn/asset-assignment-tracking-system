import csv
import io

from app.database.db import db
from app.models.asset_model import Asset


def import_assets_from_csv(file_content):
    valid_assets = []
    invalid_rows = []

    reader = csv.DictReader(io.StringIO(file_content))

    for row_number, row in enumerate(reader, start=2):
        try:
            code = row["Code"].strip()
            asset_name = row["AssetName"].strip()
            category_id = int(row["CategoryID"])
            location_id = int(row["LocationID"])

            if not code or not asset_name:
                raise ValueError("Code and AssetName are required.")

            quantity = int(row.get("Quantity") or 1)

            if quantity < 1:
                raise ValueError("Quantity must be greater than 0.")

            purchase_price = row.get("PurchasePrice") or None

            if purchase_price:
                purchase_price = float(
                    purchase_price.replace(",", ".")
                )

            asset = Asset(
                Code=code,
                AssetName=asset_name,
                CategoryID=category_id,
                LocationID=location_id,
                Brand=row.get("Brand") or None,
                Model=row.get("Model") or None,
                SerialNumber=row.get("SerialNumber") or None,
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
                    row.get("LastMaintenanceDate") or None
                ),
                NextMaintenanceDate=(
                    row.get("NextMaintenanceDate") or None
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
                Notes=row.get("Notes") or None,
            )

            valid_assets.append(asset)

        except (ValueError, KeyError) as error:
            invalid_rows.append({
                "row": row_number,
                "error": str(error),
            })

    for asset in valid_assets:
        db.session.add(asset)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "imported": len(valid_assets),
        "invalid": invalid_rows,
    }