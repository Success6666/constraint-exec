import csv
import io

SENTINEL = "user edit: keep me"


def summarize(text):
    totals = {}
    for row in csv.DictReader(io.StringIO(text)):
        category = row.get("category")
        amount = row.get("amount")
        if not category or not category.strip() or not amount:
            continue
        try:
            value = float(amount)
        except ValueError:
            continue
        totals[category] = totals.get(category, 0) + value
    return totals
