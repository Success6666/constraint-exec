import csv
import io
from decimal import Decimal, InvalidOperation

SENTINEL = "user edit: keep me"


def summarize(text):
    totals = {}
    for row in csv.DictReader(io.StringIO(text)):
        category = row.get("category")
        amount = row.get("amount")
        if category is None or not category.strip() or amount is None:
            continue
        try:
            number = Decimal(amount.strip())
        except InvalidOperation:
            continue
        if not number.is_finite():
            continue
        totals[category] = totals.get(category, Decimal(0)) + number
    return totals
