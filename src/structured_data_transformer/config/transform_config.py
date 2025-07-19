import shutil
from dataclasses import dataclass
from pathlib import Path

from structured_data_transformer.adapters.csv import transform_csv_file
from structured_data_transformer.adapters.json import transform_json_file
from structured_data_transformer.adapters.path import transform_path
from structured_data_transformer.types import TransformFunc
from structured_data_transformer.transforms import (
    StableAnonymizer,
    SkipEmptyStringTransform,
)


@dataclass
class TransformConfig:
    glob: list[str]
    transforms: dict[str, TransformFunc]

    def apply(self, filepath: Path, encoding: str):
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__.replace('TransformConfig', '')}{self.glob}"


@dataclass
class FilenameTransformConfig(TransformConfig):
    def apply(self, filepath: Path, encoding: str):
        renamed_output = transform_path(filepath, filepath, self.transforms)
        renamed_output.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(filepath), str(renamed_output))


@dataclass
class JsonTransformConfig(TransformConfig):
    def apply(self, filepath: Path, encoding: str):
        if filepath.is_file() and filepath.suffix == ".json":
            transform_json_file(filepath, encoding, self.transforms)


@dataclass
class CsvTransformConfig(TransformConfig):
    def apply(self, filepath: Path, encoding: str):
        if filepath.is_file() and filepath.suffix == ".csv":
            transform_csv_file(filepath, encoding, self.transforms)


def wrap_configs_with_stable_anonymizer(
    configs: list[TransformConfig],
    key_cache: dict[str, str],
) -> list[TransformConfig]:
    """
    Transform configs with stable anonymization - same fields will be transformed to the same value.
    It will also not transform values that are empty strings.
    """
    for config in configs:
        wrapped_transforms = {
            path: SkipEmptyStringTransform(StableAnonymizer(func, cache=key_cache))
            for path, func in config.transforms.items()
        }
        config.transforms = wrapped_transforms
    return configs
