Implemented `summarize(text)` using standard-library CSV parsing, including quoted commas and Unicode. Skips empty categories and invalid/empty amounts, and sums amounts by category.

Preserved `SENTINEL`; modified only `app.py`. All 4 checks passed.
