from typing import Any, Optional

from structured_data_transformer.models import TransformFunc
from structured_data_transformer.transforms.anonymizers import (
    fake_p2sh_address,
    fake_transaction_id,
    fake_email,
    fake_company,
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
    "fake_company": fake_company,
}


def register_transform(transform: TransformFunc, name: str) -> None:
    TRANSFORM_FUNCTION_MAP[name] = transform


def resolve_transforms(
    transforms: dict[str, str],
    transform_function_map: Optional[dict[str, TransformFunc]] = None,
) -> dict[str, TransformFunc]:
    transform_function_map = transform_function_map or TRANSFORM_FUNCTION_MAP
    return {
        pattern: transform_function_map[name] for pattern, name in transforms.items()
    }
