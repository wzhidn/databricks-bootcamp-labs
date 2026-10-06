# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Generate bootcamp sample data
# MAGIC Writes deterministic synthetic data to the `raw` volume:
# MAGIC
# MAGIC | Folder | Content |
# MAGIC |---|---|
# MAGIC | `customers/` | 500 customers (JSON lines) |
# MAGIC | `products/` | 60 products |
# MAGIC | `orders/` | one file per batch (default 5,000 orders) |
# MAGIC | `labels/` | churn ground truth for the ML lab |
# MAGIC | `tickets/` | free-text support tickets for the GenAI lab |
# MAGIC | `docs/` | support articles for the agent lab |
# MAGIC
# MAGIC Run it from the job `generate_data` (lab 01) or interactively. Re-run with a new `batch` to land more orders;
# MAGIC set `with_coupon=true` to introduce a new column (schema drift, lab 01).

# COMMAND ----------

import os
import sys

# Make src/ importable when running from the bundle's workspace files.
sys.path.append(os.path.abspath(".."))

from bootcamp_lib import datagen  # noqa: E402

dbutils.widgets.text("catalog", "bootcamp_dev")
dbutils.widgets.text("schema", "sales")
dbutils.widgets.text("batch", "0")
dbutils.widgets.text("orders_per_batch", "5000")
dbutils.widgets.dropdown("with_coupon", "false", ["false", "true"])

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
batch = int(dbutils.widgets.get("batch"))
orders_per_batch = int(dbutils.widgets.get("orders_per_batch"))
with_coupon = dbutils.widgets.get("with_coupon") == "true"

root = f"/Volumes/{catalog}/{schema}/raw"
print(f"Writing to {root} (batch={batch}, orders={orders_per_batch}, with_coupon={with_coupon})")

# COMMAND ----------

customers = datagen.generate_customers()
products = datagen.generate_products()
orders = datagen.generate_orders(customers, products, n=orders_per_batch, batch=batch, with_coupon=with_coupon)

counts = {
    "customers": datagen.write_jsonl(
        [{k: v for k, v in c.items() if k != "churn_propensity"} for c in customers],
        f"{root}/customers/customers.json"),
    "products": datagen.write_jsonl(products, f"{root}/products/products.json"),
    "orders": datagen.write_jsonl(orders, f"{root}/orders/orders_batch_{batch:03d}.json"),
    "labels": datagen.write_jsonl(datagen.churn_labels(customers), f"{root}/labels/churn_labels.json"),
    "tickets": datagen.write_jsonl(datagen.generate_tickets(orders, batch=batch), f"{root}/tickets/tickets_batch_{batch:03d}.json"),
}

os.makedirs(f"{root}/docs", exist_ok=True)
for name, text in datagen.SUPPORT_DOCS.items():
    with open(f"{root}/docs/{name}", "w", encoding="utf-8") as fh:
        fh.write(text)
counts["docs"] = len(datagen.SUPPORT_DOCS)

print(counts)
dbutils.jobs.taskValues.set("orders_written", counts["orders"])
