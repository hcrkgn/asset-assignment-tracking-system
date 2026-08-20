import csv
import io


def export_assets_to_csv(assets):
    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "AssetID",
        "Code",
        "AssetName",
        "CategoryID",
        "LocationID",
        "Brand",
        "Model",
        "SerialNumber",
        "Quantity",
        "AssetType",
        "PurchaseDate",
        "PurchasePrice",
        "WarrantyEnd",
        "MaintenancePeriodMonths",
        "LastMaintenanceDate",
        "NextMaintenanceDate",
        "UsefulLifeMonths",
        "SalvageValue",
        "Status",
        "Notes",
    ])

    for asset in assets:
        writer.writerow([
            asset.AssetID,
            asset.Code,
            asset.AssetName,
            asset.CategoryID,
            asset.LocationID,
            asset.Brand,
            asset.Model,
            asset.SerialNumber,
            asset.Quantity,
            asset.AssetType,
            asset.PurchaseDate,
            asset.PurchasePrice,
            asset.WarrantyEnd,
            asset.MaintenancePeriodMonths,
            asset.LastMaintenanceDate,
            asset.NextMaintenanceDate,
            asset.UsefulLifeMonths,
            asset.SalvageValue,
            asset.Status,
            asset.Notes,
        ])

    return "\ufeff" + output.getvalue()