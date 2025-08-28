import json
import re
from typing import Any

from structured_data_transformer.transforms.anonymizers import (
    fake_p2sh_address,
    fake_transaction_id,
)

from pathlib import Path

TXOUT_SEPARATOR = "_"


def sanitize_string_(value: str, cache: dict[str, str], separator: str = "_") -> str:
    addr_pattern = r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[0-9a-z]{39,59})\b"
    txid_pattern = r"\b[0-9a-fA-F]{64}\b"
    outref_pattern = rf"\b(?P<txid>[0-9a-fA-F]{{64}}){separator}(?P<index>[0-9]+)\b"

    for match in re.findall(addr_pattern, value):
        if match not in cache:
            cache[match] = fake_p2sh_address(None)
        value = value.replace(match, cache[match])

    for match in re.findall(txid_pattern, value):
        if match not in cache:
            cache[match] = fake_transaction_id(None)
        value = value.replace(match, cache[match])

    for match in re.finditer(outref_pattern, value):
        orig_txid = match.group("txid")
        index = match.group("index")
        fake_txid = cache.get(orig_txid)
        if not fake_txid:
            fake_txid = fake_transaction_id(None)
            cache[orig_txid] = fake_txid
        fake_ref = f"{fake_txid}{separator}{index}"
        orig_ref = match.group(0)
        cache[orig_ref] = fake_ref
        value = value.replace(orig_ref, fake_ref)

    return value


def sanitize_string(value: str, cache: dict[str, str], separator: str = "_") -> str:
    addr_pattern = r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[0-9a-z]{39,59})\b"
    txid_pattern = r"\b[0-9a-fA-F]{64}\b"
    outref_pattern = rf"\b(?P<txid>[0-9a-fA-F]{{64}}){separator}(?P<index>[0-9]+)\b"

    for match in re.findall(addr_pattern, value):
        if match not in cache:
            cache[match] = fake_p2sh_address(None)
        value = value.replace(match, cache[match])

    for match in re.finditer(outref_pattern, value):
        orig_txid = match.group("txid")
        index = match.group("index")
        fake_txid = cache.get(orig_txid)
        if not fake_txid:
            fake_txid = fake_transaction_id(None)
            cache[orig_txid] = fake_txid
        fake_ref = f"{fake_txid}{separator}{index}"
        orig_ref = match.group(0)
        cache[orig_ref] = fake_ref
        value = value.replace(orig_ref, fake_ref)

    for match in re.findall(txid_pattern, value):
        if match not in cache:
            cache[match] = fake_transaction_id(None)
        value = value.replace(match, cache[match])

    return value


class BTCSanitizer:
    def __init__(self, cache: dict[str, str] | None = None, txout_separator: str = "_"):
        self.cache = cache or {}
        self.separator = txout_separator

    def sanitize_json(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                self._sanitize_string(k): self.sanitize_json(v) for k, v in data.items()
            }
        if isinstance(data, list):
            return [self.sanitize_json(item) for item in data]
        if isinstance(data, str):
            return self._sanitize_string(data)
        return data

    def _sanitize_string(self, value: str) -> str:
        return sanitize_string(value, self.cache, self.separator)

    def sanitize_file(self, input_path: str, output_path: str) -> None:
        with open(input_path, "r") as f:
            data = json.load(f)
        sanitized = self.sanitize_json(data)
        with open(output_path, "w") as f:
            json.dump(sanitized, f, indent=2)


def sanitize_all_json_files(path: Path) -> dict[str, str]:
    sanitizer = BTCSanitizer()
    for file in path.rglob("*.json"):
        with file.open("r") as f:
            data = json.load(f)
        sanitized = sanitizer.sanitize_json(data)
        with file.open("w") as f:
            json.dump(sanitized, f, indent=2)
    return sanitizer.cache


if __name__ == "__main__":
    path = Path("~/git/VIP-detection/tests/testresources/v2/snapshots/").expanduser()
    cache = sanitize_all_json_files(path)
    # write cache to cache.json:
    with open(path / "cache.json", "w") as f:
        json.dump(cache, f, indent=2)
