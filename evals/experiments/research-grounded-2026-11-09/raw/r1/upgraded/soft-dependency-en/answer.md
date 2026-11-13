```python
import csv
import io
from decimal import Decimal


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts from CSV text with 'category' and 'amount' headers.

    Supports quoted commas and Unicode category names. Uses Decimal to
    avoid binary floating-point rounding errors.
    """
    reader = csv.DictReader(io.StringIO(csv_text, newline=""))
    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' headers.")

    totals: dict[str, Decimal] = {}
    for row in reader:
        category = row["category"]
        amount = Decimal(row["amount"])
        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```
