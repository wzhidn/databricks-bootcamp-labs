# Instructor setup — personal Free Edition + GitHub model

Trainees bring **their own Databricks Free Edition workspace and GitHub account**. There is no shared workspace to
administer; your job is to publish the repository, validate the labs on a Free Edition account, and support lab 00.

## 1 · Publish the lab repository (once)
1. Push all branches of this repository to your GitHub account (`main`, `checkpoint/*`, `solution`; keep
   `instructor-source` private if you prefer — see below).
2. **Settings → General → ✅ Template repository.** Trainees then use **Use this template → Include all branches**.
3. Keep the repository **public** (it contains only code and synthetic data) so trainees can create their copies.
4. Optional: move `instructor-source` to a separate private repository — it contains the solution markers and the
   branch generator (`tools/build_checkpoints.py`).

## 2 · Send lab 00 one week before Day 1
Send technical participants `labs/lab-00-prerequisites/README.md` and business participants its `UI-GUIDE.md`.
Ask them to confirm by e-mail or a form: *Free Edition workspace works*, *`generate_data` (technical) or
`business_quickstart` (business) ran green*, *GitHub variable, secret and environments set*.
Azure DevOps path (optional, technical): request the free hosted parallel job **at least 3 business days** before.

### Which guide for whom
| Participant | Guides | Branch |
|-------------|--------|--------|
| Engineers, analysts who code | `README.md` of each lab | `main` (+ `checkpoint/*` to catch up) |
| Business analysts, product owners, managers | `UI-GUIDE.md` of each lab + business track | `solution` + `business_quickstart` job |

Business participants join the hackathon as product owners and act as the prod approver (lab 06 business guide).

## 3 · Dry run on your own Free Edition account (half a day)
```bash
# from a clean template copy with all branches
git checkout solution
databricks bundle deploy
databricks bundle run business_quickstart     # everything the business guides need
databricks bundle run orders_job
databricks bundle run train_churn_model
# notebook 05_agent (set the chat model available that day)
# push to your copy → PR → merge → watch staging and prod in GitHub Actions
databricks bundle destroy --auto-approve
```
Record the **Foundation Model API** chat model names available in Free Edition that day (lab 05 widget default) and
the exact warehouse name, and update the defaults if they changed.

## 4 · What differs from a company workspace (talk track)
| Topic | Free Edition (labs) | Company setup (explain) |
|-------|---------------------|-------------------------|
| Environments | one workspace; catalogs `bootcamp_dev/_staging/_prod` | separate workspaces per env; `workspace.host` per target |
| CI identity | PAT or workspace service principal secret in GitHub secrets | service principal + OIDC workload identity federation (account-level policy), no secrets |
| Groups | created by the trainee (they are admin) | account groups synced from the IdP (SCIM) |
| Agent Bricks | code-first agent (no Knowledge Assistant) | Knowledge Assistant / Multi-Agent Supervisor demo |
| Quotas | 5 concurrent tasks, 1 active pipeline per type, 1 warehouse, few endpoints | budget policies and quotas you define |
| Prod approval | GitHub environment reviewer (public repo) or manual release run (private repo) | environment protection + change management |

## 5 · Common lab 00 issues
| Symptom | Fix |
|---------|-----|
| `CREATE CATALOG` fails | Enable the single-catalog fallback: add `config/*.yml` to `include:` in `databricks.yml` |
| No *Service principals* page / no *Generate secret* | Use the PAT option (lab 00, part 4, option A) |
| Environments missing in GitHub settings | Private repo on GitHub Free → use `bundle-cicd-private.yml`, or make the repo public |
| Git folder cannot push | Re-link GitHub in **Settings → Linked accounts** and authorise the Databricks app for the repo |
| Serving endpoint creation refused | Free Edition endpoint limit — delete unused endpoints under **Serving** |
