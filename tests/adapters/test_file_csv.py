import csv
from pathlib import Path
from faker import Faker

from structured_data_transformer.config.transform_config import (
    CsvTransformConfig,
    FilenameTransformConfig,
)
from structured_data_transformer.executor import apply_transforms
from structured_data_transformer.transforms import StableAnonymizer

faker = Faker()


def fake_name(_: str) -> str:
    return faker.company()


def test_file_and_csv_transform(tmp_path: Path):
    shared_cache = {}

    filename_transform = StableAnonymizer(fake_name, cache=shared_cache)
    csv_transform = StableAnonymizer(fake_name, cache=shared_cache)

    base_dir = tmp_path / "workdir"
    base_dir.mkdir()

    dir_to_rename = base_dir / "TestName (Folder)"
    dir_to_rename.mkdir()

    csv_file = dir_to_rename / "data.csv"
    with csv_file.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["entity"])
        writer.writeheader()
        writer.writerow({"entity": "OriginalEntity"})

    configs = [
        CsvTransformConfig(glob=["*/*.csv"], transforms={"entity": csv_transform}),
        FilenameTransformConfig(
            glob=["*"], transforms={r"^([^(]+?)(?=\s*\()": filename_transform}
        ),
    ]

    apply_transforms(configs, base_dir)

    output_dirs = list(base_dir.iterdir())
    assert len(output_dirs) == 1
    renamed_dir = output_dirs[0]
    assert renamed_dir.is_dir()
    assert renamed_dir.name != "TestName (Folder)"

    transformed_csv = renamed_dir / "data.csv"
    assert transformed_csv.exists()

    with transformed_csv.open("r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        transformed_value = rows[0]["entity"]

    assert transformed_value != "OriginalEntity"
    assert transformed_value == list(filename_transform.cache.values())[0]
