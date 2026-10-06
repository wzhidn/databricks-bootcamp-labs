# Lab 02 · Data Governance — technical track
**Deck section: Data Governance (Lab · Data Governance) · 45 min** · checkpoint: `checkpoint/lab-02-governance`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** secure, classify and give business meaning to the tables built in lab 01 — privileges, tags, column masks,
a governed **metric view**, glossary and lineage.

## What you build
| Artifact | Where |
|----------|-------|
| Grants for `bootcamp_analysts` and `bootcamp_engineers` | `src/notebooks/02_governance.py` section 1 |
| `pii` tags on `customer_profiles.email` and `last_name` | section 2 |
| `mask_email()` column mask | section 2 |
| `orders_metrics` metric view | section 3 |

`orders_metrics` is the governed definition of revenue. Lab 03's dashboard and Genie Agent both read it, so the
numbers in every later lab come from here.

## Prerequisites
* Lab 01 done — `orders_enriched` and `customer_profiles` exist and have rows.
* Groups `bootcamp_engineers` (with you in it) and `bootcamp_analysts` exist (lab 00, part 2.5).
* Notebook: `src/notebooks/02_governance.py`, TODOs marked `lab-02`.

> **Free Edition:** you are the workspace admin. Domains, Business Glossary and ABAC are Preview/Beta — enable them under
> **Settings → Previews** if offered; otherwise they stay in *Stretch* below.

## Part A · Privileges and tags (15 min)
1. **Privileges.** Section 1: `bootcamp_analysts` → `USE SCHEMA, SELECT`; `bootcamp_engineers` → `USE SCHEMA, SELECT,
   MODIFY, CREATE TABLE`. Verify with `SHOW GRANTS`.
2. **Tags.** Section 2: tag `customer_profiles.email` and `last_name` with `pii`.

## Part B · Mask the sensitive columns (10 min)
3. **Column mask.** Complete `mask_email()` (`is_account_group_member('bootcamp_engineers')`) and apply it with
   `ALTER TABLE … ALTER COLUMN email SET MASK`. You see full e-mails; remove yourself from `bootcamp_engineers`
   (**Settings → Identity and access → Groups**), wait a minute, re-run: masked. Add yourself back.

## Part C · A governed metric view (10 min)
4. **Metric view.** Section 3: `orders_metrics` on `orders_enriched` (`version: 1.1`), query with `MEASURE(revenue)`.

## Part D · Lineage, break and fix (10 min)
5. **Lineage.** `orders_metrics` → **Lineage** → trace back to the raw volume.
6. **Break & fix.** `REVOKE SELECT ON TABLE customer_profiles FROM bootcamp_analysts` → find the impact with Lineage and
   Permissions → grant it back.

## Stretch
* **ABAC:** one policy for every column tagged `pii` instead of per-table masks; try a tag automation rule.
* **Domain & glossary** (UI): add your schema to a *Sales* domain; create the glossary term *Revenue* and link it to the
  `revenue` measure.

## Done when
- [ ] Masking changes with group membership
- [ ] `SELECT MEASURE(revenue) FROM orders_metrics` works
- [ ] Lineage reaches the raw volume

## Troubleshooting
| Symptom | Fix |
|--------|-----|
| `Table or view not found: orders_enriched` | Lab 01 part B not finished — the gold materialized view is missing |
| E-mails still unmasked after leaving the group | Group membership is cached for about a minute; wait and re-run the cell |
| `is_account_group_member` returns false for everyone | You are checking a workspace-local group name — use the exact group name from **Settings → Identity and access → Groups** |
| Metric view rejected: unknown `version` | Use the version shown in the metric view docs for your workspace release; `1.1` is correct as of Sep 2026 |
| `WITH METRICS LANGUAGE YAML` is a syntax error | Metric views are a Preview — enable them under **Settings → Previews** |
| No **Domains** or **Business glossary** in the sidebar | Not offered in your Free Edition workspace; skip the Stretch item |
| `GRANT` fails on the schema | You must own the schema — check you deployed the bundle to **dev**, not staging |
