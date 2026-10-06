# Lab 05 · Generative AI — technical track
**Deck section: Generative AI (Lab · Gen AI) · 75 min** · checkpoint: `checkpoint/lab-05-genai`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** apply GenAI to governed data at scale with **AI Functions**, then build, trace and evaluate a tool-using
**support agent** with **MLflow 3** — models reached through Foundation Model APIs and governed by **Unity Gateway**.

## What you build
| Artifact | Where |
|----------|-------|
| `tickets_enriched` — category, sentiment, entities + measured accuracy | `src/notebooks/05_ai_functions.py` |
| UC functions `lookup_order`, `customer_order_summary` | `src/notebooks/05_agent_tools.py` |
| `support_docs` governed knowledge table | same notebook |
| Traced, evaluated support agent | `src/notebooks/05_agent.py` |

## Prerequisites
* Lab 01 done — `orders_enriched` exists and `tickets/` and `docs/` are in the raw volume.
* Run `05_ai_functions` → `05_agent_tools` → `05_agent`, in that order; the agent reads `support_docs`.
* A pay-per-token chat model listed under **Serving**. Set the `llm_endpoint` widget to a name you actually see
  there — the default may not exist in your workspace.

> **Free Edition:** the Agent Bricks *Knowledge Assistant* is not available, so Part C builds the same pattern in code.
> One AI Search endpoint is allowed (Part D, optional).

## Part A · AI Functions in SQL (20 min)
`src/notebooks/05_ai_functions.py` (TODOs `lab-05`): load 300 support tickets → `tickets_enriched` with
`ai_classify`, `ai_analyze_sentiment`, `ai_extract` → **measure accuracy** against the stored true category →
`ai_summarize` + `ai_gen` draft replies for negative tickets → `ai_query` with an explicit model.

## Part B · Governed tools (10 min)
`src/notebooks/05_agent_tools.py`: UC functions `lookup_order` (TODO) and `customer_order_summary`, and the governed
knowledge table `support_docs`. The function `COMMENT`s tell the agent when to call them.

## Part C · Agent + evaluation (35 min)
`src/notebooks/05_agent.py`:
1. Pick a tool-calling chat model under **Serving** → widget `llm_endpoint`.
2. Complete the agent loop (TODO): call the model with `tools=TOOLS`, run requested tools with `run_tool()`, loop until
   it answers. Ask *"What did order 1 contain, and can I still return it?"* → open the **trace**.
3. Complete the evaluation (TODO): `mlflow.genai.evaluate` with Correctness, RelevanceToQuery, Safety and a Guidelines
   judge → **Experiments → bootcamp-support-agent → Evaluations**.
4. Human in the loop: *"Refund order 1 now."* must trigger a confirmation question.

## Stretch
* **AI Search:** `support_docs` → **Create → Vector search index** (Delta Sync, managed embeddings) → swap `search_policies`.
* **Genie as a tool:** call your lab 03 Genie Agent (or the Genie One MCP server) for revenue questions.
* **Monitoring:** `Safety().register(name="safety").start(...)` to score new traces continuously (AgentOps loop slide).
* **Unity Gateway:** open the endpoint's usage/budget settings and discuss spend caps.

## Done when
- [ ] `tickets_enriched` exists and accuracy is measured
- [ ] A trace shows a UC function call; answers cite policy documents
- [ ] An evaluation with ≥ 3 judges is logged in MLflow

## Troubleshooting
| Symptom | Fix |
|--------|-----|
| `ai_classify` / `ai_query` fails: endpoint not found | The `llm_endpoint` default may not exist here — pick a name from **Serving** and set the widget |
| AI Functions return NULL for every row | The model is rate-limited or the text column is empty; try 10 rows first, then scale up |
| Accuracy looks far too low | Check you compared `category` with `true_category` on `tickets_enriched`, not on `support_tickets` |
| `lookup_order(1)` returns nothing | Order ids start at 1 per batch — confirm `orders_enriched` has rows for batch 0 |
| Agent loops without answering | The loop must append the assistant message *and* one `{"role": "tool", …}` per tool call before re-calling the model |
| `mlflow.genai.evaluate` is missing | Needs `mlflow[databricks]>=3.1`; re-run the first cell and `%restart_python` |
| No traces under the experiment | `mlflow.openai.autolog()` must run before the first LLM call — re-run the setup cell |
| Vector search index creation refused | Free Edition allows one AI Search endpoint; the keyword retriever in `search_policies` is the fallback |
