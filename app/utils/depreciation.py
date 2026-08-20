from datetime import date
from decimal import Decimal


def calculate_depreciation(
    purchase_price,
    useful_life_months,
    salvage_value,
    purchase_date,
    current_date=None,
):
    if current_date is None:
        current_date = date.today()

    purchase_price = Decimal(str(purchase_price or 0))
    salvage_value = Decimal(str(salvage_value or 0))

    if purchase_price <= 0:
        return {
            "monthly_depreciation": Decimal("0.00"),
            "book_value": salvage_value,
        }

    if useful_life_months is None or useful_life_months <= 0:
        return {
            "monthly_depreciation": Decimal("0.00"),
            "book_value": purchase_price,
        }

    if purchase_date > current_date:
        return {
            "monthly_depreciation": Decimal("0.00"),
            "book_value": purchase_price,
        }

    monthly_depreciation = (
        purchase_price - salvage_value
    ) / Decimal(useful_life_months)

    months_elapsed = (
        (current_date.year - purchase_date.year) * 12
        + current_date.month
        - purchase_date.month
    )

    months_elapsed = max(0, months_elapsed)
    months_elapsed = min(months_elapsed, useful_life_months)

    accumulated_depreciation = (
        monthly_depreciation * Decimal(months_elapsed)
    )

    book_value = purchase_price - accumulated_depreciation

    if book_value < salvage_value:
        book_value = salvage_value

    return {
        "monthly_depreciation": monthly_depreciation.quantize(
            Decimal("0.01")
        ),
        "book_value": book_value.quantize(
            Decimal("0.01")
        ),
    }