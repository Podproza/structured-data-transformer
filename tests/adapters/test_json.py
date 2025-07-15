from structured_data_transformer.adapters.json import (
    transform_json,
)
from structured_data_transformer.transforms.anonymizers import fake_email, fake_company


def test_single_field_transformation():
    data = {"email": "real@example.com"}
    transformations = {"$.email": fake_email}
    transform_json(data, transformations)
    assert data["email"] != "real@example.com"


def test_list_of_objects_transformation():
    data = [{"email": "one@example.com"}, {"email": "two@example.com"}]
    transformations = {"$[*].email": fake_email}
    transform_json(data, transformations)
    assert data[0]["email"] != "one@example.com"
    assert data[1]["email"] != "two@example.com"


def test_nested_field_transformation():
    data = {"user": {"company": "MyCorp"}}
    transformations = {"$.user.company": fake_company}
    transform_json(data, transformations)
    assert data["user"]["company"] != "MyCorp"


def test_missing_jsonpath_tolerant():
    data = {"user": {"company": "MyCorp"}}
    transformations = {"$.user.missing": fake_company}
    transform_json(data, transformations)
    assert data == {"user": {"company": "MyCorp"}}


def test_multiple_fields_transformation():
    data = {"user": {"email": "foo@example.com", "company": "FooCorp"}}
    transformations = {"$.user.email": fake_email, "$.user.company": fake_company}
    transform_json(data, transformations)
    assert data["user"]["email"] != "foo@example.com"
    assert data["user"]["company"] != "FooCorp"
