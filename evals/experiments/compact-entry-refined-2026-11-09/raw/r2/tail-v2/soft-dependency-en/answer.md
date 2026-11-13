```python
import csv
import io
from decimal import Decimal


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts from CSV text with 'category' and 'amount' headers.

    Handles quoted commas and Unicode category names. Uses Decimal for
    exact decimal arithmetic and preserves category names as written.
    """
    totals: dict[str, Decimal] = {}

    for row in csv.DictReader(io.StringIO(csv_text, newline="")):
        category = row["category"]
        amount = Decimal(row["amount"].strip())
        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```

Example:

```python
text = '''category,amount
"Food, dining",12.50
旅行,100.00
"Food, dining",7.25
'''

print(sum_amounts_by_category(text))
# {'Food, dining': Decimal('19.75'), '旅行': Decimal('100.00')}
```
