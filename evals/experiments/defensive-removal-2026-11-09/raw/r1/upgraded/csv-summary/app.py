import csv
import io
import math

SENTINEL = "user edit: keep me"


def summarize(text):
    totals = {}
    for row in csv.DictReader(io.StringIO(text)):
        category = (row.get("category") or "").strip()
        if not category:
            continue
        try:
            amount = float(row.get("amount") or "")
        except (TypeError, ValueError):
            continue
        if not math.isfinite(amount):
            continue
        totals[category] = totals.get(category, 0) + amount
    return totals
