# Lab 03 · Business Intelligence — technical track
**Deck section: Business Intelligence (Lab · Business Intelligence) · 60 min** · checkpoint: `checkpoint/lab-03-bi`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** model the gold layer as a **star schema** with keys, publish an **AI/BI dashboard** on governed metrics and curate
a **Genie Agent** that answers correctly — proven with benchmarks.

## What you build
| Artifact | Where |
|----------|-------|
| `dim_customer`, `dim_product`, `dim_date` | `src/notebooks/03_bi_model.py` |
| `fact_orders` with PK/FK constraints (`RELY`) | same notebook |
| Published dashboard *Sales overview (&lt;you&gt;)* | Dashboards UI |
| Genie Agent with instructions, trusted SQL and benchmarks | Genie UI |

Lab 06 brings the dashboard and the Genie Agent under code with `bundle generate`, so give them the names used here.

## Prerequisites
* Lab 01 done — `orders_silver` and `orders_enriched` have rows.
* Lab 02 done — `orders_metrics` exists; the dashboard and Genie both read it, not the raw tables.
* Notebook: `src/notebooks/03_bi_model.py`, TODOs marked `lab-03`.
* One SQL warehouse is running (Free Edition has exactly one).

## Part A · Star schema (20 min)
Complete the notebook: `dim_customer`, `dim_product`, `dim_date` (TODO), `fact_orders` (TODO), primary keys and
foreign keys (TODO) with `RELY`. Open **Catalog → fact_orders → Overview** → *Entity relationship diagram*.

💡 Compare with the *Star schema*, *Snowflake schema* and *Data Vault* slides: which would you pick for this dataset, and why?

## Part B · AI/BI dashboard on the metric view (15 min)
**Dashboards → Create dashboard** → **Data** tab → **Add data source** → `orders_metrics` (and `fact_orders`).
Build: revenue trend by `order_month`, revenue by `region`, `avg_order_value` by `segment`, a filter on `channel`.
**Publish** (embed credentials: off) and share with `bootcamp_analysts`.

## Part C · Genie Agent (20 min)
**Genie → New** → data: `orders_metrics`, `fact_orders`, `dim_customer`, `dim_product`, `dim_date` →
* **Instructions:** *Revenue always means the governed revenue measure. Use calendar months. Answer in EUR.*
* **Trusted SQL:** one example query (e.g. revenue by segment and quarter).
* **Benchmarks:** 5 questions with expected SQL/answers → **Run benchmarks** → fix what fails.
Ask *"Which region grew fastest last month?"* → **Show code**.

## Part D · Genie One (5 min)
Open **Genie One** (account-level chat) and ask the same question; note it answers from your Genie Agent and dashboard.

## Stretch
* Genie One **MCP server** (GA): expose your Genie Agent to other agents (used again in lab 05).
* Put the dashboard and Genie Agent under code in lab 06 (`bundle generate dashboard / genie-space`).

## Done when
- [ ] Star schema with PK/FK constraints
- [ ] Published dashboard on `orders_metrics`
- [ ] Genie Agent passes ≥ 4 of 5 benchmarks

## Troubleshooting
| Symptom | Fix |
|--------|-----|
| `ADD CONSTRAINT … PRIMARY KEY` fails | The key column must be `NOT NULL` first — run the `ALTER COLUMN … SET NOT NULL` line above it |
| Foreign key rejected | Create `fact_orders` after all three dimensions; the notebook drops the fact first for exactly this reason |
| No *Entity relationship diagram* on the table page | It appears once at least one foreign key with `RELY` exists; refresh the Catalog page |
| `orders_metrics` not listed when adding a dashboard data source | Lab 02 part C not done, or the warehouse cannot read it — check `SELECT MEASURE(revenue)` works in SQL Editor first |
| Dashboard shows no data after publishing | Publish with *embed credentials* off, then confirm `bootcamp_analysts` has `SELECT` from lab 02 part A |
| Genie answers with the wrong revenue | Add an instruction pinning revenue to the governed measure, and save a trusted SQL example |
| Benchmarks never finish | Free Edition has one 2X-Small warehouse — run benchmarks when no pipeline or job is running |
