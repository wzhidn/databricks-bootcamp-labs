# Lab 06 · Releasing changes safely — you are the business approver
**Deck section: DevOps – DABs · 45 min · no code** · [How to read this guide](../UI-CONVENTIONS.md)
Prerequisites: lab 00 business path, including part **E** (GitHub variable, secret and environments).

**What you will learn:** how data and AI changes travel from **dev** to **staging** to **prod**, what automated checks
protect you, and how *you* approve — or stop — a release. You never touch production by hand.

## 1 · Release the course solution to staging (15 min)
1. github.com → your repository → **Pull requests** → **New pull request**.
2. *base:* **main** ← *compare:* **solution** → **Create pull request** → title *Release v1* → **Create pull request**.
3. Wait for the checks (≈ 3 min): **unit-tests** ✅ and **plan-staging** ✅. Click **Details** next to *plan-staging* →
   **Summary**: the *Bundle plan* lists everything that will be created in staging — jobs, pipeline, tables' schema.
4. 💬 As an approver, what would you look for in this list?
5. **Merge pull request** → **Confirm merge**.
6. **Actions** tab → the new run → **deploy-staging**: it deploys and runs the full pipeline as a rehearsal
   (*Integration run*).
7. Databricks → **Jobs & Pipelines** → search *staging* → `[staging] orders_job` ✅. **Catalog** → **bootcamp_staging**
   → **sales**: the tables exist — completely separate from your **dev** data.

## 2 · Approve production (5 min)
8. GitHub → the same run → **deploy-prod** shows *Waiting* → **Review deployments** → tick **prod** → comment
   *Staging checked* → **Approve and deploy**.
9. Databricks: `[prod] orders_job` exists (paused); **bootcamp_prod** → **sales** exists.

## 3 · Change a business rule — as code (10 min)
The quality check allows at most **5 %** rejected orders before a release is blocked. The business wants **2 %**.
10. GitHub → **Code** → `resources/orders.job.yml` → ✏️ **Edit** → change `max_drop_rate: "0.05"` to `"0.02"` →
    **Commit changes…** → *Create a new branch* → **Propose changes** → **Create pull request**.
11. Checks pass → **Merge** → staging rehearsal passes (the real rejection rate is ~1 %) → **approve prod**.
    The rule change is now reviewed, tested, approved and traceable in history.

## 4 · See the safety net stop a bad release (10 min)
12. Repeat step 10 with an impossible rule: `"0.001"` (0.1 %) → merge.
13. **Actions**: *deploy-staging* ❌ fails at *Integration run* → *deploy-prod* is **skipped**. Production is untouched.
14. Open the merged pull request → **Revert** → **Create pull request** → **Merge**: back to green.

## 5 · Discuss (5 min)
💬 Map this flow to your organisation:
| Step here | Who does it in your company? |
|-----------|------------------------------|
| Propose a change (pull request) | |
| Review the plan | |
| Automated rehearsal in staging | |
| Approve production | |
| Roll back | |

## Take-aways
- Changes to data, pipelines, dashboards and AI are *code*: reviewed, tested and versioned like software.
- Staging is a full rehearsal; a failing check automatically blocks production.
- The business approves releases with one click — and can see exactly what changed and when.
