# Structured Data Transformer

Anonymize sensitive fields in JSON, CSV, and filenames — with stable mappings for reversible anonymization.

---

## Installation

```bash
pip install .
```

Or for development:

```bash
pip install -e '.[dev]'
```

---

## Usage (CLI)

```bash
sdt --config CONFIG --base-dir BASE_DIR
```

Usage help:

```bash
sdt -h
```

Output:

```bash
usage: sdt [-h] --config CONFIG --base-dir BASE_DIR [--cache-in CACHE_IN] [--cache-out CACHE_OUT] [--reverse-cache]

Apply structured data transforms in place.

options:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to the JSON config file to load.
  --base-dir BASE_DIR, -d BASE_DIR
                        Base directory containing the data to transform in place.
  --cache-in CACHE_IN, -ci CACHE_IN
                        Optional path to input JSON cache file for stable anonymizer.
  --cache-out CACHE_OUT, -co CACHE_OUT
                        Optional path to output JSON cache file for stable anonymizer.
  --reverse-cache, -r   Reverse keys and values in the input cache (for decoding instead of encoding).
```

## Examples

There is [examples](examples/simple) folder containing simple input, output, config and key.json.

Anonymize:

```bash
sdt --config examples/simple/config.json --base-dir examples/simple/input

```
Anonymize using existing key:

```bash
sdt -c examples/simple/config.json -d examples/simple/input -ci examples/simple/key.json
```

Reverse:

```bash
sdt -c examples/simple/config.json -d examples/simple/output -r -ci examples/simple/key.json
```

## What it does

- Anonymizes fields in JSON, CSV, and filenames with pattern rules.
- Handles Bitcoin transactions, addresses, company names, emails, etc.
- Keeps empty values unchanged.
- Maintains a stable mapping so each value is always replaced the same way.
- Saves the key for reuse so data can be deanonymized with `--reverse-cache`.

## Customization

### Custom transforms

You can add your own transform function. It doesn't necessarily need to anonymize, it can transform the field to any kind of form.
Transform function expected input and output is `Optional[str | int | float | bool]` (Json primitives).
Only `str` can happen for csv/path adapters.

To register the transform function, use `register_transform(func: callable, name: str)` 

Example custom transform can be `uppercase`:

```python
from typing import Optional
from structured_data_transformer.transforms import register_transform
from structured_data_transformer.types import JSONPrimitive


def uppercase(value: Optional[JSONPrimitive]) -> Optional[JSONPrimitive]:
    if value:
        return str(value).upper()
    return value


register_transform(uppercase, "uppercase")
```

