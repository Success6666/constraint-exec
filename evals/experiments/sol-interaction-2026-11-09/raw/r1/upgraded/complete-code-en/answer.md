Save as `count_lines.py`. Whitespace-only lines are treated as empty.

```python
import argparse


def main():
    parser = argparse.ArgumentParser(description="Count non-empty lines in a UTF-8 file.")
    parser.add_argument("path", help="Path to the text file")
    args = parser.parse_args()

    try:
        with open(args.path, encoding="utf-8") as file:
            count = sum(1 for line in file if line.strip())
    except (OSError, UnicodeError) as error:
        parser.exit(1, f"Error: {error}\n")

    print(count)


if __name__ == "__main__":
    main()
```

Usage:

```sh
python count_lines.py input.txt
```
