# Lab 00 · Prerequisites: Databricks Free Edition + your GitHub account
**Before Day 1 · 60–75 min · everyone (technical and business tracks)**

> 🖱️ **Business track?** Follow the click-by-click [UI-GUIDE.md](UI-GUIDE.md) instead — same result, no terminal.

Every trainee works in **their own Databricks Free Edition workspace** and **their own GitHub account**. Nothing is
shared, so nothing you do can break someone else's lab. This page prepares everything the labs need, including the
**dev / staging / prod** environments used by Declarative Automation Bundles (DABs) and CI/CD.

| Part | What | Time | Needed for |
|------|------|------|-----------|
| [1](#part-1--github-your-copy-of-the-lab-repository) | GitHub: your copy of the lab repository | 10 min | all labs |
| [2](#part-2--databricks-free-edition-workspace) | Free Edition: workspace, Git folder, catalogs, groups, warehouse | 20 min | all labs |
| [3](#part-3--choose-your-track) | Choose your track (technical: `main` · business: `solution` + one-click data) | 5–20 min | all labs |
| [4](#part-4--credentials-for-cicd) | Credentials for CI/CD | 5 min | lab 06 |
| [5](#part-5--github-actions-variables-secrets-environments) | GitHub Actions: variables, secrets, environments | 10 min | lab 06 |
| [6](#part-6--optional-databricks-cli-on-your-laptop) | *(optional)* Databricks CLI on your laptop | 10 min | labs 01, 06 |
| [7](#part-7--verify) | Verify | 5 min | — |

---

## How dev, staging and prod are isolated in one Free Edition workspace

Free Edition gives you **one workspace** and no account console, so we cannot use one workspace per environment.
The bundle isolates the three environments **inside** your workspace on every layer that matters:

| Layer | dev | staging | prod |
|-------|-----|---------|------|
| **Catalog** | `bootcamp_dev` | `bootcamp_staging` | `bootcamp_prod` |
| **Schema** | `dev_<you>_sales` (automatic prefix) | `sales` | `sales` |
| **Bundle files** | `/Users/<you>/.bundle/bootcamp_lakehouse/dev` | `/Users/<ci identity>/.bundle/…/staging` | `…/prod` |
| **Resource names** | `[dev <you>] orders_job` | `[staging] orders_job` | `[prod] orders_job` |
| **Schedules** | paused | paused — CI starts runs explicitly | paused during the bootcamp |
| **Who deploys** | you (workspace UI or CLI) | GitHub Actions on merge to `main` | GitHub Actions after approval |
| **Identity** | you | CI token (you) or a service principal | same as staging |
| **Tags** | `dev=<you>` | `env=staging` | `env=prod` |

In a company, staging and prod are **separate workspaces** with their own service principals; only
`workspace.host` changes per target — everything else you learn here is identical (see the *CI/CD: enterprise vs.
bootcamp setup* slide).

`<you>` = the part of your sign-in e-mail before `@`, with non-alphanumeric characters replaced by `_`.

---

## Part 1 · GitHub: your copy of the lab repository
1. Sign in to (or create) your personal **GitHub** account.
2. Open the bootcamp repository URL from your instructor → **Use this template** → **Create a new repository**:
   * **Include all branches** ✅ (you need `solution` and the `checkpoint/*` branches)
   * Owner: you · Name: `databricks-bootcamp-labs` · Visibility: **Public** (see below) → **Create repository**
3. **Settings → Actions → General** → *Allow all actions and reusable workflows* → **Save**.

| | Public (recommended) | Private on GitHub Free |
|---|---|---|
| Environments + required reviewers (prod approval in lab 06) | ✅ | ❌ not available |
| Credentials | GitHub **secrets** — never in code | GitHub **secrets** |
| Workflow used in lab 06 | `bundle-cicd.yml` + `bundle-rollback.yml` | `bundle-cicd-private.yml` (manual prod release) |

The repository contains code and synthetic data only — no credentials — so public is safe.

## Part 2 · Databricks Free Edition workspace
### 2.1 Sign up
databricks.com → *Try Databricks* → **Free Edition** → sign up with e-mail, Google or Microsoft.
Copy your **workspace URL** (e.g. `https://dbc-1234abcd-5678.cloud.databricks.com`).

### 2.2 Link GitHub
Avatar → **Settings** → **Linked accounts** → **Add Git credential** → **GitHub** → **Link Git account** → authorise the
Databricks app for your repository → **Save**. (Alternative: a fine-grained GitHub token with *Contents: read & write*.)

### 2.3 Clone your repository as a Git folder
**Workspace** → **Home** → **Create** → **Git folder** → `https://github.com/<you>/databricks-bootcamp-labs` → **Create**.

### 2.4 Create the environment catalogs
Open `setup/free_edition_setup` → compute **Serverless** → **Run all**. It creates `bootcamp_dev`, `bootcamp_staging`,
`bootcamp_prod` and checks groups and the warehouse.
*If catalog creation is refused:* add `config/*.yml` to `include:` in `databricks.yml` — every environment then lives in
the built-in `workspace` catalog with separate schemas.

### 2.5 Groups (used in lab 02)
**Settings** → **Identity and access** → **Groups** → **Manage** → **Add group** → `bootcamp_engineers`; again →
`bootcamp_analysts`. Open `bootcamp_engineers` → **Add members** → yourself.

### 2.6 SQL warehouse
**SQL Warehouses**: note the name — usually **Serverless Starter Warehouse**. Different? Set `warehouse_name` in
`databricks.yml`.

### 2.7 Preview features (you are the admin)
**Settings** → **Previews**: enable what is offered among *Metric views*, *Domains*, *Business Glossary*,
*ABAC / tag policies*, *Genie One*. Anything not offered in Free Edition is marked *optional* in the labs.

## Part 3 · Choose your track
**Technical track** — stay on branch `main`. In the Git folder open `databricks.yml` → **Deployments** → target
**dev** → **Deploy** → then ▶ **Run** `generate_data`. You will build the rest yourself, lab by lab.

**Business track** — use the finished solution and build all the data in one click:
1. Git folder → branch selector (top) → **solution** → **Switch**.
2. `databricks.yml` → **Deployments** → **dev** → **Deploy** → confirm.
3. **Bundle resources** → ▶ **Run** `business_quickstart` (≈ 15–20 min on serverless; Free Edition runs up to 5 tasks at a time).

Fell behind in the technical track? Commit your work and switch to the matching `checkpoint/lab-NN-*` branch.

## Part 4 · Credentials for CI/CD
Free Edition has no account console, so GitHub **OIDC workload identity federation** — the enterprise best practice — is
not available (it needs an account-level federation policy). CI authenticates with a **secret stored in GitHub**:

* **Option A (default) — personal access token:** **Settings** → **Developer** → **Access tokens** → **Manage** →
  **Generate new token** → comment *github-ci-bootcamp* · lifetime **30 days** → copy it once.
* **Option B (if offered) — service principal:** **Settings** → **Identity and access** → **Service principals** →
  **Add service principal** → *bootcamp-ci* → note the **Application ID** → **Secrets** → **Generate secret**. Then:
  ```sql
  GRANT USE CATALOG, CREATE SCHEMA ON CATALOG bootcamp_staging TO `<application-id>`;
  GRANT USE CATALOG, CREATE SCHEMA ON CATALOG bootcamp_prod    TO `<application-id>`;
  ```
  give it **Can use** on the SQL warehouse, and uncomment the `run_as:` blocks of `staging` and `prod` in `databricks.yml`.

## Part 5 · GitHub Actions: variables, secrets, environments
In your repository → **Settings**:
1. **Secrets and variables → Actions → Variables** → `DATABRICKS_HOST` = your workspace URL (no trailing `/`).
2. **Secrets** → `DATABRICKS_TOKEN` = token (option A) — or `DATABRICKS_CLIENT_ID` + `DATABRICKS_CLIENT_SECRET` (option B).
3. *(Public repo)* **Environments** → `staging` (no rules) and `prod` → ✅ **Required reviewers** = you (leave *Prevent
   self-review* unticked) → **Deployment branches** → `main` only.

## Part 6 · (optional) Databricks CLI on your laptop
Every lab also works in the workspace (Git folder + web terminal). Locally:
```bash
brew tap databricks/tap && brew install databricks        # Windows: winget install Databricks.DatabricksCLI
databricks auth login --host https://<your-workspace-url> --profile bootcamp
export DATABRICKS_CONFIG_PROFILE=bootcamp
git clone https://github.com/<you>/databricks-bootcamp-labs.git && cd databricks-bootcamp-labs
databricks bundle validate && databricks bundle validate -t staging
```

## Part 7 · Verify
* Technical: `[dev <you>] generate_data` ran green; **Catalog → bootcamp_dev → dev_<you>_sales → Volumes → raw** has files.
* Business: `[dev <you>] business_quickstart` ran green; the schema contains `orders_metrics`, `fact_orders`, `tickets_enriched`.

| Lab (deck section) | Technical track needs | Business track needs |
|--------------------|-----------------------|----------------------|
| 01 Data Ingestion | Parts 1–3 | Parts 1–3 |
| 02 Data Governance | groups (2.5) | groups (2.5) |
| 03 Business Intelligence | lab 01–02 done | quickstart done |
| 04 Machine Learning | lab 01 done | quickstart done |
| 05 Generative AI | a chat model under **Serving** (built in) | same |
| 06 DevOps (DABs) | Parts 4–5 (+ 6 optional) | Parts 4–5 |

## Free Edition limits that shape the labs
* Serverless only; **one** 2X-Small SQL warehouse; **5 concurrent job tasks**; **one active pipeline per type** —
  don't run your dev pipeline while CI runs staging.
* A limited number of model serving endpoints (CPU only); **one** AI Search endpoint; **up to 3 Apps** (≤ 24 h runtime);
  **one** Lakebase project.
* Not available: Agent Bricks *Knowledge Assistant* (lab 05 builds the agent in code), clean rooms, online tables,
  account console (so no OIDC federation), SSO/SCIM. Non-commercial use only.

## Troubleshooting
| Symptom | Fix |
|---------|-----|
| `CREATE CATALOG` refused in `free_edition_setup` | Add `config/*.yml` to `include:` in `databricks.yml` — everything then lives in the built-in `workspace` catalog, isolated by schema |
| Git folder cannot clone or push | Re-link GitHub under **Settings → Linked accounts** and authorise the Databricks app for *this* repository |
| **Deployments** panel missing next to `databricks.yml` | You opened the file outside a Git folder, or the file is not at the repository root |
| `bundle deploy` creates nothing | Check the target is **dev**; staging and prod are deployed by CI only |
| No **Service principals** page, or no **Generate secret** | Not offered in your Free Edition workspace — use the PAT option (part 4, option A) |
| **Environments** missing in GitHub settings | Private repo on GitHub Free — make it public, or use `bundle-cicd-private.yml` in lab 06 |
| `business_quickstart` run sits queued | Free Edition runs 5 tasks at a time; let earlier tasks finish rather than starting more runs |
| Warehouse is not called *Serverless Starter Warehouse* | Set `warehouse_name` in `databricks.yml` to the name you see under **SQL Warehouses** |
| Preview features not listed under **Settings → Previews** | They roll out gradually; anything missing stays optional in the labs |

## After the bootcamp
Revoke the CI token (or service principal secret) and delete the GitHub secrets.
