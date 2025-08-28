from typing import Any

import pytest

from structured_data_transformer.btc_json_sanitizer import BTCSanitizer


@pytest.fixture(autouse=True)
def patch_fakes(monkeypatch):
    monkeypatch.setattr(
        "structured_data_transformer.btc_json_sanitizer.fake_p2sh_address",
        lambda _: "A",
    )
    monkeypatch.setattr(
        "structured_data_transformer.btc_json_sanitizer.fake_transaction_id",
        lambda _: "T",
    )


def test_sanitize_keys_and_values():
    addr = "1BoatSLRHtKNngkdXEeobR76b53LETtpyT"
    tx = "4e9b7b60ffb9e2c3a56492e7985c3a4f35692b95d3fa7bb5db83d4d1c09e2b88"

    data = {addr: {"tx": tx, addr: tx}}

    sanitizer = BTCSanitizer()
    sanitized = sanitizer.sanitize_json(data)

    assert "A" in sanitized
    assert sanitized["A"]["tx"] == "T"
    assert "A" in sanitized["A"]
    assert sanitized["A"]["A"] == "T"


def test_full_sample_input():
    input_data = {
        "tx_inputs_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68": [
                "4c3252709a93816e41b7c5ca24f7659c30cfe8d5550e79e244d04ad1d90a3550_0"
            ]
        },
        "output_value_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68_0": 16524,
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68_1": 1687916,
        },
        "output_script_type_data": {},
        "block_height_txs_data": {},
        "last_processed_block_data": None,
        "tx_locktime_data": {},
        "tx_block_height_data": {},
        "tx_exists_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68": True
        },
        "address_exists_data": {},
        "tx_input_count_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68": 1,
            "cb44e442f0e6d03c290753e3d1a67a041acff947aa465a5509dbf538a5b8e12d": 2,
        },
        "output_next_tx_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68_1": [
                "cb44e442f0e6d03c290753e3d1a67a041acff947aa465a5509dbf538a5b8e12d"
            ]
        },
        "tx_mined_timestamp_data": {},
        "address_outputs_data": {
            "bc1qg9ejedy5g508l9ht086wya0r3w5jhe7dzg7dc2fcnm942202j26sey8scr": [
                "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68_1"
            ]
        },
        "tx_vsize_data": {},
        "output_address_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68_0": "bc1qrkzh9qwst7fs2w4gcg9krdjq2mh7jdrc3el3e5",
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68_1": "bc1qg9ejedy5g508l9ht086wya0r3w5jhe7dzg7dc2fcnm942202j26sey8scr",
            "4c3252709a93816e41b7c5ca24f7659c30cfe8d5550e79e244d04ad1d90a3550_0": "3QsrMnAx2vsQGin4F7PMqygam2ZXHoVWmk",
        },
        "output_exists_data": {},
        "tx_output_count_data": {
            "3773010ff2b1b10f9bcb6529b77b4a842985e745a4ffd22c76e99ba6ab42fa68": 2,
            "cb44e442f0e6d03c290753e3d1a67a041acff947aa465a5509dbf538a5b8e12d": 2,
        },
    }

    sanitizer = BTCSanitizer()
    sanitized = sanitizer.sanitize_json(input_data)

    def check_no_originals(d: Any):
        if isinstance(d, dict):
            for k, v in d.items():
                for forbidden in ["3773010f", "cb44e442", "4c325270", "bc1q"]:
                    assert forbidden not in k
                check_no_originals(v)
        elif isinstance(d, list):
            for i in d:
                check_no_originals(i)
        elif isinstance(d, str):
            for forbidden in ["3773010f", "cb44e442", "4c325270", "bc1q"]:
                assert forbidden not in d

    check_no_originals(sanitized)
