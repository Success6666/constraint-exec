Uses only the standard library. Expects `category` and `amount` columns and returns `Decimal` totals to avoid binary floating-point rounding.

```python
import csv
import io
from decimal import Decimal, InvalidOperation


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts by category, preserving category names exactly."""
    reader = csv.DictReader(io.StringIO(csv_text, newline=""))

    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' columns")

    totals: dict[str, Decimal] = {}

    for row in reader:
        category = row["category"]
        amount_text = row["amount"]

        if category is None or amount_text is None:
            raise ValueError(f"Missing value near CSV line {reader.line_num}")

        try:
            amount = Decimal(amount_text.strip())
        except InvalidOperation as exc:
            raise ValueError(
                f"Invalid amount near CSV line {reader.line_num}: {amount_text!r}"
            ) from exc

        if not amount.is_finite():
            raise ValueError(
                f"Amount must be finite near CSV line {reader.line_num}"
            )

        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```

```python
text = '''category,amount
"Food, dining",12.50
旅行,100.00
"Food, dining",7.25
旅行,-20.00
'''

print(sum_by_category(text))
# {'Food, dining': Decimal('19.75'), '旅行': Decimal('80.00')}
```
