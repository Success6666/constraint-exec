```python
import csv
import io
from decimal import Decimal


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum CSV amounts by category.

    Expects a header with 'category' and 'amount' columns.
    Supports quoted commas and Unicode category names.
    Uses Decimal for exact decimal arithmetic.
    """
    totals: dict[str, Decimal] = {}

    reader = csv.DictReader(io.StringIO(csv_text, newline=""))
    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' columns")

    for row in reader:
        category = row["category"]
        amount = Decimal(row["amount"])
        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```

Example:
```python
text = '''category,amount
"Café, snacks",12.50
交通,3.25
"Café, snacks",2.00
'''

print(sum_amounts_by_category(text))
# {'Café, snacks': Decimal('14.50'), '交通': Decimal('3.25')}
```
