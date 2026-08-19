from datetime import date, timedelta

from app.app import app
from app.database.db import db
from app.models.asset_model import Asset
from app.models.notification_model import Notification


def run_maintenance_job():
    today = date.today()
    due_soon_date = today + timedelta(days=30)

    assets = (
        Asset.query
        .filter(
            Asset.NextMaintenanceDate.isnot(None),
            Asset.NextMaintenanceDate <= due_soon_date
        )
        .all()
    )

    created_count = 0

    for asset in assets:
        message = (
            f"Maintenance due soon for asset "
            f"{asset.Code} - {asset.AssetName}."
        )

        # Aynı bildirim daha önce oluşturulmuşsa tekrar oluşturma
        existing_notification = Notification.query.filter_by(
            UserID=1,
            Message=message
        ).first()

        if existing_notification:
            continue

        notification = Notification(
            UserID=1,
            Message=message
        )

        db.session.add(notification)
        created_count += 1

    db.session.commit()

    return created_count


if __name__ == "__main__":
    with app.app_context():
        count = run_maintenance_job()
        print(f"Maintenance job completed. {count} notification(s) created.")