import json
from pathlib import Path
from typing import Union, Any

import jsonpath_ng

from structured_data_transformer.types import TransformFunc

JSONType = Union[dict[str, Any], list[Any]]


class NoMatchError(Exception):
    pass


def transform_json(data: JSONType, transforms: dict[str, TransformFunc]) -> None:
    if not data:
        return
    for jsonpath, transform in transforms.items():
        _apply_transformation(data, jsonpath, transform)


def _apply_transformation(
    data: JSONType, jsonpath: str, transform: TransformFunc
) -> None:
    expr = jsonpath_ng.parse(jsonpath)
    matches = expr.find(data)
    for match in matches:
        new_value = transform(match.value)
        match.full_path.update(data, new_value)


def transform_json_file(path: Path, encoding: str, transform: dict[str, Any]) -> None:
    with path.open("r", encoding=encoding) as f:
        data: Any = json.load(f)
    transform_json(data, transform)
    with path.open("w", encoding=encoding) as f:
        json.dump(data, f, indent=2)
