# The two ways to do each lab

| | `README.md` — **technical track** | `UI-GUIDE.md` — **business track** |
|---|---|---|
| For | Data engineers, analysts who code, ML engineers | Business analysts, product owners, domain experts, managers |
| You work in | Notebooks, SQL files, YAML, terminal, Git | Only the Databricks and GitHub web pages |
| Data | You build it step by step (starts from `main`) | Ready-made: one click builds it all (branch `solution`, job `business_quickstart`) |
| Focus | *How* it is built | *What* it means for the business, *how* to use it, *what* to ask for |

Both tracks use **your own** Databricks Free Edition workspace and **your own** GitHub account (see [lab 00](lab-00-prerequisites/README.md)).

## Reading the business guides
* **Bold** = a button, menu, tab or field to click. `→` = then click.
* *Italic* = text to type.
* 📋 = copy-paste this exactly (no need to understand the code).
* 💬 = a question to discuss with your group.
* `<you>` = the part of your sign-in e-mail before the `@`, with dots replaced by `_` (e.g. `ana.lopez@…` → `ana_lopez`).
* Your data lives in catalog **bootcamp_dev**, schema **dev_<you>_sales**.
* Your SQL warehouse is **Serverless Starter Warehouse** (Free Edition has exactly one).

Databricks renames and moves buttons from time to time. If a label differs, look for the closest match or use the
search bar at the top of the workspace — and ask your instructor.

## The bundle "Deployments" panel (used in lab 00 and lab 06)
Open `databricks.yml` in your Git folder: the right-hand panel shows **Deployments**.

| Control | What it does |
|---------|--------------|
| **Target** | which environment: always **dev** when you click it yourself |
| **Deploy** | creates or updates everything declared in the project — shows you the list first |
| **Bundle resources** → ▶ **Run** | starts a job or pipeline |
