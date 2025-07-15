from pathlib import Path
from typing import Iterator

from tqdm import tqdm

from structured_data_transformer.config.transform_config import (
    TransformConfig,
)


def apply_transforms(
    configs: list[TransformConfig], base_dir: Path, encoding: str = "utf-8"
) -> None:
    for config in configs:
        for filepath in tqdm(
            find_matching_files(config.glob, base_dir), desc=f"{config}"
        ):
            config.apply(filepath, encoding=encoding)


def find_matching_files(glob_patterns: list[str], base_dir: Path) -> Iterator[Path]:
    for pattern in glob_patterns:
        yield from base_dir.glob(pattern)
