# Guidance for AI coding agents (Genie Code, Claude Code, Codex, …)

- This repo is a **Declarative Automation Bundle**. Resources are declared in `resources/*.yml`; do not create jobs or pipelines through the UI or API.
- Reference resources with `${resources.<type>.<key>.<field>}` and variables with `${var.<name>}`. Never hardcode catalog, schema, workspace URLs, IDs or secrets.
- Put reusable Python in `src/bootcamp_lib/` and add unit tests in `tests/unit/`. Run `pytest -q` and `databricks bundle validate` before proposing a change.
- Pipelines are Spark Declarative Pipelines in SQL under `src/pipelines/`. Keep data-quality rules in sync with `src/bootcamp_lib/quality.py`.
- Only CI deploys to `staging` and `prod`. Humans and agents deploy to `dev` only.
