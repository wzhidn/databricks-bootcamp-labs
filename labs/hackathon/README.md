# Hackathon

> 🖱️ UI step-by-step: [UI-GUIDE.md](UI-GUIDE.md)

**Day 3 · 1:45 – 4:50 PM · mixed teams (1 business product owner + 3–4 engineers)**

## Timeline
| Time | Step |
|------|------|
| 1:45 | Briefing — challenges come from the business track's use-case canvases; teams formed |
| 2:00 | **Sprint 1** — ingest, model, govern; everything in your team's bundle from the first commit |
| 3:30 | Break — mentors run a governance & cost check with each team |
| 3:45 | **Sprint 2** — build the experience (dashboard, Genie Agent, agent or app); merge → CI deploys staging |
| 4:25 | Demos — 5 minutes per team, show the CI run and the deployed resources |
| 4:50 | Close-out |

## Working as a team with personal accounts
Every trainee has their own Free Edition workspace and GitHub account, so a team works like an open-source project:

| Role | Setup |
|------|-------|
| **Repo owner** (one engineer) | Uses their lab 06 repository (CI/CD configured). **Settings → Collaborators → Add people** → teammates (Write). The repo's CI secrets point to the **owner's** workspace — staging/prod live there. |
| **Teammates** | Accept the invitation → in *their own* workspace: **Create → Git folder** from the owner's repo → deploy to **their own dev** target. |
| **Product owner** (business track) | Collaborator too; follows the lab 06 business guide to review and approves the `prod` environment (add as required reviewer in **Settings → Environments → prod**). |

Everyone develops in an isolated dev workspace, integrates through pull requests, and CI deploys the merged result to
the owner's staging and prod — the same flow as in a company, with workspaces instead of catalogs as the dev boundary.

## Rules
1. Start from the owner's lab 06 repository (or `checkpoint/lab-06-devops`). One repository per team.
2. **Everything ships through the pipeline to staging.** Nothing is created by hand in staging or prod.
3. At least one unit test for any new Python logic, and at least one expectation for any new table.
4. Data stays in Unity Catalog with correct permissions; PII is tagged and masked.
5. Use serverless and tag your resources (`project=bootcamp`, `team=<name>`).

## Building blocks
Starter repo (this one) · Auto Loader / pipelines · metric views · AI/BI dashboards · Genie Agents ·
the lab 05 agent pattern · AI Functions (`ai_classify`, `ai_extract`, `ai_summarize`) · Foundation Model APIs ·
Databricks Apps (≤ 3) · Lakebase (1 project) · MLflow 3.

**Free Edition quotas per workspace:** 5 concurrent job tasks, one active pipeline per type, one 2X-Small SQL
warehouse, limited serving endpoints — plan runs so they don't collide.

## Suggested challenges (if the business track produces fewer than needed)
1. **Churn early-warning** — score customers daily with `churn_model_fs`, surface at-risk enterprise customers in a
   Genie Agent and a dashboard for account managers.
2. **Support copilot** — extend the lab 05 agent with order lookups and refund eligibility; evaluate it with 10 benchmark questions.
3. **Coupon effectiveness** — analyse `coupon_code` impact on order value with metric views; recommend which coupon to keep.
4. **Regional manager app** — a Databricks App on Lakebase where managers annotate anomalies in regional revenue.

See [judging.md](judging.md) and [use-case-canvas.md](use-case-canvas.md).
