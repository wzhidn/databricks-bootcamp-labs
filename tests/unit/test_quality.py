import pytest

from bootcamp_lib import quality


@pytest.mark.parametrize("raw, expected", [
    ("EMEA", "EMEA"), (" emea ", "EMEA"), ("na", "NA"), ("MARS", None), (None, None),
])
def test_normalize_region(raw, expected):
    assert quality.normalize_region(raw) == expected


@pytest.mark.parametrize("record, valid", [
    ({"customer_id": 1, "amount": 10.0, "quantity": 1}, True),
    ({"customer_id": None, "amount": 10.0, "quantity": 1}, False),
    ({"customer_id": 1, "amount": -5.0, "quantity": 1}, False),
    ({"customer_id": 1, "amount": 10.0, "quantity": 0}, False),
])
def test_is_valid_order(record, valid):
    assert quality.is_valid_order(record) is valid


def test_discount_rate():
    assert quality.discount_rate("vip20") == 0.20
    assert quality.discount_rate(None) == 0.0


def test_silver_expectations_match_python_rules():
    """The SQL expectations must encode the same rules as quality.py."""
    import pathlib
    sql = (pathlib.Path(__file__).parents[2] / "src/pipelines/02_silver.sql").read_text()
    if "CONSTRAINT" not in sql:
        pytest.skip("Silver expectations not implemented yet (lab 01)")
    assert "customer_id IS NOT NULL" in sql
    assert "amount > 0" in sql
    for region in quality.VALID_REGIONS:
        assert f"'{region}'" in sql
