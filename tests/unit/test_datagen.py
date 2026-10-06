from bootcamp_lib import datagen


def test_generation_is_deterministic():
    c1, c2 = datagen.generate_customers(50), datagen.generate_customers(50)
    assert c1 == c2
    p = datagen.generate_products(10)
    assert datagen.generate_orders(c1, p, n=100) == datagen.generate_orders(c2, p, n=100)


def test_order_ids_are_unique_across_batches():
    c, p = datagen.generate_customers(50), datagen.generate_products(10)
    ids = [o["order_id"] for b in range(3) for o in datagen.generate_orders(c, p, n=500, batch=b)]
    assert len(ids) == len(set(ids))


def test_bad_records_are_injected_at_the_expected_rate():
    c, p = datagen.generate_customers(200), datagen.generate_products(20)
    orders = datagen.generate_orders(c, p, n=5000, bad_record_rate=0.02)
    bad = [o for o in orders if o["customer_id"] is None or o["amount"] <= 0]
    assert 0.01 < len(bad) / len(orders) < 0.03


def test_schema_drift_adds_coupon_column_only_when_requested():
    c, p = datagen.generate_customers(20), datagen.generate_products(5)
    assert "coupon_code" not in datagen.generate_orders(c, p, n=10)[0]
    assert "coupon_code" in datagen.generate_orders(c, p, n=10, with_coupon=True)[0]


def test_churn_labels_are_binary_and_balanced_enough():
    labels = datagen.churn_labels(datagen.generate_customers(500))
    share = sum(row["churned"] for row in labels) / len(labels)
    assert {row["churned"] for row in labels} <= {0, 1}
    assert 0.1 < share < 0.6


def test_write_jsonl(tmp_path):
    path = tmp_path / "nested" / "out.json"
    assert datagen.write_jsonl([{"a": 1}, {"a": 2}], str(path)) == 2
    assert path.read_text().count("\n") == 2


def test_tickets_mention_real_orders_and_cover_all_categories():
    c, p = datagen.generate_customers(100), datagen.generate_products(20)
    orders = datagen.generate_orders(c, p, n=500)
    tickets = datagen.generate_tickets(orders, n=200)
    order_ids = {str(o["order_id"]) for o in orders}
    assert len(tickets) == 200
    assert {t["true_category"] for t in tickets} == set(datagen.TICKET_TEMPLATES)
    with_order = [t for t in tickets if t["true_category"] != "account"]
    assert all(any(oid in t["body"] for oid in order_ids) for t in with_order[:20])
