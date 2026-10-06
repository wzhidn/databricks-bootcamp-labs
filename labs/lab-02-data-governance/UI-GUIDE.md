# Lab 02 · Trustworthy, protected data — business track
**Deck section: Data Governance · 45 min · no code** · [How to read this guide](../UI-CONVENTIONS.md)

**What you will learn:** how to find data you can trust, who can see what (and why), how sensitive data is protected
automatically, and how one KPI definition is shared by every report and AI assistant.

## 1 · Find and understand data (10 min)
1. Top search bar → type *revenue* → open **orders_metrics** (a *metric view*).
2. **Overview** tab: read the description, owner and columns. Click **AI generate** next to an empty description if
   offered — then edit it in business words and **Save**.
3. Open **orders_silver** → **Sample data**. Open **History**: who changed it and when.

💬 What information must a table page show before you would trust it for a board report?

## 2 · Label sensitive data (5 min)
4. **customer_profiles** → **Columns** → row **email** → **Tags** → **Add tag** → key *pii*, value *email* → **Save**.
   (The course script already added it — check it is there, then add *pii = name* on **last_name**.)

## 3 · See protection in action (10 min)
5. **customer_profiles** → **Sample data**: you see full e-mail addresses because you belong to *bootcamp_engineers*.
6. **avatar** → **Settings** → **Identity and access** → **Groups** → **bootcamp_engineers** → remove yourself.
   Wait one minute → back to **Sample data**: e-mails now show as `***@example.com`.
7. Add yourself back to the group.

💬 The rule is defined once, on the data. Why is this safer than hiding the column in each report?

## 4 · Give access the right way (5 min)
8. **Catalog** → **dev_<you>_sales** → **Permissions** → **Grant** → *bootcamp_analysts* → tick **SELECT** and
   **USE SCHEMA** → **Confirm**. Analysts can now read — but not change — everything in the schema.

## 5 · One KPI definition for everyone (10 min)
9. Open **orders_metrics** → **Overview**: *revenue*, *order_count* and *avg_order_value* are defined **once** here.
10. **SQL Editor** → 📋
    ```sql
    SELECT order_month, region, MEASURE(revenue) AS revenue
    FROM bootcamp_dev.dev_<you>_sales.orders_metrics
    GROUP BY ALL ORDER BY order_month;
    ```
    Replace `<you>`, then **Run**. Dashboards, Genie and apps will all use this same definition (lab 03).
11. *(optional, if listed)* **Catalog** → **Business glossary** → **New term** → *Revenue* — *Sum of order amounts after
    data-quality checks* → **Link** to `orders_metrics.revenue`. **Domains** → add your schema to a *Sales* domain.

## 6 · Where does this number come from? (5 min)
12. **orders_metrics** → **Lineage** tab → **See lineage graph** → expand to the left until you reach the raw files.

💬 Your CFO asks "where does this revenue figure come from?" — how long would that answer take today?

## Take-aways
- Governance is attached to the data, not to each report.
- Sensitive columns are protected by rule and by tag, for every tool at once.
- A metric view makes "revenue" mean the same thing everywhere — including for AI.
