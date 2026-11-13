```python
import csv
import io
from decimal import Decimal, InvalidOperation


def sum_by_category(csv_text: str) -> dict[str, Decimal]:
    """Sum CSV amounts by category.

    Requires 'category' and 'amount' headers. Extra columns are allowed.
    Category names are preserved exactly. Empty input returns {}.
    Invalid rows or non-finite amounts raise ValueError.
    """
    reader = csv.DictReader(io.StringIO(csv_text, newline=""), strict=True)
    totals: dict[str, Decimal] = {}

    try:
        if reader.fieldnames is None:
            return totals
        if not {"category", "amount"}.issubset(reader.fieldnames):
            raise ValueError("CSV must include 'category' and 'amount' headers.")

        for row in reader:
            category = row.get("category")
            raw_amount = row.get("amount")
            if None in row or category is None or raw_amount is None:
                raise ValueError(f"Malformed row at line {reader.line_num}.")

            try:
                amount = Decimal(raw_amount.strip())
            except InvalidOperation as exc:
                raise ValueError(
                    f"Invalid amount at line {reader.line_num}: {raw_amount!r}"
                ) from exc

            if not amount.is_finite():
                raise ValueError(f"Non-finite amount at line {reader.line_num}.")

            totals[category] = totals.get(category, Decimal("0")) + amount

    except csv.Error as exc:
        raise ValueError(f"Invalid CSV at line {reader.line_num}: {exc}") from exc

    return totals
```

Uses only the standard library. `Decimal` avoids binary floating-point rounding for typical monetary amounts.

```python
text = '''category,amount
"Café, snacks",12.50
交通,3.25
"Café, snacks",2.00
'''

print(sum_by_category(text))
# {'Café, snacks': Decimal('14.50'), '交通': Decimal('3.25')}
```
