Uses Python’s standard library. Expects `category` and `amount` headers and returns exact decimal totals.

```python
import csv
import io
from decimal import Decimal


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum CSV amounts by category, supporting quoted fields and Unicode."""
    reader = csv.DictReader(io.StringIO(csv_text, newline=""))

    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' headers")

    totals: dict[str, Decimal] = {}

    for row in reader:
        category = row["category"]
        amount_text = row["amount"]
        if category is None or amount_text is None:
            raise ValueError("Each row must contain a category and amount")

        amount = Decimal(amount_text.strip())
        if not amount.is_finite():
            raise ValueError("Amounts must be finite numbers")

        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```

Example:

```python
text = '''category,amount
"Café, snacks",12.50
交通,8.00
"Café, snacks",2.25
'''

print(sum_amounts_by_category(text))
# {'Café, snacks': Decimal('14.75'), '交通': Decimal('8.00')}
```
