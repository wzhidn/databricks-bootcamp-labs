# Lab 01 · Data Ingestion — technical track
**Deck section: Data Engineering (Lab · Data Ingestion) · 75 min** · checkpoint: `checkpoint/lab-01-ingestion`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** land raw files incrementally, clean them with data-quality expectations, build business-ready gold tables with
**Lakeflow Spark Declarative Pipelines**, survive a schema change — and use the 2026 Delta / Iceberg features on the result.

## What you build
| Artifact | Where |
|----------|-------|
| `orders_bronze` streaming table | `src/pipelines/01_bronze.sql` |
| `orders_silver` with three expectations | `src/pipelines/02_silver.sql` |
| `revenue_by_region_daily`, `orders_enriched` | `src/pipelines/03_gold.sql` |
| `orders_copy_into` (idempotent batch load) | `src/notebooks/01_copy_into.py` |
| `orders_iceberg`, `orders_status`, `customer_profiles` | `src/notebooks/01_delta_iceberg.py` |

Everything downstream — governance, BI, ML and the agent — reads these tables, so finish this lab before moving on.

## Prerequisites
* Lab 00 parts 1–3 done: Git folder, catalogs created, `generate_data` available.
* Files you edit are marked `TODO (lab-01)`; the pipeline itself is declared as code in
  `resources/ingestion.pipeline.yml` — never create it in the UI.
* Free Edition: one active pipeline per type. Don't start a second pipeline run while this one is going.

## Part A · Workspace warm-up (10 min)
1. Git folder → `databricks.yml` → **Deployments** → **dev** → **Deploy** (or `databricks bundle deploy`).
   Note the names: `[dev <you>] …`, schema `dev_<you>_sales` — development mode isolates you.
2. Run `generate_data` (**Bundle resources** ▶, or `databricks bundle run generate_data`) and browse
   **Catalog → bootcamp_dev → dev_<you>_sales → Volumes → raw**.
3. **SQL Editor** on *Serverless Starter Warehouse*: query the files directly
   ```sql
   SELECT region, count(*) AS orders, round(sum(amount), 2) AS revenue
   FROM read_files('/Volumes/bootcamp_dev/dev_<you>_sales/raw/orders/', format => 'json')
   GROUP BY ALL ORDER BY revenue DESC;
   ```
   Ask **Genie Code** to add the average order value, review the diff, accept.

## Part B · Medallion pipeline (30 min)
| Layer | File | You write |
|-------|------|-----------|
| Bronze | `01_bronze.sql` | streaming table `orders_bronze` over `STREAM read_files('${raw_path}/orders/', format => 'json', schemaEvolutionMode => 'addNewColumns')` + `source_file`, `ingested_at` |
| Silver | `02_silver.sql` | three expectations: drop null `customer_id`, drop `amount <= 0`, warn on unknown region |
| Gold | `03_gold.sql` | materialized view `revenue_by_region_daily` |

Then:
```bash
databricks bundle deploy
databricks bundle run orders_pipeline
```
Open the pipeline graph → `orders_silver` → **Data quality**: ≈ 1 % of rows dropped (the generator injects bad records).

## Part C · Schema drift (10 min)
```bash
databricks bundle run generate_data --params batch=1,with_coupon=true
databricks bundle run orders_pipeline
```
Bronze picks up the new column `coupon_code` (the stream restarts once — expected). Add `coupon_code` to the silver
select list (second TODO), redeploy, run again.

## Part D · COPY INTO (5 min)
`src/notebooks/01_copy_into.py`: complete the TODO, run twice — the second run inserts 0 rows (idempotent).

## Part E · Delta Lake & managed Iceberg (20 min)
`src/notebooks/01_delta_iceberg.py`, top to bottom:
managed **Iceberg** table (`USING ICEBERG`) · `MERGE` · **multi-statement transaction** (GA Jul 2026) ·
accidental `DELETE` → time travel → `RESTORE` · row-level changes with `table_changes()` · `CLUSTER BY AUTO`.

## Stretch
* **Zerobus Ingest:** push events straight into a Delta table with the Zerobus SDK.
* **Lakeflow Designer:** rebuild the gold aggregate on the no-code canvas and compare the generated SQL.
* **Lakeflow Connect:** your instructor demos a managed connector (SharePoint / Salesforce).

## Done when
- [ ] `orders_bronze`, `orders_silver`, `revenue_by_region_daily`, `orders_enriched` exist and have rows
- [ ] `coupon_code` arrived without breaking the pipeline
- [ ] The refund transaction and the RESTORE worked; `orders_status` uses automatic liquid clustering

## Troubleshooting
| Symptom | Fix |
|--------|-----|
| `CATALOG_DOES_NOT_EXIST: bootcamp_dev` | Run `setup/free_edition_setup` (lab 00) or enable the single-catalog fallback |
| `Table or view not found: orders_bronze` | Part B bronze not done — silver depends on it |
| Pipeline fails with a limit error | Free Edition: one active pipeline per type — wait for other runs |
| Transaction syntax refused | Check the transactions docs for your runtime |
