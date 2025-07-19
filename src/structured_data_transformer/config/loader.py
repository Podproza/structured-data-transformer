import json
from pathlib import Path
from typing import Literal, Union

from pydantic import BaseModel, TypeAdapter

from structured_data_transformer.config.transform_config import (
    FilenameTransformConfig,
    JsonTransformConfig,
    CsvTransformConfig,
    TransformConfig,
)
from structured_data_transformer.transforms import resolve_transforms


class LoaderBaseModel(BaseModel):
    adapter: str
    glob: list[str]
    transforms: dict[str, str]

    def transform_config_class(self) -> type[TransformConfig]:
        raise NotImplementedError()

    def to_runtime(self) -> TransformConfig:
        return self.transform_config_class()(
            glob=self.glob, transforms=resolve_transforms(self.transforms)
        )


class FilenameLoaderModel(LoaderBaseModel):
    adapter: Literal["filename"]

    def transform_config_class(self):
        return FilenameTransformConfig


class JsonLoaderModel(LoaderBaseModel):
    adapter: Literal["json"]

    def transform_config_class(self):
        return JsonTransformConfig


class CsvLoaderModel(LoaderBaseModel):
    adapter: Literal["csv"]

    def transform_config_class(self):
        return CsvTransformConfig


AllLoaderModels = Union[
    FilenameLoaderModel,
    JsonLoaderModel,
    CsvLoaderModel,
]


def loader_models_to_runtime_configs(
    loader_models: list[LoaderBaseModel],
) -> list[TransformConfig]:
    return [model.to_runtime() for model in loader_models]


def load_transform_configs_from_file(
    path: Path, encoding: str = "utf-8"
) -> list[TransformConfig]:
    content = path.read_text(encoding=encoding)
    raw_configs = json.loads(content)

    loader_models: list[LoaderBaseModel] = [
        TypeAdapter(AllLoaderModels).validate_python(cfg) for cfg in raw_configs
    ]

    return [model.to_runtime() for model in loader_models]
