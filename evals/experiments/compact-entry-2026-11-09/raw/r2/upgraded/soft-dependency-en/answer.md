```python
import csv
import io
from decimal import Decimal, InvalidOperation


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum CSV columns 'category' and 'amount', returning exact decimal totals.

    Handles quoted commas and Unicode names. Raises ValueError for missing
    required columns, missing values, or invalid/non-finite amounts.
    """
    reader = csv.DictReader(io.StringIO(csv_text, newline=""), strict=True)
    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must include 'category' and 'amount' columns.")

    totals: dict[str, Decimal] = {}
    for row in reader:
        category = row["category"]
        raw_amount = row["amount"]
        if category is None or raw_amount is None:
            raise ValueError(f"Missing value near line {reader.line_num}.")

        try:
            amount = Decimal(raw_amount.strip())
        except InvalidOperation as exc:
            raise ValueError(
                f"Invalid amount near line {reader.line_num}: {raw_amount!r}"
            ) from exc
        if not amount.is_finite():
            raise ValueError(f"Non-finite amount near line {reader.line_num}.")

        totals[category] = totals.get(category, Decimal(0)) + amount

    return totals
```

Example:

```python
text = '''category,amount
"Café, snacks",12.50
交通,3.25
"Café, snacks",2.00
'''

assert sum_amounts_by_category(text) == {
    "Café, snacks": Decimal("14.50"),
    "交通": Decimal("3.25"),
}
```
