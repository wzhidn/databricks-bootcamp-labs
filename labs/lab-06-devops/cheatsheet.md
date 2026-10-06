# Declarative Automation Bundles — cheat sheet

| Task | Command |
|------|---------|
| New project from a template | `databricks bundle init default-python` (also `default-minimal`, `default-sql`, `pydabs`, `mlops-stacks`) |
| Org template | `databricks bundle init <git-url> --template-dir <folder>` |
| Validate config | `databricks bundle validate [-t <target>]` |
| What will change? | `databricks bundle plan [-t <target>]` |
| Deploy | `databricks bundle deploy [-t <target>]` |
| Deploy only some resources (dev) | `databricks bundle deploy --select <key>[,<key>]` |
| Run a job / pipeline | `databricks bundle run <key> [--params k=v,k2=v2]` |
| Run some tasks only | `databricks bundle run <job-key> --only <task-key>` |
| What is deployed? | `databricks bundle summary` |
| Open in browser | `databricks bundle open <key>` |
| YAML from an existing asset | `databricks bundle generate job\|pipeline\|dashboard\|genie-space\|app\|alert …` |
| Adopt existing asset | `databricks bundle deployment bind <key> <id>` |
| Release from bundle | `databricks bundle deployment unbind <key>` |
| Migrate a Terraform-engine bundle | `databricks bundle deployment migrate` |
| Remove everything deployed | `databricks bundle destroy [-t <target>]` |
| Override a variable | `--var="name=value"` or env `BUNDLE_VAR_name=value` |

**Substitutions:** `${bundle.name}`, `${bundle.target}`, `${workspace.current_user.userName}`,
`${workspace.current_user.short_name}`, `${var.<name>}`, `${resources.<type>.<key>.id|name}`.

**Modes:** `development` → `[dev <you>]` prefix, paused schedules, per-user paths.
`production` → requires a stable identity (`run_as`), shared root path, schedules active.

**Engine:** direct deployment engine is the default (CLI ≥ 1.3). Terraform-engine bundles are auto-migrated from CLI 1.14;
temporary opt-out with `bundle.engine: terraform`.
