"""Deterministic synthetic data for the bootcamp (standard library only).

Every function is pure and seeded so unit tests and every participant get the
same data. `write_jsonl` is the only function that touches the filesystem.
"""
from __future__ import annotations

import json
import os
import random
from collections.abc import Iterable
from datetime import date, datetime, timedelta

REGIONS = ["EMEA", "NA", "LATAM", "APAC"]
SEGMENTS = ["consumer", "smb", "enterprise"]
CATEGORIES = ["laptops", "phones", "accessories", "software", "services"]
CHANNELS = ["web", "mobile", "store", "partner"]
FIRST_NAMES = ["Amina", "Youssef", "Sara", "Omar", "Lina", "Karim", "Nora", "Adam", "Ines", "Hugo",
               "Maya", "Leo", "Zoe", "Ali", "Emma", "Noah"]
LAST_NAMES = ["Benali", "Martin", "Garcia", "Smith", "Rossi", "Haddad", "Dubois", "Khan", "Silva", "Novak"]

START_DATE = date(2026, 1, 1)


def generate_customers(n: int = 500, seed: int = 42) -> list[dict]:
    """Customers with a hidden churn propensity that drives order behaviour."""
    rng = random.Random(seed)
    customers = []
    for i in range(1, n + 1):
        first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
        segment = rng.choices(SEGMENTS, weights=[6, 3, 1])[0]
        customers.append({
            "customer_id": i,
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{i}@example.com",
            "region": rng.choice(REGIONS),
            "segment": segment,
            "signup_date": (START_DATE - timedelta(days=rng.randint(30, 900))).isoformat(),
            # 0 = loyal, 1 = very likely to churn. Used to shape orders and the label.
            "churn_propensity": round(rng.betavariate(2, 5), 3),
        })
    return customers


def generate_products(n: int = 60, seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    products = []
    for i in range(1, n + 1):
        category = CATEGORIES[(i - 1) % len(CATEGORIES)]
        base = {"laptops": 1100, "phones": 700, "accessories": 40, "software": 150, "services": 300}[category]
        products.append({
            "product_id": i,
            "name": f"{category.removesuffix('s')}-{i:03d}",
            "category": category,
            "list_price": round(base * rng.uniform(0.6, 1.6), 2),
        })
    return products


def generate_orders(
    customers: list[dict],
    products: list[dict],
    n: int = 5000,
    batch: int = 0,
    seed: int = 100,
    with_coupon: bool = False,
    bad_record_rate: float = 0.01,
) -> list[dict]:
    """Orders for one landing batch.

    - Customers with high churn propensity order less and stop ordering earlier.
    - About `bad_record_rate` of rows are deliberately invalid (non-positive amount
      or missing customer) so pipeline expectations have something to catch.
    - `with_coupon=True` adds a new `coupon_code` column to simulate schema drift.
    """
    rng = random.Random(seed + batch)
    weights = [1.0 - c["churn_propensity"] * 0.8 for c in customers]
    orders = []
    for k in range(n):
        order_id = batch * 1_000_000 + k + 1
        customer = rng.choices(customers, weights=weights)[0]
        product = rng.choice(products)
        # High-propensity customers concentrate their orders early in the year.
        horizon = int(240 * (1.0 - customer["churn_propensity"])) + 30
        ts = datetime.combine(START_DATE, datetime.min.time()) + timedelta(
            days=rng.randint(0, horizon), seconds=rng.randint(0, 86_399))
        quantity = rng.choices([1, 2, 3, 5], weights=[70, 20, 7, 3])[0]
        amount = round(product["list_price"] * quantity * rng.uniform(0.85, 1.0), 2)
        record = {
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "amount": amount,
            "channel": rng.choice(CHANNELS),
            "order_ts": ts.isoformat(timespec="seconds"),
            "region": customer["region"].lower() if rng.random() < 0.05 else customer["region"],
        }
        if rng.random() < bad_record_rate:
            if rng.random() < 0.5:
                record["amount"] = -abs(record["amount"])
            else:
                record["customer_id"] = None
        if with_coupon:
            record["coupon_code"] = rng.choice([None, None, None, "WELCOME10", "SPRING15", "VIP20"])
        orders.append(record)
    return orders


def churn_labels(customers: list[dict], threshold: float = 0.45) -> list[dict]:
    """Ground-truth churn label derived from the hidden propensity."""
    return [{"customer_id": c["customer_id"], "churned": int(c["churn_propensity"] >= threshold)}
            for c in customers]


TICKET_TEMPLATES = {
    "delivery": [
        ("Where is my order {order_id}?", "Hi, I ordered on {date} and order {order_id} still has not arrived. {tone}"),
        ("Late delivery", "My {category} order {order_id} was supposed to arrive last week. {tone}"),
    ],
    "return": [
        ("Return request", "I would like to return the {category} item from order {order_id}. It does not fit my needs. {tone}"),
        ("Refund status", "I sent back order {order_id} ten days ago and have not received my refund yet. {tone}"),
    ],
    "billing": [
        ("Charged twice", "I was charged twice for order {order_id}. Please fix this. {tone}"),
        ("Coupon not applied", "My coupon was not applied to order {order_id}. {tone}"),
    ],
    "product_issue": [
        ("Defective product", "The {category} I received in order {order_id} stopped working after two days. {tone}"),
        ("Missing parts", "Order {order_id} arrived without the charger. {tone}"),
    ],
    "account": [
        ("Cannot log in", "I cannot log in to my account; the password reset link has expired. {tone}"),
        ("Update my e-mail", "Please update the e-mail address on my account. {tone}"),
    ],
}
TONES = {
    "positive": ["Thanks a lot for your help!", "Your team has always been great."],
    "neutral": ["Could you please check?", "Let me know the next steps."],
    "negative": ["This is really frustrating.", "I am very disappointed and considering another supplier."],
}


def generate_tickets(orders: list[dict], n: int = 300, batch: int = 0, seed: int = 11) -> list[dict]:
    """Free-text support tickets for the GenAI lab (classification, extraction, summarisation)."""
    rng = random.Random(seed + batch)
    valid = [o for o in orders if o.get("customer_id") is not None]
    tickets = []
    for i in range(1, n + 1):
        order = rng.choice(valid)
        category = rng.choice(list(TICKET_TEMPLATES))
        sentiment = rng.choices(list(TONES), weights=[2, 5, 3])[0]
        subject, body = rng.choice(TICKET_TEMPLATES[category])
        text = body.format(order_id=order["order_id"], date=order["order_ts"][:10],
                           category=rng.choice(CATEGORIES), tone=rng.choice(TONES[sentiment]))
        tickets.append({
            "ticket_id": batch * 100_000 + i,
            "customer_id": order["customer_id"],
            "channel": rng.choice(["email", "chat", "phone"]),
            "created_at": order["order_ts"],
            "subject": subject.format(order_id=order["order_id"]),
            "body": text,
            "true_category": category,          # ground truth to evaluate ai_classify
        })
    return tickets


SUPPORT_DOCS = {
    "returns-policy.md": """# Returns policy
Customers can return any product within 30 days of delivery for a full refund.
Software licences can be refunded only if the licence key was not activated.
Refunds are issued to the original payment method within 5 business days.
""",
    "shipping.md": """# Shipping
Standard shipping takes 3-5 business days in EMEA and NA, 5-8 in LATAM and APAC.
Express shipping (1-2 business days) is available for orders above 100 EUR.
""",
    "loyalty-program.md": """# Loyalty program
Enterprise customers get a dedicated account manager.
Coupon VIP20 gives 20% off accessories and can be combined with free shipping.
Coupons WELCOME10 and SPRING15 cannot be combined with other offers.
""",
    "password-reset.md": """# Password reset
Use 'Forgot password' on the sign-in page. The reset link is valid for 30 minutes.
If the link expired, request a new one; accounts lock after 5 failed attempts for 15 minutes.
""",
}


def write_jsonl(records: Iterable[dict], path: str) -> int:
    """Write records as JSON lines; creates parent folders. Returns the row count."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    count = 0
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
            count += 1
    return count
