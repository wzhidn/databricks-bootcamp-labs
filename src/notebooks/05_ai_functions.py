# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 05 · Generative AI in SQL with AI Functions
# MAGIC Turn 300 free-text support tickets into structured, governed data — no model hosting, no Python.
# MAGIC Every call goes through **Foundation Model APIs** and is governed by **Unity Gateway**.
# MAGIC
# MAGIC Prerequisite: `generate_data` ran (tickets are in the `raw` volume).

# COMMAND ----------

# MAGIC %run ./_setup

# COMMAND ----------

spark.sql(f"""
  CREATE OR REPLACE TABLE support_tickets
  COMMENT 'Raw support tickets (synthetic) — input for AI Functions'
  AS SELECT * FROM read_files('{raw_path}/tickets/', format => 'json')
""")
display(spark.sql("SELECT ticket_id, channel, subject, body FROM support_tickets LIMIT 10"))

# COMMAND ----------

# MAGIC %md ## 1 · Classify, analyse sentiment, extract

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO (lab-05): Create table tickets_enriched with ai_classify(body, ARRAY('delivery','return','billing','product_issue','account')) AS category, ai_analyze_sentiment(body) AS sentiment and ai_extract(body, ARRAY('order_id','product')) AS entities, for all tickets.

# COMMAND ----------

# MAGIC %md ## 2 · How good is the classifier?
# MAGIC The generator stored the true category, so we can measure accuracy — always evaluate GenAI output.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT round(avg(CASE WHEN category = true_category THEN 1.0 ELSE 0 END) * 100, 1) AS accuracy_pct,
# MAGIC        count(*) AS tickets
# MAGIC FROM tickets_enriched;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT category, sentiment, count(*) AS tickets
# MAGIC FROM tickets_enriched
# MAGIC GROUP BY ALL
# MAGIC ORDER BY tickets DESC;

# COMMAND ----------

# MAGIC %md ## 3 · Summarise and draft replies for the angry customers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO (lab-05): For the 10 most recent negative tickets, return ai_summarize(body, 20) AS summary and an ai_gen draft reply that is polite, apologises and never promises a refund.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · Choose your model explicitly with `ai_query`
# MAGIC Task-specific functions pick a default model. `ai_query` lets you choose any endpoint listed under **Serving**.

# COMMAND ----------

dbutils.widgets.text("llm_endpoint", "databricks-meta-llama-3-3-70b-instruct", "Chat model (see Serving)")
llm = dbutils.widgets.get("llm_endpoint")
display(spark.sql(f"""
  SELECT ticket_id, body,
         ai_query('{llm}', concat('In one short sentence, what does the customer want? ', body)) AS intent
  FROM support_tickets LIMIT 5
"""))
