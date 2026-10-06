# Databricks Data & AI Bootcamp — Labs

Hands-on labs for the bootcamp deck (*From Data Platform to Data Cloud*, September 2026 update). One lab per lab slot in
the deck, each in **two versions**:

* **`README.md` — technical track:** notebooks, SQL, YAML, CLI and Git; you build everything step by step.
* **`UI-GUIDE.md` — business track:** only the Databricks and GitHub web pages; ready-made data, business questions,
  discussion prompts. Written for analysts, product owners and managers.

**Each trainee uses their own accounts:** a **Databricks Free Edition** workspace and a personal **GitHub** account.
Dev, staging and prod are isolated inside that one workspace by catalog, schema, bundle path, naming and identity —
see [lab 00](labs/lab-00-prerequisites/README.md#how-dev-staging-and-prod-are-isolated-in-one-free-edition-workspace).

| # | Lab | Deck section | Technical | Business |
|---|-----|--------------|-----------|----------|
| 00 | **Prerequisites: Free Edition + GitHub** | before Day 1 | [README](labs/lab-00-prerequisites/README.md) · 60–75 min | [UI-GUIDE](labs/lab-00-prerequisites/UI-GUIDE.md) · 60 min |
| 01 | Data Ingestion | Data Engineering | [README](labs/lab-01-data-ingestion/README.md) · 75 min | [UI-GUIDE](labs/lab-01-data-ingestion/UI-GUIDE.md) · 45 min |
| 02 | Data Governance | Data Governance | [README](labs/lab-02-data-governance/README.md) · 45 min | [UI-GUIDE](labs/lab-02-data-governance/UI-GUIDE.md) · 45 min |
| 03 | Business Intelligence | Business Intelligence | [README](labs/lab-03-business-intelligence/README.md) · 60 min | [UI-GUIDE](labs/lab-03-business-intelligence/UI-GUIDE.md) · 60 min |
| 04 | Machine Learning | Machine Learning | [README](labs/lab-04-machine-learning/README.md) · 75 min | [UI-GUIDE](labs/lab-04-machine-learning/UI-GUIDE.md) · 45 min |
| 05 | Generative AI | Generative AI | [README](labs/lab-05-generative-ai/README.md) · 75 min | [UI-GUIDE](labs/lab-05-generative-ai/UI-GUIDE.md) · 60 min |
| 06 | DevOps with bundles & CI/CD | DevOps – DABs | [README](labs/lab-06-devops/README.md) · 90 min | [UI-GUIDE](labs/lab-06-devops/UI-GUIDE.md) · 45 min |
| B | Business track: Genie studio & use-case framing | Business Track | — | [README](labs/business-track/README.md) |
| H | Hackathon | Hackathon | [README](labs/hackathon/README.md) | [UI-GUIDE](labs/hackathon/UI-GUIDE.md) |

How to read the business guides: [labs/UI-CONVENTIONS.md](labs/UI-CONVENTIONS.md) · Instructors:
[docs/instructor-setup.md](docs/instructor-setup.md)

## Branches
| Branch | Content | Used by |
|--------|---------|---------|
| `main` | Starter code; exercises marked `TODO (lab-NN): …` | technical track |
| `checkpoint/lab-01-ingestion` … `checkpoint/lab-06-devops` | Solutions for every lab up to and including NN | catch-up |
| `solution` | Everything solved + the one-click `business_quickstart` job | business track, instructors |
| `instructor-source` | Annotated sources + `tools/build_checkpoints.py` | instructors |

Create your copy with **Use this template → Include all branches**. Behind in the technical track? Commit your work,
then switch your Git folder (or `git checkout`) to the checkpoint of the lab you missed.

## Repository layout
```
databricks.yml         bundle root: variables and dev / staging / prod targets
resources/             schema + volume, data generator job, pipeline, ML assets, jobs (as code)
src/bootcamp_lib/      tested Python package (data generator, quality rules)
src/pipelines/         Spark Declarative Pipelines (SQL): bronze → silver → gold
src/notebooks/         one or more notebooks per lab (NN_*.py)
setup/                 one-time Free Edition setup notebook (catalogs and checks)
config/                optional single-catalog fallback
tests/unit/            pytest suite, run by CI on every pull request
labs/                  lab guides (technical + business), CI templates for GitHub and Azure DevOps
docs/                  instructor setup
```

Product names and feature status reflect Databricks releases up to **September 2026**. In Free Edition you are the
admin: enable Preview features under **Settings → Previews**. Limits that shape the labs are listed in
[lab 00](labs/lab-00-prerequisites/README.md#free-edition-limits-that-shape-the-labs).
