import csv
import io
from decimal import Decimal, InvalidOperation

SENTINEL = "user edit: keep me"


def summarize(text):
    totals = {}
    for row in csv.DictReader(io.StringIO(text)):
        category = (row.get("category") or "").strip()
        amount = (row.get("amount") or "").strip()
        if not category or not amount:
            continue
        try:
            value = Decimal(amount)
        except InvalidOperation:
            continue
        if not value.is_finite():
            continue
        totals[category] = totals.get(category, Decimal(0)) + value
    return totals
