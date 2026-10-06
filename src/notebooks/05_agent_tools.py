# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 05 · Governed tools for the support agent
# MAGIC Unity Catalog functions become agent tools: governed, versioned, discoverable — and callable through MCP.
# MAGIC After this notebook, they are wired into the code-first agent in `05_agent` (Free Edition has no Agent Bricks Knowledge Assistant).

# COMMAND ----------

# MAGIC %run ./_setup

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SOLUTION-BEGIN lab-05: Create a table-valued SQL function lookup_order(p_order_id BIGINT) that returns order_id, order_date, amount, channel, category and region from orders_enriched, with a COMMENT the agent can read.
# MAGIC CREATE OR REPLACE FUNCTION lookup_order(p_order_id BIGINT COMMENT 'The order number the customer mentions')
# MAGIC RETURNS TABLE (order_id BIGINT, order_date DATE, amount DECIMAL(12, 2), channel STRING, category STRING, region STRING)
# MAGIC COMMENT 'Look up a single order by its order number. Use when a customer asks about the status or content of an order.'
# MAGIC RETURN
# MAGIC   SELECT order_id, order_date, amount, channel, category, region
# MAGIC   FROM orders_enriched
# MAGIC   WHERE order_id = p_order_id;
# MAGIC -- SOLUTION-END

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION customer_order_summary(p_customer_id BIGINT COMMENT 'Customer identifier')
# MAGIC RETURNS TABLE (customer_id BIGINT, orders BIGINT, revenue DECIMAL(22, 2), last_order DATE)
# MAGIC COMMENT 'Summarise a customer''s order history: number of orders, total spend and last order date.'
# MAGIC RETURN
# MAGIC   SELECT customer_id, count(*), sum(amount), max(order_date)
# MAGIC   FROM orders_enriched
# MAGIC   WHERE customer_id = p_customer_id
# MAGIC   GROUP BY customer_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM lookup_order(1);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customer_order_summary(42);

# COMMAND ----------

# MAGIC %md
# MAGIC ## Knowledge source: support documents as a governed table
# MAGIC The agent retrieves policy text from this table. (Stretch: index it with Databricks AI Search.)

# COMMAND ----------

from pyspark.sql import functions as F

docs = (
    spark.read.format("text").option("wholetext", True).load(f"{raw_path}/docs/")
    .select(F.col("_metadata.file_name").alias("doc_id"), F.col("value").alias("content"))
)
docs.write.mode("overwrite").option("overwriteSchema", True).saveAsTable("support_docs")
spark.sql("ALTER TABLE support_docs SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
display(spark.table("support_docs"))
