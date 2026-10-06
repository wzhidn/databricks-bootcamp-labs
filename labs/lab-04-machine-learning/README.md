# Lab 04 · Machine Learning — technical track
**Deck section: Machine Learning (Lab · Machine Learning) · 75 min** · checkpoint: `checkpoint/lab-04-ml`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** engineer governed features, train and track a churn model with **MLflow 3**, register it in **Unity Catalog**
with aliases (not stages — the workspace registry is legacy), score in batch, serve it, and roll it back — all as code.

Notebook: `src/notebooks/04_ml_training.py` (TODOs marked `lab-04`). Run on **Serverless**.

## Part A · Features and training (35 min)
1. Compute customer features from `orders_enriched` (orders, revenue, recency, category breadth, mobile share).
2. Register `customer_features` as a **feature table in Unity Catalog** (primary key `customer_id`).
3. Build a training set with a `FeatureLookup` — only `customer_id` and the label are passed in.
4. Train a gradient-boosted classifier; the run logs `test_auc` to MLflow. Register two models:
   `churn_model_fs` (carries its feature lookups — batch scoring) and `churn_model` (plain sklearn — real-time serving).
5. Set the `@champion` alias; batch-score with `fe.score_batch` → table `churn_predictions`.

## Part B · ML as code (25 min)
Create `resources/ml.yml` (reference: `checkpoint/lab-04-ml`): an **experiment**, a **job** `train_churn_model` running the
notebook, and — under `targets.dev.resources` — a **serving endpoint** `churn-endpoint` (deployed as
`dev_<you>_churn-endpoint`) with an inference table. The endpoint lives in dev only because the model must exist first.
```bash
databricks bundle plan && databricks bundle deploy
```
Query the endpoint (**Serving → Query** with the model's input example) and inspect `churn_endpoint_payload`.

## Part C · Retrain, promote, roll back (15 min)
```bash
databricks bundle run train_churn_model                  # new version becomes @champion
databricks bundle deploy --var="churn_model_version=2"   # serve it
databricks bundle deploy --var="churn_model_version=1"   # roll back = redeploy
```
Batch consumers that load `models:/…@champion` roll back by moving the alias.

> **Free Edition:** CPU serving only, limited number of endpoints; online tables are not available (online features
> need your one Lakebase project — optional). If the endpoint can't be created, keep Part B as a demo.

## Stretch
* **AI Runtime** (serverless GPU, Preview) and **Genie Code for ML**: ask Genie Code to rewrite training with LightGBM.
* Production monitoring for the model's inference table.

## Done when
- [ ] `customer_features` has a primary key; AUC visible in the experiment
- [ ] `churn_model@champion` set; `churn_predictions` table exists
- [ ] Endpoint served v2, then rolled back to v1 by redeploying
