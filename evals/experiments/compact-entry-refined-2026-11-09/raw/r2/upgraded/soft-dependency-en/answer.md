```python
import csv
import io
from decimal import Decimal


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum amounts from CSV text with 'category' and 'amount' headers.

    Supports quoted commas and Unicode names. Uses Decimal for exact
    decimal arithmetic. Invalid amounts or missing columns raise an error.
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
"Café, snacks",12.50
交通,3.25
"Café, snacks",2.10
'''

assert sum_by_category(text) == {
    "Café, snacks": Decimal("14.60"),
    "交通": Decimal("3.25"),
}
```

Uses only Python’s standard library.
