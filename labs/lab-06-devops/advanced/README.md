# Lab 06 stretch · Python resources and mutators

Define resources in Python when YAML would be repetitive, and enforce standards with **mutators** that run on every
resource at deploy time. Python and YAML resources live side by side in the same bundle.

## Enable it
1. Copy the folder to the bundle root: `cp -r labs/lab-06-devops/advanced/bundle_python .`
2. Create a virtual environment with the Python package for bundles:
   ```bash
   python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install databricks-bundles
   ```
   Use the same major/minor version as your CLI (`databricks --version`).
3. Add to `databricks.yml`:
   ```yaml
   python:
     venv_path: .venv
     resources:
       - "bundle_python.resources:load_resources"
     mutators:
       - "bundle_python.mutators:add_standard_tags"
   ```
4. `databricks bundle validate -o json | jq '.resources.jobs | keys'` → `ingest_customers`, `ingest_orders`, …
   and every job — including the YAML ones — now carries `cost_center`, `deployed_by` and `target` tags.

## Discuss
* Which of your projects have dozens of near-identical jobs that a metadata table could generate?
* Which standards (tags, notifications, timeouts, budget policies) should a platform team enforce with mutators?
* In CI, the runner needs the same venv: add `pip install databricks-bundles` before `databricks bundle deploy`.
