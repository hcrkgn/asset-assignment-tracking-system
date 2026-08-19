from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


def calculate_next_maintenance(last_date, period_months):
    if not last_date or not period_months:
        return None

    return last_date + relativedelta(months=period_months)


def get_maintenance_due_soon(assets, days=30):
    today = date.today()
    due_date = today + timedelta(days=days)

    return [
        asset
        for asset in assets
        if asset.NextMaintenanceDate
        and asset.NextMaintenanceDate <= due_date
    ]