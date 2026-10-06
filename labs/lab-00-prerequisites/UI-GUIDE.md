# Lab 00 · Getting set up — business track
**≈ 60 min before Day 1 · no technical background needed** · [How to read this guide](../UI-CONVENTIONS.md)

**What you will have at the end:** your own free Databricks workspace full of realistic sales data, your own copy of the
course material on GitHub, and everything ready so that — in the DevOps lab — *you* can act as the business approver
of production releases.

**Why three environments?** Companies never change production directly. Changes are built in **dev** (a personal
sandbox), tested in **staging** (a rehearsal) and only then released to **prod** (what the business uses) — after an
approval. In your free workspace the three are kept apart by name:

| | dev | staging | prod |
|---|---|---|---|
| Data lives in | `bootcamp_dev` | `bootcamp_staging` | `bootcamp_prod` |
| Who changes it | you, freely | the automated pipeline | the automated pipeline, **after your approval** |

---

## A · GitHub (10 min)
1. Go to **github.com** → **Sign up** (or sign in) with a personal e-mail.
2. Open the course link from your instructor → green **Use this template** → **Create a new repository**.
3. Tick **Include all branches** → *Repository name*: *databricks-bootcamp-labs* → **Public** → **Create repository**.
4. **Settings** (top of your repository) → **Actions** → **General** → *Allow all actions and reusable workflows* → **Save**.

## B · Databricks Free Edition (15 min)
5. Search the web for **Databricks Free Edition** → **Sign up** with Google, Microsoft or your e-mail.
6. After signing in, copy the address in your browser bar up to `.com` — this is your **workspace URL**. Keep it in a note.
7. Top-right **avatar** → **Settings** → **Linked accounts** → **Add Git credential** → **GitHub** → **Link Git account** →
   **Authorize** → **Save**.
8. Left sidebar **Workspace** → **Home** → **Create** → **Git folder** → paste
   *https://github.com/<your-github-name>/databricks-bootcamp-labs* → **Create Git folder**.

## C · One-time setup (10 min)
9. In the new folder open **setup** → **free_edition_setup** → top right choose **Serverless** → **Run all**.
   Wait for the green ticks: three catalogs (dev, staging, prod) are created.
10. **avatar** → **Settings** → **Identity and access** → **Groups** → **Manage** → **Add group** → *bootcamp_engineers* →
    **Add**. Again → *bootcamp_analysts*. Open **bootcamp_engineers** → **Add members** → yourself → **Add**.
11. **avatar** → **Settings** → **Previews** → switch on any of *Metric views*, *Domains*, *Business Glossary*,
    *Genie One* that are listed.

## D · Load all the course data in one click (20 min, mostly waiting)
12. In your Git folder, click the branch name at the top (it says **main**) → choose **solution** → **Switch**.
13. Open **databricks.yml** → the right-hand panel **Deployments** → *Target* **dev** → **Deploy** → **Deploy** again to confirm.
14. In **Bundle resources**, next to **business_quickstart** click ▶ **Run**. Click the run link and watch the boxes turn
    green (about 15–20 minutes). Take a coffee.
15. Left sidebar **Catalog** → **bootcamp_dev** → **dev_<you>_sales**: you should see tables such as *orders_silver*,
    *fact_orders*, *orders_metrics*, *tickets_enriched*.

## E · Prepare the release approval for lab 06 (10 min)
16. Databricks: **avatar** → **Settings** → **Developer** → **Access tokens** → **Manage** → **Generate new token** →
    comment *github-ci-bootcamp*, lifetime *30* days → **Generate** → **Copy**. (Treat it like a password.)
17. GitHub: your repository → **Settings** → **Secrets and variables** → **Actions**:
    * **Variables** tab → **New repository variable** → *DATABRICKS_HOST* = your workspace URL → **Add variable**
    * **Secrets** tab → **New repository secret** → *DATABRICKS_TOKEN* = the token → **Add secret**
18. **Settings** → **Environments** → **New environment** → *staging* → **Configure environment** → **Save protection rules**.
19. **New environment** → *prod* → tick **Required reviewers** → add yourself → **Deployment branches and tags** →
    *Selected branches and tags* → add *main* → **Save protection rules**.

## You are ready when
- [ ] `business_quickstart` job in **Jobs & Pipelines** finished with all boxes green
- [ ] You can see `orders_metrics` in **Catalog**
- [ ] GitHub shows the variable, the secret and the two environments

💬 In your organisation, who approves changes to a KPI definition or a report before it reaches management?
