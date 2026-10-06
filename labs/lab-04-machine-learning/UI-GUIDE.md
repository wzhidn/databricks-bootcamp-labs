# Lab 04 · Predicting customer churn — business track
**Deck section: Machine Learning · 45 min · no code** · [How to read this guide](../UI-CONVENTIONS.md)
Prerequisite: `business_quickstart` ran (it trained the model for you).

**What you will learn:** how a machine-learning model is built, tracked and governed; how to read its quality; how to use
its predictions — and what questions a business owner should ask before trusting it.

## 1 · Where the model came from (10 min)
1. Left sidebar **Experiments** → *bootcamp-churn* (or open **Catalog → churn_model → Versions → Source run**).
2. Open the latest **run** → **Overview**: metric **test_auc**. 0.5 = coin toss, 1.0 = perfect. Anything above ~0.75 is
   useful for prioritising, not for automatic decisions.
3. **Artifacts** → the model files; **Inputs**: which data it learned from.

💬 Which mistake is more expensive for you: calling a loyal customer "at risk", or missing one who is about to leave?

## 2 · The model is governed like data (5 min)
4. **Catalog** → **dev_<you>_sales** → **Models** → **churn_model** → **Versions**: version 1 carries the alias
   **@champion** — the one applications use.
5. **Lineage**: the model links back to the feature table and to the orders it was trained on.

## 3 · Use the predictions (15 min)
6. **SQL Editor** → 📋 (replace `<you>`):
   ```sql
   SELECT c.segment, c.region,
          sum(p.churn_predicted)                 AS customers_at_risk,
          count(*)                               AS customers,
          round(avg(p.churn_predicted) * 100, 1) AS pct_at_risk
   FROM bootcamp_dev.dev_<you>_sales.churn_predictions p
   JOIN bootcamp_dev.dev_<you>_sales.dim_customer c USING (customer_id)
   GROUP BY ALL ORDER BY customers_at_risk DESC;
   ```
7. Click **[⋮]** top right → **file** → **Add to dashboard** → your *Sales overview* → a new "customers at risk" chart.
8. *(optional)* Ask your Genie Agent (lab 03) after adding `churn_predictions` to it: *"Which enterprise customers are at
   risk in EMEA?"*

## 4 · Forecast revenue in one query (10 min) — *if AI Functions are available*
9. **SQL Editor** → 📋
   ```sql
   SELECT * FROM ai_forecast(
     observed  => TABLE(SELECT order_date AS ds, sum(amount) AS revenue
                        FROM bootcamp_dev.dev_<you>_sales.fact_orders GROUP BY ALL),
     horizon   => '2026-12-31',
     time_col  => 'ds',
     value_col => 'revenue');
   ```
   Show it as a line chart (**+** → **Visualization**).

## 5 · A business owner's model checklist (5 min)
💬 Discuss and fill in for the churn model:
| Question | Answer |
|----------|--------|
| What decision will the prediction support? | |
| What quality (AUC) is "good enough" for that decision? | |
| How often must it be retrained, and who approves a new version? | |
| How do we switch back if the new version is worse? (hint: the **@champion** alias) | |

## Take-aways
- Every training run is tracked (MLflow): results are reproducible and comparable.
- Models are governed in Unity Catalog like tables: permissions, lineage, versions, aliases.
- Business owns the *decision* and the *acceptance criteria*, not the algorithm.
