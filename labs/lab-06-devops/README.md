# Lab 06 · DevOps with Declarative Automation Bundles — technical track
**Deck section: DevOps – DABs (Lab · DevOps) · 90 min** · checkpoint: `checkpoint/lab-06-devops`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md) — act as the business approver of a release.

**Goal:** put the whole bootcamp solution under code, deploy it to **dev**, and ship it through **GitHub Actions** to
**staging** and **prod** in your Free Edition workspace — with tests, a reviewed plan, an approval gate and a rollback.

Cheat sheet: [cheatsheet.md](cheatsheet.md) · Azure DevOps instead of GitHub: [azure-devops/README.md](azure-devops/README.md)

```
feature branch ──PR──▶ unit tests · validate · plan(staging)
        main ──push──▶ unit tests · deploy staging · integration run ──your approval──▶ deploy prod
  manual run ────────▶ rollback prod to any commit/tag
```

## What you build
| Artifact | Where |
|----------|-------|
| `resources/orders.job.yml` — `orders_job`, 3 tasks, daily trigger | you author it in part A |
| `my_first_job` adopted from the UI without duplicating it | part B |
| `.github/workflows/bundle-cicd.yml` + `bundle-rollback.yml` | part D |
| `[staging]` and `[prod]` deployments of the whole bundle | parts D–E |

## Prerequisites
* Labs 01–05 done, or start from `checkpoint/lab-06-devops`.
* Lab 00 parts 4–5: GitHub variable `DATABRICKS_HOST`, secret `DATABRICKS_TOKEN`, and the `staging` / `prod`
  environments. Without these, part D fails at the first workflow run.
* A public repo if you want the prod approval gate; on GitHub Free, private repos have no environments — use
  `bundle-cicd-private.yml` instead.
* Databricks CLI ≥ 1.14 (lab 00 part 6) if you work locally rather than in the Git folder.

## Part A · Author a job by hand (15 min)
Create `resources/orders.job.yml`: job `orders_job` with tasks `generate_batch` (notebook `00_generate_data.py`,
`batch = {{job.parameters.batch}}`, `with_coupon=true`) → `refresh_pipeline` (`${resources.pipelines.orders_pipeline.id}` —
never an ID) → `quality_checks` (`99_quality_checks.py`, `max_drop_rate: "0.05"`), daily trigger, `max_concurrent_runs: 1`.
```bash
databricks bundle validate && databricks bundle plan && databricks bundle deploy
databricks bundle run orders_job --params batch=2
```
`[dev <you>] orders_job`: schedule **paused** — development mode.

## Part B · Bring UI-created assets under code (15 min)
1. In the UI, create a job *my_first_job* running `src/notebooks/_setup` on serverless.
2. Generate and bind it — the deploy then **updates** it instead of creating a duplicate:
   ```bash
   databricks jobs list --name my_first_job
   databricks bundle generate job --existing-job-id <id> --key my_first_job
   databricks bundle deployment bind my_first_job <id>
   databricks bundle plan        # "update", not "create"
   ```
3. Same for your lab 03 dashboard and Genie Agent:
   `bundle generate dashboard --existing-path "…/Sales overview (<you>).lvdash.json" --key sales_overview`,
   `bundle generate genie-space --existing-id <id> --key sales_genie`. Examples: [examples/](examples/).

## Part C · Environments (10 min)
Read the `staging` and `prod` targets in `databricks.yml`: own catalog, `mode: production`, own root path, presets
(name prefix, tags, paused triggers), optional `run_as`. Then:
```bash
databricks bundle validate -t staging
databricks bundle plan -t staging     # what CI will create in bootcamp_staging
```
Set `bundle.name` to something unique if you share a workspace (you don't in Free Edition).

## Part D · CI/CD with GitHub Actions (30 min)
Prerequisites: lab 00 parts 4–5 (variable `DATABRICKS_HOST`, secret `DATABRICKS_TOKEN`, environments).

| Your repo | Workflow | Prod gate |
|-----------|----------|-----------|
| Public | `github/bundle-cicd.yml` + `github/bundle-rollback.yml` | environment `prod`, you as required reviewer |
| Private (GitHub Free) | `github/bundle-cicd-private.yml` | manual run with `deploy_prod = yes` |

```bash
git checkout -b ci/add-pipeline
mkdir -p .github/workflows
cp labs/lab-06-devops/github/bundle-cicd.yml labs/lab-06-devops/github/bundle-rollback.yml .github/workflows/
git add -A && git commit -m "Bundle + CI/CD" && git push -u origin ci/add-pipeline
```
Open a PR → **unit-tests** + **plan-staging** (read the plan in the run **Summary**) → merge → **deploy-staging** runs
`orders_job` as an integration test → **deploy-prod** waits → **Review deployments** → approve.

**Why a secret and not OIDC?** OIDC workload identity federation needs an account-level federation policy; Free Edition
has no account console. The workflow is otherwise identical — see *Enterprise variant* below.

## Part E · Break it, then roll back (15 min)
1. Set `max_drop_rate: "0.001"` → PR → merge → staging's integration run fails → prod is never deployed.
2. Revert → green: Open the merged PR and click Revert. Merge the PR that GitHub creates.
3. **Actions → bundle-rollback → Run workflow** with an earlier good SHA (Git commit unique ID) (private repo:
   `bundle-cicd-private` with `deploy_prod = yes`, `git_ref = <sha>`).

## Stretch
* [advanced/](advanced/README.md): Python-defined resources and mutators.
* Service principal identity (lab 00, option B): `run_as` in staging/prod — jobs no longer run as a person.
* Add the serving endpoint to staging/prod after the first training run.

## Done when
- [ ] `orders_job` runs green in dev; `my_first_job` managed without duplicates
- [ ] PR shows tests and the plan; staging deployed and integration run passed
- [ ] Prod deployed after approval; failing change stopped at staging; rollback performed

## Troubleshooting
| Symptom | Fix |
|--------|-----|
| `cannot configure default credentials` | `DATABRICKS_HOST` must be a **variable**, `DATABRICKS_TOKEN` a **secret** |
| `Invalid access token` | Token expired — generate a new one, update the secret |
| `CREATE SCHEMA` denied on `bootcamp_staging` | Run `setup/free_edition_setup`; with a service principal, grant it the catalog privileges |
| Pipeline limit error in staging | One active pipeline per type — don't run dev and staging pipelines together |
| Private repo on `checkpoint/lab-06-devops` | That branch ships the public workflows — replace them with `bundle-cicd-private.yml` |

## Enterprise variant
Separate staging/prod workspaces, one service principal per environment and no secrets:
```yaml
permissions: {id-token: write, contents: read}
env:
  DATABRICKS_AUTH_TYPE: github-oidc
  DATABRICKS_HOST: ${{ vars.DATABRICKS_HOST }}
  DATABRICKS_CLIENT_ID: ${{ vars.DATABRICKS_CLIENT_ID }}
```
+ an account-level federation policy with subject `repo:<owner>/<repo>:environment:<env>`.
