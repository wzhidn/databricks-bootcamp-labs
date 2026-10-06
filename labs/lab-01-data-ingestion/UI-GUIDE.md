# Lab 01 · From raw files to trusted data — business track
**Deck section: Data Engineering · 45 min · no code** · [How to read this guide](../UI-CONVENTIONS.md)
Prerequisite: lab 00 business path (`business_quickstart` ran).

**What you will learn:** where the data behind your reports comes from, how the platform keeps it clean automatically,
and why "bronze, silver, gold" matters when you ask engineers for new data.

## 1 · Look at the raw data (5 min)
1. Left sidebar **Catalog** → **bootcamp_dev** → **dev_<you>_sales** → **Volumes** → **raw** → **orders**.
2. Click a file → **Preview**. This is what arrives from the web shop: raw, unchecked records.

💬 What could go wrong if a report read these files directly?

## 2 · See the pipeline that cleans it (10 min)
3. Left sidebar **Jobs & Pipelines** → **[dev <you>] orders_pipeline** → open the latest run.
4. Read the **graph** from left to right:
   * **Bronze** (`orders_bronze`) — everything that landed, untouched
   * **Silver** (`orders_silver`) — cleaned and checked
   * **Gold** (`revenue_by_region_daily`, `orders_enriched`) — ready for business use
5. Click **orders_silver** → **Data quality** tab. About **1 %** of orders were rejected: no customer, or a negative amount.
   These rules are *written in the pipeline*, so they run every time — nobody has to remember.

💬 Which quality rules would you ask for on your own data (e.g. "an invoice date can't be in the future")?

## 3 · Build a small pipeline without code (15 min) — *if Lakeflow Designer is available*
6. **Jobs & Pipelines** → **Create** → **ETL pipeline** (or **Lakeflow Designer**) → *Visual* / *Designer* canvas.
7. Add a **source**: table `bootcamp_dev.dev_<you>_sales.orders_enriched`.
8. Add a **Filter**: `channel` = *mobile*. Add an **Aggregate**: group by `category`, sum of `amount`.
9. Look at the **preview** under each step, then **Save**. Open the generated SQL: engineers can review exactly what you built.

Not available in your workspace? Do step 10 instead.

## 4 · Bring your own spreadsheet (5 min)
10. Save any small table from Excel as CSV → Databricks **New** (top left) → **Add or upload data** → **Create or modify
    table** → drop the file → catalog **bootcamp_dev**, schema **dev_<you>_sales** → **Create table**.
    It is now governed like every other table.

## 5 · Undo a mistake with time travel (10 min)
11. **Catalog** → **customer_profiles** → **History** tab. You see every change, including a *DELETE* someone made
    (the course script deleted all EMEA customers on purpose) and the *RESTORE* that brought them back.
12. 💬 How would "we can go back to yesterday's version of any table" change your audit or month-end close process?

## Take-aways
- Raw data is never lost (bronze); rules are code, applied on every run (silver); gold is what reports should use.
- You can prototype a transformation visually and hand it to engineers as reviewable code.
- Every table keeps its history — mistakes are reversible.
