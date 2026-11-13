Uses only Python’s standard library. Expects `category` and `amount` headers; `Decimal` keeps monetary arithmetic exact.

```python
import csv
import io
from decimal import Decimal


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts by category from CSV text with category,amount headers."""
    reader = csv.DictReader(io.StringIO(csv_text, newline=""))

    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' headers")

    totals: dict[str, Decimal] = {}
    for row in reader:
        category = row["category"]
        amount = Decimal(row["amount"].strip())
        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```

Example, including a quoted comma and Unicode:

```python
text = '''category,amount
"Food, dining",12.50
旅行,100.00
"Food, dining",7.25
'''

print(sum_by_category(text))
# {'Food, dining': Decimal('19.75'), '旅行': Decimal('100.00')}
```
