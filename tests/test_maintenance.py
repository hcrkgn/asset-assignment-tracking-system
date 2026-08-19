from datetime import date

from app.utils.maintenance import (
    calculate_next_maintenance,
    get_maintenance_due_soon,
)


def test_january_31_plus_one_month():
    result = calculate_next_maintenance(
        date(2026, 1, 31),
        1
    )

    assert result == date(2026, 2, 28)


def test_leap_year_january_31_plus_one_month():
    result = calculate_next_maintenance(
        date(2028, 1, 31),
        1
    )

    assert result == date(2028, 2, 29)


def test_six_month_maintenance_period():
    result = calculate_next_maintenance(
        date(2026, 8, 19),
        6
    )

    assert result == date(2027, 2, 19)


def test_maintenance_due_soon():
    class TestAsset:
        def __init__(self, next_date):
            self.NextMaintenanceDate = next_date

    assets = [
        TestAsset(date(2026, 8, 25)),
        TestAsset(date(2026, 9, 10)),
        TestAsset(date(2026, 10, 1)),
    ]

    result = get_maintenance_due_soon(
        assets,
        days=30
    )

    assert len(result) == 2


def test_maintenance_without_date_is_ignored():
    class TestAsset:
        def __init__(self, next_date):
            self.NextMaintenanceDate = next_date

    assets = [
        TestAsset(None),
        TestAsset(date(2026, 10, 1)),
    ]

    result = get_maintenance_due_soon(
        assets,
        days=30
    )

    assert len(result) == 0