import csv
from pathlib import Path
from structured_data_transformer.adapters.csv import transform_csv_file
from structured_data_transformer.transforms.anonymizers import fake_email, fake_company


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def test_csv_single_column_transformation(tmp_path: Path):
    file = tmp_path / "data.csv"
    write_csv(file, ["email"], [{"email": "real@example.com"}])

    transformations = {"email": fake_email}
    transform_csv_file(file, "utf-8", transformations)

    rows = read_csv_rows(file)
    assert rows[0]["email"] != "real@example.com"


def test_csv_multiple_rows_transformation(tmp_path: Path):
    file = tmp_path / "data.csv"
    write_csv(
        file,
        ["email"],
        [
            {"email": "one@example.com"},
            {"email": "two@example.com"},
        ],
    )

    transformations = {"email": fake_email}
    transform_csv_file(file, "utf-8", transformations)

    rows = read_csv_rows(file)
    assert rows[0]["email"] != "one@example.com"
    assert rows[1]["email"] != "two@example.com"


def test_csv_multiple_columns_transformation(tmp_path: Path):
    file = tmp_path / "data.csv"
    write_csv(
        file,
        ["email", "company"],
        [
            {"email": "foo@example.com", "company": "FooCorp"},
        ],
    )

    transformations = {"email": fake_email, "company": fake_company}
    transform_csv_file(file, "utf-8", transformations)

    rows = read_csv_rows(file)
    assert rows[0]["email"] != "foo@example.com"
    assert rows[0]["company"] != "FooCorp"


def test_csv_missing_column_tolerant(tmp_path: Path):
    file = tmp_path / "data.csv"
    write_csv(file, ["company"], [{"company": "FooCorp"}])

    transformations = {"missing": fake_company}
    transform_csv_file(file, "utf-8", transformations)

    rows = read_csv_rows(file)
    assert rows[0]["company"] == "FooCorp"
