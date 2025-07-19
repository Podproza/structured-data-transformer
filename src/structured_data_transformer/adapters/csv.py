import csv
from pathlib import Path

from structured_data_transformer.types import TransformFunc


def transform_csv_file(
    path: Path, encoding: str, transforms: dict[str, TransformFunc]
) -> None:
    temp_path = path.with_suffix(".tmp")

    with (
        path.open("r", encoding=encoding, newline="") as infile,
        temp_path.open("w", newline="", encoding=encoding) as outfile,
    ):
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            for column, transform in transforms.items():
                if column in row:
                    row[column] = transform(row[column])
            writer.writerow(row)

    temp_path.replace(path)
