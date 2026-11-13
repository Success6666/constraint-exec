Save as `count_lines.py`:

```python
import argparse


def main():
    parser = argparse.ArgumentParser(description="Count non-empty lines in a UTF-8 file.")
    parser.add_argument("path", help="Path to the text file")
    args = parser.parse_args()

    with open(args.path, encoding="utf-8") as file:
        count = sum(1 for line in file if line.strip())

    print(count)


if __name__ == "__main__":
    main()
```

Whitespace-only lines are treated as empty.

Usage:
```sh
python count_lines.py input.txt
```
