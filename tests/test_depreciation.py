from datetime import date
from decimal import Decimal

from app.utils.depreciation import calculate_depreciation


def test_purchase_in_mid_month():
    result = calculate_depreciation(
        purchase_price=12000,
        useful_life_months=12,
        salvage_value=1200,
        purchase_date=date(2026, 8, 15),
        current_date=date(2026, 9, 15),
    )

    assert result["monthly_depreciation"] == Decimal("900.00")
    assert result["book_value"] == Decimal("11100.00")


def test_book_value_does_not_go_below_salvage_value():
    result = calculate_depreciation(
        purchase_price=12000,
        useful_life_months=12,
        salvage_value=1200,
        purchase_date=date(2025, 1, 1),
        current_date=date(2027, 1, 1),
    )

    assert result["book_value"] == Decimal("1200.00")


def test_zero_purchase_price():
    result = calculate_depreciation(
        purchase_price=0,
        useful_life_months=12,
        salvage_value=0,
        purchase_date=date(2026, 1, 1),
        current_date=date(2026, 8, 1),
    )

    assert result["monthly_depreciation"] == Decimal("0.00")
    assert result["book_value"] == Decimal("0.00")


def test_zero_useful_life():
    result = calculate_depreciation(
        purchase_price=12000,
        useful_life_months=0,
        salvage_value=1200,
        purchase_date=date(2026, 1, 1),
        current_date=date(2026, 8, 1),
    )

    assert result["monthly_depreciation"] == Decimal("0.00")
    assert result["book_value"] == Decimal("12000.00")


def test_future_purchase_date():
    result = calculate_depreciation(
        purchase_price=12000,
        useful_life_months=12,
        salvage_value=1200,
        purchase_date=date(2026, 12, 1),
        current_date=date(2026, 8, 1),
    )

    assert result["monthly_depreciation"] == Decimal("0.00")
    assert result["book_value"] == Decimal("12000.00")