from structured_data_transformer.adapters.json import transform_json
from structured_data_transformer.transforms import StableAnonymizer
from structured_data_transformer.transforms.anonymizers import fake_email, fake_company


def test_stable_anonymizer_same_input_same_output():
    anonymizer = StableAnonymizer(fake_email, cache={})
    value1 = anonymizer("foo@example.com")
    value2 = anonymizer("foo@example.com")
    assert value1 == value2


def test_stable_anonymizer_different_inputs_different_outputs():
    anonymizer = StableAnonymizer(fake_email, cache={})
    value1 = anonymizer("foo@example.com")
    value2 = anonymizer("bar@example.com")
    assert value1 != value2


def test_stable_anonymizer_shared_cache_same_output():
    shared_cache = {}
    anon1 = StableAnonymizer(fake_email, cache=shared_cache)
    anon2 = StableAnonymizer(fake_email, cache=shared_cache)

    value1 = anon1("foo@example.com")
    value2 = anon2("foo@example.com")
    assert value1 == value2


def test_stable_anonymizer_different_transformers_same_cache_possible_collision():
    shared_cache = {}
    anon_email = StableAnonymizer(fake_email, cache=shared_cache)
    anon_company = StableAnonymizer(fake_company, cache=shared_cache)

    val1 = anon_email("foo@example.com")
    val2 = anon_company("foo@example.com")

    assert val1 == val2


def test_stable_anonymizer_uses_existing_cache():
    shared_cache = {"foo@example.com": "cached_value@example.com"}
    anonymizer = StableAnonymizer(fake_email, cache=shared_cache)

    result = anonymizer("foo@example.com")
    assert result == "cached_value@example.com"


def test_stable_transformer_same_value_multiple_times():
    shared_cache = {}

    anonymize_email = StableAnonymizer(fake_email, cache=shared_cache)

    data = {
        "contacts": [
            {"email": "foo@example.com"},
            {"email": "foo@example.com"},
            {"email": "bar@example.com"},
        ]
    }

    transformations = {"$.contacts[*].email": anonymize_email}

    transform_json(data, transformations)

    emails = [item["email"] for item in data["contacts"]]

    assert emails[0] == emails[1]
    assert emails[0] != "foo@example.com"
    assert emails[2] != emails[0]


def test_stable_transformer_consistent_across_runs_with_same_cache():
    shared_cache = {}

    anonymize_email = StableAnonymizer(fake_email, cache=shared_cache)

    data1 = [{"email": "foo@example.com"}, {"email": "bar@example.com"}]

    data2 = [{"email": "foo@example.com"}, {"email": "baz@example.com"}]

    transformations = {"$[*].email": anonymize_email}

    transform_json(data1, transformations)
    first_result = [item["email"] for item in data1]

    transform_json(data2, transformations)
    second_result = [item["email"] for item in data2]

    assert first_result[0] == second_result[0]

    assert second_result[1] != "baz@example.com"
    assert second_result[1] != first_result[0]
