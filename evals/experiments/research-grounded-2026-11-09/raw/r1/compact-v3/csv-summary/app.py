import csv
import io
from decimal import Decimal, InvalidOperation


SENTINEL = "user edit: keep me"


def summarize(text):
    totals = {}
    for row in csv.DictReader(io.StringIO(text)):
        category = row.get("category")
        amount = row.get("amount")
        if not category or not category.strip() or amount is None:
            continue
        try:
            value = Decimal(amount.strip())
        except InvalidOperation:
            continue
        if not value.is_finite():
            continue
        totals[category] = totals.get(category, Decimal(0)) + value
    return totals
