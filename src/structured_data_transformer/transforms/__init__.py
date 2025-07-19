from typing import Any

from structured_data_transformer.types import TransformFunc
from structured_data_transformer.transforms.anonymizers import (
    fake_p2sh_address,
    fake_transaction_id,
    fake_email,
    fake_company,
    fake_hostname,
    fake_name,
    fake_full_name,
)


class StableAnonymizer:
    def __init__(self, func: TransformFunc, cache: dict[Any, Any]) -> None:
        self.func = func
        if cache is None:
            raise ValueError("Cache must be a non-empty dictionary")
        self.cache = cache

    def __call__(self, value: Any) -> Any:
        if value in self.cache:
            return self.cache[value]
        new_value = self.func(value)
        self.cache[value] = new_value
        return new_value


class SkipEmptyStringTransform:
    def __init__(self, func: TransformFunc):
        self.func = func

    def __call__(self, value: Any) -> Any:
        if value == "":
            return value
        return self.func(value)


TRANSFORM_FUNCTION_MAP: dict[str, TransformFunc] = {
    "fake_p2sh_address": fake_p2sh_address,
    "fake_transaction_id": fake_transaction_id,
    "fake_email": fake_email,
    "fake_hostname": fake_hostname,
    "fake_company": fake_company,
    "fake_name": fake_name,
    "fake_full_name": fake_full_name,
}


def register_transform(transform: TransformFunc, name: str) -> None:
    TRANSFORM_FUNCTION_MAP[name] = transform


def resolve_transforms(
    transforms: dict[str, str],
    transform_function_map: dict[str, TransformFunc],
) -> dict[str, TransformFunc]:
    return {
        pattern: transform_function_map[name] for pattern, name in transforms.items()
    }
