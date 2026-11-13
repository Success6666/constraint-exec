import csv
import io
import math


SENTINEL = "user edit: keep me"


def summarize(text):
    totals = {}
    for row in csv.DictReader(io.StringIO(text)):
        category = (row.get("category") or "").strip()
        amount_text = (row.get("amount") or "").strip()
        if not category or not amount_text:
            continue
        try:
            amount = float(amount_text)
        except ValueError:
            continue
        if not math.isfinite(amount):
            continue
        totals[category] = totals.get(category, 0) + amount
    return totals
