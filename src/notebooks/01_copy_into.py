# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 01 · Idempotent batch loads with COPY INTO
# MAGIC Compare with the Auto Loader streaming table in the pipeline: COPY INTO is a simple,
# MAGIC re-runnable SQL command that skips files it has already loaded.

# COMMAND ----------

# MAGIC %run ./_setup

# COMMAND ----------

spark.sql("CREATE TABLE IF NOT EXISTS orders_copy_into")

# SOLUTION-BEGIN lab-01: Write a COPY INTO statement that loads JSON files from f"{raw_path}/orders/" into orders_copy_into with mergeSchema enabled for both format and copy options. Display the result.
result = spark.sql(f"""
  COPY INTO orders_copy_into
  FROM '{raw_path}/orders/'
  FILEFORMAT = JSON
  FORMAT_OPTIONS ('mergeSchema' = 'true', 'inferSchema' = 'true')
  COPY_OPTIONS ('mergeSchema' = 'true')
""")
display(result)
# SOLUTION-END

# COMMAND ----------

# MAGIC %md
# MAGIC Run the previous cell **again**. `num_inserted_rows` is 0 — COPY INTO is idempotent.
# MAGIC Now run the `generate_data` job with `batch=1` and re-run: only the new file is loaded.

# COMMAND ----------

display(spark.sql("SELECT count(*) AS total_rows, count(DISTINCT order_id) AS distinct_orders FROM orders_copy_into"))
