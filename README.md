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

Example help:

```bash
usage: sdt [-h] --config CONFIG --base-dir BASE_DIR [--cache-in CACHE_IN] [--cache-out CACHE_OUT] [--reverse-cache]
```

## Examples

There is examples folder containing sample input, output, config and key.json.

Anonymize:

```bash
sdt -c examples/simple/config.json -d examples/simple/input -ci examples/simple/key.json

```
Anonymize using existing key:

```bash
sdt -c examples/simple/config.json -d examples/simple/input -ci examples/simple/key.json
```

Reverse:

```bash
sdt -c examples/simple/config.json -d examples/simple/output -r -ci examples/simple/key.json
```

## 


## What it does

- Anonymizes fields in JSON, CSV, and filenames with pattern rules.
- Handles Bitcoin transactions, addresses, company names, emails, etc.
- Keeps empty values unchanged.
- Maintains a stable mapping so each value is always replaced the same way.
- Saves the key for reuse so data can be deanonymized with `--reverse-cache`.

