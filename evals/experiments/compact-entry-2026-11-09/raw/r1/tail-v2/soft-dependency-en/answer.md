Uses only Python’s standard library. Expects headers named `category` and `amount`; returns `Decimal` totals for exact decimal arithmetic.

```python
import csv
import io
from decimal import Decimal


def sum_amounts_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts by category, supporting CSV quoting and Unicode names."""
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
"Food, groceries",12.50
旅行,100.00
"Food, groceries",7.25
旅行,-10.00
'''

print(sum_amounts_by_category(text))
# {'Food, groceries': Decimal('19.75'), '旅行': Decimal('90.00')}
```
