# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 04 · Unity Catalog, Domains & Metric Views
# MAGIC Prerequisites: labs 02–03 completed; you created the groups `bootcamp_analysts` and
# MAGIC `bootcamp_engineers` and added yourself to `bootcamp_engineers` (lab 00, part 2.5).
# MAGIC
# MAGIC UI steps (Domains, glossary, lineage) are in `labs/lab-02-data-governance/README.md`.

# COMMAND ----------

# MAGIC %run ./_setup

# COMMAND ----------

# MAGIC %md ## 1 · Privileges

# COMMAND ----------

# TODO (lab-02): Grant USE SCHEMA and SELECT on your schema to bootcamp_analysts, and USE SCHEMA, SELECT, MODIFY and CREATE TABLE to bootcamp_engineers. Then SHOW GRANTS on the schema.

# COMMAND ----------

# MAGIC %md ## 2 · Tag sensitive columns and mask them

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE customer_profiles ALTER COLUMN email SET TAGS ('pii' = 'email');
# MAGIC ALTER TABLE customer_profiles ALTER COLUMN last_name SET TAGS ('pii' = 'name');

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO (lab-02): Create a SQL UDF mask_email(email STRING) that returns the e-mail for members of bootcamp_engineers and '***@<domain>' for everyone else, then apply it as a column mask on customer_profiles.email.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- You are in bootcamp_engineers: full e-mails. Now remove yourself from the group
# MAGIC -- (Settings → Identity and access → Groups), wait ~1 minute and re-run: e-mails are masked.
# MAGIC -- Add yourself back afterwards.
# MAGIC SELECT customer_id, first_name, email, region FROM customer_profiles LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch · the same control with ABAC
# MAGIC Attribute-based policies apply to **every** column tagged `pii`, in every table of the schema,
# MAGIC instead of one table at a time. Follow the ABAC docs for your workspace
# MAGIC (policy syntax and availability vary by release — metastore-level policies are Beta):
# MAGIC https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/
# MAGIC
# MAGIC Optional: create a *tag automation* rule (Beta) that tags every new column named `email` with `pii=email`.

# COMMAND ----------

# MAGIC %md ## 3 · A governed metric view

# COMMAND ----------

# TODO (lab-02): Create the metric view orders_metrics (CREATE OR REPLACE VIEW ... WITH METRICS LANGUAGE YAML) on orders_enriched with dimensions order_month, region, segment, category, channel and measures revenue, order_count and avg_order_value.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_month, region,
# MAGIC        MEASURE(revenue)         AS revenue,
# MAGIC        MEASURE(avg_order_value) AS aov
# MAGIC FROM orders_metrics
# MAGIC GROUP BY ALL
# MAGIC ORDER BY order_month, region;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · Troubleshoot
# MAGIC Break it yourself: `REVOKE SELECT ON TABLE customer_profiles FROM bootcamp_analysts`.
# MAGIC Then use **Catalog Explorer → Permissions** and **Lineage** to find which downstream objects analysts can no
# MAGIC longer read (metric view, dashboard), and grant it back.
