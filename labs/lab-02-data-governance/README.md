# Lab 02 · Data Governance — technical track
**Deck section: Data Governance (Lab · Data Governance) · 45 min** · checkpoint: `checkpoint/lab-02-governance`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** secure, classify and give business meaning to the tables built in lab 01 — privileges, tags, column masks,
a governed **metric view**, glossary and lineage.

Notebook: `src/notebooks/02_governance.py` (TODOs marked `lab-02`). Prerequisites: lab 01; groups `bootcamp_engineers`
(with you in it) and `bootcamp_analysts` (lab 00, 2.5).

> **Free Edition:** you are the workspace admin. Domains, Business Glossary and ABAC are Preview/Beta — enable them under
> **Settings → Previews** if offered; otherwise skip the steps marked *optional*.

## Steps
1. **Privileges.** Section 1: `bootcamp_analysts` → `USE SCHEMA, SELECT`; `bootcamp_engineers` → `USE SCHEMA, SELECT,
   MODIFY, CREATE TABLE`. Verify with `SHOW GRANTS`.
2. **Tags.** Section 2: tag `customer_profiles.email` and `last_name` with `pii`.
3. **Column mask.** Complete `mask_email()` (`is_account_group_member('bootcamp_engineers')`) and apply it with
   `ALTER TABLE … ALTER COLUMN email SET MASK`. You see full e-mails; remove yourself from `bootcamp_engineers`
   (**Settings → Identity and access → Groups**), wait a minute, re-run: masked. Add yourself back.
4. **ABAC** *(optional)*: one policy for every column tagged `pii` instead of per-table masks; try a tag automation rule.
5. **Metric view.** Section 3: `orders_metrics` on `orders_enriched` (`version: 1.1`), query with `MEASURE(revenue)`.
6. **Domain & glossary** *(optional, UI)*: add your schema to a *Sales* domain; create the glossary term *Revenue* and link
   it to the `revenue` measure.
7. **Lineage.** `orders_metrics` → **Lineage** → trace back to the raw volume.
8. **Break & fix.** `REVOKE SELECT ON TABLE customer_profiles FROM bootcamp_analysts` → find the impact with Lineage and
   Permissions → grant it back.

## Done when
- [ ] Masking changes with group membership
- [ ] `SELECT MEASURE(revenue) FROM orders_metrics` works
- [ ] Lineage reaches the raw volume

> If your workspace rejects `version: 1.1` in the metric view YAML, use the version shown in the metric view docs.
