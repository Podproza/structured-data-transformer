from structured_data_transformer.btc_json_sanitizer import sanitize_string


def test_btc_address():
    s = "Send to 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"
    cache = {}
    result = sanitize_string(s, cache)
    assert result == "Send to A"
    assert "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy" in cache


def test_txid_only():
    txid = "4e9b7b60ffb9e2c3a56492e7985c3a4f35692b95d3fa7bb5db83d4d1c09e2b88"
    s = f"TX: {txid}"
    cache = {}
    result = sanitize_string(s, cache)
    assert result == "TX: T"
    assert txid in cache


def test_outref_only():
    txid = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    s = f"{txid}_1"
    cache = {}
    result = sanitize_string(s, cache)
    assert result == "T_1"
    assert cache[txid] == "T"
    assert cache[s] == "T_1"


def test_mixed_string():
    addr = "1BoatSLRHtKNngkdXEeobR76b53LETtpyT"
    txid = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    s = f"{addr} paid in {txid}_0"
    cache = {}
    result = sanitize_string(s, cache)
    assert result == "A paid in T_0"
    assert addr in cache
    assert txid in cache
    assert f"{txid}_0" in cache


def test_shared_txid_consistency():
    txid = "c" * 64
    s = f"{txid} and {txid}_2"
    cache = {}
    result = sanitize_string(s, cache)
    assert result == "T and T_2"
    assert cache[txid] == "T"
    assert cache[f"{txid}_2"] == "T_2"
