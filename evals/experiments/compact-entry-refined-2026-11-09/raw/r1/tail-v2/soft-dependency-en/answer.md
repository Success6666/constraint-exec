```python
import csv
import io
from decimal import Decimal


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum CSV amounts by category.

    Expects a header with 'category' and 'amount' columns.
    Supports quoted commas and Unicode names. Uses Decimal for exact
    decimal arithmetic.
    """
    totals: dict[str, Decimal] = {}

    with io.StringIO(csv_text, newline="") as stream:
        for row in csv.DictReader(stream):
            category = row["category"]
            amount = Decimal(row["amount"].strip())
            totals[category] = totals.get(category, Decimal(0)) + amount

    return totals
```

Example (standard library only):

```python
text = '''category,amount
"Food, dining",12.50
交通,3.25
"Food, dining",7.50
交通,2.75
'''

print(sum_by_category(text))
# {'Food, dining': Decimal('20.00'), '交通': Decimal('6.00')}
```
