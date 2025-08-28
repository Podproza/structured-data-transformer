import pytest


@pytest.fixture(autouse=True)
def patch_fakes(monkeypatch):
    monkeypatch.setattr(
        "structured_data_transformer.btc_json_sanitizer.fake_p2sh_address",
        lambda _: "A",
    )
    monkeypatch.setattr(
        "structured_data_transformer.btc_json_sanitizer.fake_transaction_id",
        lambda _: "T",
    )
