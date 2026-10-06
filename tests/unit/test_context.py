from bootcamp_lib import context


def test_short_name_matches_dev_mode_prefix():
    assert context.short_name("First.Last-Name@example.com") == "first_last_name"


def test_resolve_defaults_to_dev_schema():
    assert context.resolve("", "", "ana.b@example.com") == ("bootcamp_dev", "dev_ana_b_sales")
    assert context.resolve("bootcamp_prod", "sales", "x@example.com") == ("bootcamp_prod", "sales")
