import json
from pathlib import Path

from structured_data_transformer.config.loader import (
    FilenameLoaderModel,
    JsonLoaderModel,
    CsvLoaderModel,
    loader_models_to_runtime_configs,
    load_transform_configs_from_file,
)
from structured_data_transformer.config.transform_config import TransformConfig
from structured_data_transformer.transforms import TRANSFORM_FUNCTION_MAP


def test_filename_loader_model_to_runtime():
    loader = FilenameLoaderModel(
        adapter="filename",
        glob=["*.json"],
        transforms={"pattern": "fake_transaction_id"},
    )
    config = loader.to_runtime()

    assert isinstance(config, TransformConfig)
    assert callable(config.transforms["pattern"])
    assert config.transforms["pattern"] == TRANSFORM_FUNCTION_MAP["fake_transaction_id"]


def test_json_loader_model_to_runtime():
    loader = JsonLoaderModel(
        adapter="json",
        glob=["*.json"],
        transforms={"$.hash": "fake_transaction_id"},
    )
    config = loader.to_runtime()

    assert isinstance(config, TransformConfig)
    assert callable(config.transforms["$.hash"])
    assert config.transforms["$.hash"] == TRANSFORM_FUNCTION_MAP["fake_transaction_id"]


def test_csv_loader_model_to_runtime():
    loader = CsvLoaderModel(
        adapter="csv",
        glob=["*.csv"],
        transforms={"entity": "fake_company"},
    )
    config = loader.to_runtime()

    assert isinstance(config, TransformConfig)
    assert callable(config.transforms["entity"])
    assert config.transforms["entity"] == TRANSFORM_FUNCTION_MAP["fake_company"]


def test_loader_models_to_runtime_configs():
    loaders = [
        FilenameLoaderModel(
            adapter="filename",
            glob=["*.json"],
            transforms={"pattern": "fake_transaction_id"},
        ),
        CsvLoaderModel(
            adapter="csv",
            glob=["*.csv"],
            transforms={"entity": "fake_company"},
        ),
    ]

    runtime_configs = loader_models_to_runtime_configs(loaders)

    assert len(runtime_configs) == 2
    for cfg in runtime_configs:
        assert isinstance(cfg, TransformConfig)
        for func in cfg.transforms.values():
            assert callable(func)


def test_load_transform_configs_from_file(tmp_path: Path):
    config_data = [
        {
            "adapter": "filename",
            "glob": ["files/*.json"],
            "transforms": {r"([^/\\]+)(?=\.json$)": "fake_transaction_id"},
        },
        {
            "adapter": "json",
            "glob": ["files/*.json"],
            "transforms": {
                "$.hash": "fake_transaction_id",
                "$.address": "fake_p2sh_address",
            },
        },
        {
            "adapter": "csv",
            "glob": ["files/*.csv"],
            "transforms": {"entity": "fake_company"},
        },
    ]

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data, indent=2))

    configs = load_transform_configs_from_file(config_file)

    assert len(configs) == 3
    for config in configs:
        assert isinstance(config, TransformConfig)
        for func in config.transforms.values():
            assert callable(func)
