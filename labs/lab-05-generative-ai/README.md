# Lab 05 · Generative AI — technical track
**Deck section: Generative AI (Lab · Gen AI) · 75 min** · checkpoint: `checkpoint/lab-05-genai`

> 🖱️ Business track: [UI-GUIDE.md](UI-GUIDE.md)

**Goal:** apply GenAI to governed data at scale with **AI Functions**, then build, trace and evaluate a tool-using
**support agent** with **MLflow 3** — models reached through Foundation Model APIs and governed by **Unity Gateway**.

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

## Part D · Optional
* **AI Search:** `support_docs` → **Create → Vector search index** (Delta Sync, managed embeddings) → swap `search_policies`.
* **Genie as a tool:** call your lab 03 Genie Agent (or the Genie One MCP server) for revenue questions.
* **Monitoring:** `Safety().register(name="safety").start(...)` to score new traces continuously (AgentOps loop slide).
* **Unity Gateway:** open the endpoint's usage/budget settings and discuss spend caps.

## Done when
- [ ] `tickets_enriched` exists and accuracy is measured
- [ ] A trace shows a UC function call; answers cite policy documents
- [ ] An evaluation with ≥ 3 judges is logged in MLflow
