Uses only Python’s standard library. `csv` handles quoted commas and Unicode; `Decimal` keeps monetary sums exact.

```python
import csv
import io
from decimal import Decimal


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts from CSV text with 'category' and 'amount' headers.

    Amounts must be numeric strings, such as 12.50 or -3.25.
    Category names are preserved exactly.
    """
    reader = csv.DictReader(io.StringIO(csv_text, newline=""))

    if not {"category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV must contain 'category' and 'amount' columns")

    totals: dict[str, Decimal] = {}
    for row in reader:
        category = row["category"]
        amount = Decimal(row["amount"])
        totals[category] = totals.get(category, Decimal("0")) + amount

    return totals
```

Example:

```python
text = '''category,amount
"Food, drinks",12.50
交通,3.20
"Food, drinks",7.50
交通,1.80
'''

print(sum_by_category(text))
# {'Food, drinks': Decimal('20.00'), '交通': Decimal('5.00')}
```
