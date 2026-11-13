Uses Python’s standard library and `Decimal` for monetary amounts. The CSV must have `category` and `amount` headers.

```python
import csv
from decimal import Decimal
from io import StringIO


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts by category, supporting CSV quoting and Unicode names."""
    reader = csv.DictReader(StringIO(csv_text, newline=""))

    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' headers")

    totals: dict[str, Decimal] = {}
    for row in reader:
        category = row["category"]
        amount = Decimal(row["amount"].strip())
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

print(sum_by_category(text))
# {'Café, snacks': Decimal('14.75'), '交通': Decimal('8.00')}
```
