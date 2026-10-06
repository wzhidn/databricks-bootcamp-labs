# Instructor source

Annotated sources. Solution code is wrapped in markers:

* `SOLUTION-BEGIN lab-NN: <hint>` … `SOLUTION-END` — replaced by `TODO (lab-NN): <hint>` below level NN
* `SOLUTION-FILE lab-NN` — file omitted below level NN

Regenerate every participant branch after editing:

```bash
for L in 0 1 2 3 4 5 6 99; do python tools/build_checkpoints.py . /tmp/out/L$L $L; done
# L0 → main, L1 → checkpoint/lab-01-ingestion, L2 → lab-02-governance, L3 → lab-03-bi,
# L4 → lab-04-ml, L5 → lab-05-genai, L6 → lab-06-devops, L99 → solution
```
Checkpoints are cumulative (checkpoint/lab-NN = state *after* lab NN). Validate each with `pytest -q` and
`databricks bundle validate -t dev|staging|prod`. The business track uses the `solution` branch.
