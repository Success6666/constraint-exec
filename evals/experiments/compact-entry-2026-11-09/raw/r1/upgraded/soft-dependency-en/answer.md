```python
import csv
import io
from decimal import Decimal


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts from CSV text with 'category' and 'amount' headers.

    Handles quoted commas and Unicode names. Uses Decimal for exact
    decimal arithmetic. Blank lines are ignored; invalid amounts raise
    ValueError. Category names are preserved exactly.
    """
    reader = csv.DictReader(io.StringIO(csv_text, newline=""))
    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' headers")

    totals: dict[str, Decimal] = {}

    for row in reader:
        category = row["category"]
        raw_amount = row["amount"]
        if category is None or raw_amount is None:
            raise ValueError(f"Missing field near CSV line {reader.line_num}")

        try:
            amount = Decimal(raw_amount.strip())
        except ArithmeticError as exc:
            raise ValueError(
                f"Invalid amount near CSV line {reader.line_num}: {raw_amount!r}"
            ) from exc

        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```
