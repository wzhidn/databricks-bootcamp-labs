# Lab 03 · Self-service analytics with dashboards and Genie — business track
**Deck section: Business Intelligence · 60 min · no code** · [How to read this guide](../UI-CONVENTIONS.md)

**What you will learn:** build a governed dashboard in minutes, set up a **Genie Agent** that answers business questions
in plain English — and *test* it before you let colleagues rely on it.

## 1 · The data model behind your reports (5 min)
1. **Catalog** → **dev_<you>_sales** → **fact_orders** → **Overview**. The key icons show how orders link to customers,
   products and dates — a **star schema** (see the slide). Open the *relationship diagram* if shown.

💬 Which "dimensions" does your business slice by every week (region, product line, channel…)?

## 2 · Build a dashboard (20 min)
2. Left sidebar **Dashboards** → **Create dashboard**.
3. **Data** tab → **Add data source** → search *orders_metrics* → select it.
4. **Canvas** tab → **Add a visualization** → in the widget panel:
   * *Line* chart: X = **order_month**, Y = **revenue**
   * *Bar* chart: X = **region**, Y = **revenue**
   * *Counter*: **avg_order_value**
   Tip: type what you want in the **AI** prompt of the widget, e.g. *"revenue by region as a bar chart"*.
5. **Add a filter** → field **channel**.
6. Rename the dashboard *Sales overview (<you>)* → **Publish** → **Share** → *bootcamp_analysts* → **Can view**.

💬 Every chart uses the governed *revenue* from lab 02. What disagreements in your meetings would that end?

## 3 · Set up a Genie Agent (20 min)
7. Left sidebar **Genie** → **New** → add *orders_metrics*, *fact_orders*, *dim_customer*, *dim_product*, *dim_date* →
   **Create**. Name it *Sales assistant (<you>)*.
8. **Instructions** → write, in plain business language:
   *Revenue always means the governed revenue measure. Use calendar months. Answer in EUR. If a question is ambiguous, ask.*
9. **Chat**: ask *"What was revenue by region last month?"* → open **Show code** to see the query Genie wrote.
10. Ask a trickier one: *"Which segment has the highest average order value on mobile?"*

## 4 · Test it before you share it (10 min)
11. **Benchmarks** → **Add benchmark** → enter a question and the answer you *know* is right (check it on your dashboard).
    Add 3–5 of them.
12. **Run benchmarks** → review which ones fail → improve the **Instructions** → run again.
13. **Share** → *bootcamp_analysts* → **Can run**.

## 5 · Ask Genie One (5 min) — *if available*
14. Open **Genie One** (app switcher / *Genie One* in the sidebar) → ask *"How is revenue trending this quarter?"*
    It uses your Genie Agent and dashboard, with your permissions.
15. *(optional)* In Excel or Google Sheets with the Databricks add-in, ask the same question.

## Take-aways
- Dashboards and Genie sit on the same governed definitions — one truth, many ways to consume it.
- Genie Agents are *curated* by the business: instructions + benchmarks = an assistant you can trust.
- Always open **Show code**: transparency is what makes AI answers auditable.
