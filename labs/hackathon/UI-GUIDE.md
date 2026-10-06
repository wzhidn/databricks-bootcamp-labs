# Hackathon — UI-only path

Teams can build and ship entirely from the browser:

| Need | UI path |
|------|---------|
| Join the team repo | Accept the GitHub invitation → your workspace → **Create** → **Git folder** → owner's repo URL |
| Start a feature | Git folder → **Branch** → **Create branch** *feature/<topic>* |
| Ingest a new source | **Jobs & Pipelines** → **Create** → **Ingestion pipeline** (connectors) or add a SQL file to `src/pipelines/` in the Lakeflow editor |
| Declare it in the bundle | Create *resources/<name>.yml* in the Git folder (Genie Code can draft it) → **Deployments** → **dev** → **Deploy** |
| KPI | **Catalog** → **Create** → **Metric view** |
| Dashboard / Genie Agent | **Dashboards** → **Create**; **Genie** → **New** — then add them to the bundle as in lab 06 |
| Agent | Copy the lab 05 pattern (`src/notebooks/05_agent`) and swap the tools |
| App | **Compute → Apps** → **Create app**, or App Space → **Genie App Builder** |
| Ship to staging | Git folder → **Git** → **Commit & Push** → open a PR on GitHub → review → merge → CI deploys to the owner's staging |

Rules and judging: [README.md](README.md), [judging.md](judging.md).
