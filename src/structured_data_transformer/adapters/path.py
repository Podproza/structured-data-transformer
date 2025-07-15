import re
from pathlib import Path

from structured_data_transformer.models import TransformFunc


def transform_path(
    input_path: Path, output_path: Path, transforms: dict[str, TransformFunc]
) -> Path:
    name = input_path.name
    for pattern, transform in transforms.items():
        match = re.search(pattern, name)
        if match:
            original = match.group(1)
            new_value = transform(original)
            new_name = re.sub(pattern, new_value, name)
            return output_path.with_name(new_name)
    return output_path
