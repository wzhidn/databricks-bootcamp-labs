# Lab 06 (optional path) · CI/CD with Azure DevOps
**Technical track · 60 min · replaces Part D of the GitHub lab** · checkpoint: `checkpoint/lab-06-devops`

**Goal:** the same pipeline as the GitHub lab — tests, plan, staging + integration run, approval, prod, rollback —
built with **Azure Pipelines** in your **own Azure DevOps organisation**, deploying to your **Free Edition** workspace.
Your code can stay in your GitHub repository.

```
PR to main ─────▶ Test · Validate & plan (staging)
push to main ───▶ Test · Deploy staging + integration run ──approval──▶ Deploy prod
manual run ─────▶ azure-pipelines-rollback.yml: redeploy prod from any commit/tag
```

## Before you start
* Lab 00 done (catalogs exist, a Databricks personal access token generated).
* A free **Azure DevOps organisation** (dev.azure.com → *Start free* with your Microsoft or GitHub account) and a project.
* **Hosted build minutes:** new organisations must request the free Microsoft-hosted parallel job
  (https://aka.ms/azpipelines-parallelism-request — approval can take 2–3 business days). **Request it before the
  bootcamp**, or register your laptop as a self-hosted agent (*Project settings → Agent pools → Default → New agent*)
  and replace `vmImage: ubuntu-latest` with `name: Default`.

### Authentication
Free Edition runs on AWS and has no account console, so neither Azure service connections (`azure-cli` auth) nor
OIDC federation apply. The pipeline uses your Databricks token stored as a **secret variable** in a variable group
(optionally in Azure Key Vault). Secret variables are never printed and must be mapped explicitly into `env:`.

## Steps

### 1 · Variable group and environments (10 min)
1. **Pipelines → Library → + Variable group** `bootcamp-databricks`:
   `DATABRICKS_HOST` = workspace URL; `DATABRICKS_TOKEN` = token → click the 🔒 to make it **secret** → **Save**.
2. **Pipelines → Environments**: create `bootcamp-staging` and `bootcamp-prod`.
   On `bootcamp-prod` → **Approvals and checks → Approvals** → add yourself.

### 2 · Add the pipeline files (5 min)
```bash
git checkout -b ci/add-azure-pipeline
mkdir -p .azure-pipelines/templates
cp labs/lab-06-devops/azure-devops/azure-pipelines*.yml .azure-pipelines/
cp labs/lab-06-devops/azure-devops/templates/install-databricks-cli.yml .azure-pipelines/templates/
git add .azure-pipelines && git commit -m "Add Azure Pipelines CI/CD" && git push -u origin ci/add-azure-pipeline
```

### 3 · Create the pipeline (5 min)
**Pipelines → New pipeline → GitHub** (authorise the Azure Pipelines app for your repo) or **Azure Repos Git** →
**Existing Azure Pipelines YAML file** → branch `ci/add-azure-pipeline`, path `/.azure-pipelines/azure-pipelines.yml` →
**Save**. On first run, **Permit** access to the variable group and environments.

### 4 · PR, staging, approval, prod (25 min)
Open a PR to `main` → stages **Test** (see **Tests** tab) and **Validate & plan** run. Merge → **Deploy to staging**
(deploy + `bundle run orders_job`) → **Deploy to prod** waits for your approval → approve.

### 5 · Break it, then roll back (15 min)
Set `max_drop_rate: "0.001"` → PR → merge → staging fails, prod not touched → revert → green.
Create a second pipeline from `/.azure-pipelines/azure-pipelines-rollback.yml` and run it with an earlier commit SHA.

## Done when
- [ ] PR validation shows tests and the plan
- [ ] Staging deployed and the integration run passed
- [ ] Prod deployed after approval
- [ ] A failing change was stopped at staging, and a rollback was performed

## Troubleshooting
| Symptom | Fix |
|--------|-----|
| *No hosted parallelism has been purchased or granted* | Request the free grant (link above) or use a self-hosted agent |
| `cannot configure default credentials` | The secret must be mapped in `env:` (`DATABRICKS_TOKEN: $(DATABRICKS_TOKEN)`) |
| Pipeline waits on "permission needed" | **View** → **Permit** the variable group / environment |
| Template not found | `templates/install-databricks-cli.yml` must sit under `.azure-pipelines/templates/` |

## Enterprise variant (for reference)
With Azure Databricks: an ARM service connection using workload identity federation + `AzureCLI@2` and
`DATABRICKS_AUTH_TYPE: azure-cli` — no secrets stored in Azure DevOps.
