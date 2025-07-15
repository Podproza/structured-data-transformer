import hashlib
import os
import secrets
from typing import Optional

import base58
from faker import Faker

faker = Faker()


def generate_p2sh_address() -> str:
    redeem_script_hash = os.urandom(20)
    prefix = b"\x05"
    payload = prefix + redeem_script_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address_bytes = payload + checksum
    return base58.b58encode(address_bytes).decode()


def generate_fake_txid() -> str:
    return secrets.token_bytes(32).hex()


def fake_p2sh_address(_: Optional[str]) -> str:
    return generate_p2sh_address()


def fake_transaction_id(_: Optional[str]) -> str:
    return generate_fake_txid()


def fake_email(_: Optional[str]) -> str:
    return faker.email()


def fake_company(_: Optional[str]) -> str:
    return faker.company()
