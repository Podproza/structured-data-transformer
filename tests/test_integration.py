import json
import shutil
from pathlib import Path

import pytest

from structured_data_transformer.config.loader import load_transform_configs_from_file
from structured_data_transformer.config.transform_config import (
    wrap_configs_with_stable_anonymizer,
)
from structured_data_transformer.executor import apply_transforms

THIS_DIR = Path(__file__).parent
PROJECT_ROOT = THIS_DIR.parent


@pytest.fixture(scope="module")
def sample_data():
    base = PROJECT_ROOT / "examples/simple"
    return {
        "input": base / "input",
        "output": base / "output",
        "config": base / "config.json",
        "key": base / "key.json",
    }


@pytest.fixture
def temp_copy(tmp_path: Path):
    def _copy(source: Path, dest_name: str) -> Path:
        dest = tmp_path / dest_name
        shutil.copytree(source, dest)
        return dest

    return _copy


def compare_dirs(dir1: Path, dir2: Path):
    files1 = sorted([p.relative_to(dir1) for p in dir1.rglob("*") if p.is_file()])
    files2 = sorted([p.relative_to(dir2) for p in dir2.rglob("*") if p.is_file()])

    assert files1 == files2, f"File lists do not match:\n{files1}\n!=\n{files2}"

    for rel in files1:
        f1 = dir1 / rel
        f2 = dir2 / rel
        assert f2.exists(), f"{f2} missing"
        assert f1.read_text() == f2.read_text(), f"Content mismatch for {rel}"


def test_forward_transformation(sample_data, temp_copy):
    input_dir = sample_data["input"]
    expected_output_dir = sample_data["output"]
    config_file = sample_data["config"]
    key_file = sample_data["key"]

    working_dir = temp_copy(input_dir, "forward")
    key_data = json.loads(key_file.read_text())

    configs = load_transform_configs_from_file(config_file)
    wrapped_configs = wrap_configs_with_stable_anonymizer(configs, key_data)

    apply_transforms(configs=wrapped_configs, base_dir=working_dir)

    compare_dirs(working_dir, expected_output_dir)


def test_reverse_transformation(sample_data, temp_copy):
    output_dir = sample_data["output"]
    expected_input_dir = sample_data["input"]
    config_file = sample_data["config"]
    key_file = sample_data["key"]

    working_dir = temp_copy(output_dir, "reverse")
    key_data = json.loads(key_file.read_text())
    reversed_key = {v: k for k, v in key_data.items()}

    configs = load_transform_configs_from_file(config_file)
    wrapped_configs = wrap_configs_with_stable_anonymizer(configs, reversed_key)

    apply_transforms(configs=wrapped_configs, base_dir=working_dir)

    compare_dirs(working_dir, expected_input_dir)
