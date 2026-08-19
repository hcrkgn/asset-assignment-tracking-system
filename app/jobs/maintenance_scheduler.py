import time
from datetime import datetime, timedelta

from app.app import app
from app.jobs.maintenance_job import run_maintenance_job


def seconds_until_next_run():
    now = datetime.now()

    next_run = now.replace(
        hour=8,
        minute=0,
        second=0,
        microsecond=0
    )

    if next_run <= now:
        next_run += timedelta(days=1)

    return (next_run - now).total_seconds()


while True:
    sleep_seconds = seconds_until_next_run()

    print(
        f"Next maintenance job will run in "
        f"{sleep_seconds / 3600:.2f} hours."
    )

    time.sleep(sleep_seconds)

    with app.app_context():
        count = run_maintenance_job()
        print(
            f"Scheduled maintenance job completed. "
            f"{count} notification(s) created."
        )