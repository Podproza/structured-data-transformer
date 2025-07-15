from pathlib import Path

from structured_data_transformer.adapters.path import transform_path
from structured_data_transformer.transforms.anonymizers import fake_company, fake_email


def test_transform_path_single_pattern_match():
    input_path = Path("/tmp/CompanyABC_report.csv")
    output_path = Path("/tmp/output.csv")
    transforms = {r"(CompanyABC)": fake_company}
    new_path = transform_path(input_path, output_path, transforms)
    assert "CompanyABC" not in new_path.name
    assert new_path.parent == output_path.parent


def test_transform_path_multiple_patterns_first_match():
    input_path = Path("/tmp/user_email_report.csv")
    output_path = Path("/tmp/output.csv")
    transforms = {r"(user_email)": fake_email, r"(report)": fake_company}
    new_path = transform_path(input_path, output_path, transforms)
    assert "user_email" not in new_path.name


def test_transform_path_no_match_returns_original_output():
    input_path = Path("/tmp/nothing_to_replace.csv")
    output_path = Path("/tmp/output.csv")
    transforms = {r"(missing)": fake_company}
    new_path = transform_path(input_path, output_path, transforms)
    assert new_path.name == output_path.name
    assert new_path.parent == output_path.parent


def test_transform_path_partial_regex():
    input_path = Path("/tmp/test_123_data.csv")
    output_path = Path("/tmp/output.csv")

    def add_prefix(value: str) -> str:
        return f"prefix_{value}"

    transforms = {r"test_(\d+)_data": add_prefix}
    new_path = transform_path(input_path, output_path, transforms)
    assert "prefix_" in new_path.name
