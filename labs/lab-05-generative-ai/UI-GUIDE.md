# Lab 05 · Generative AI for the business — business track
**Deck section: Generative AI · 60 min · no code** · [How to read this guide](../UI-CONVENTIONS.md)
Prerequisite: `business_quickstart` ran (it already classified 300 support tickets with AI).

**What you will learn:** what large language models are good (and bad) at, how AI can process thousands of documents
inside governed data, how to check its quality, and which guardrails a business owner should insist on.

## 1 · Try the models yourself (15 min)
1. Left sidebar **Playground** (under *AI/ML*).
2. Pick a model at the top (e.g. a Llama, Claude, GPT or Gemini model — whatever is listed).
3. **System prompt**: *You are a polite customer-support agent for an electronics web shop. Never promise refunds.*
4. Ask: *"My laptop order is 10 days late and I'm furious. Refund me now!"*
5. Click **+** / **Compare** to add a second model and ask the same question. Compare tone, length and speed.

💬 Which answer would you put in front of a customer? What would you change in the system prompt?

## 2 · AI on 300 tickets at once (15 min)
6. **Catalog** → **dev_<you>_sales** → **support_tickets** → **Sample data**: free text, like your real inbox.
7. Open **tickets_enriched** → **Sample data**: every ticket now has a **category**, a **sentiment** and extracted
   **entities** (order number, product) — produced by AI Functions in one SQL statement.
8. **SQL Editor** → 📋 (replace `<you>`) — *how often was the AI right?*
   ```sql
   SELECT round(avg(CASE WHEN category = true_category THEN 1.0 ELSE 0 END) * 100, 1) AS accuracy_pct
   FROM bootcamp_dev.dev_<you>_sales.tickets_enriched;
   ```
9. 📋 *where are the angry customers?*
   ```sql
   SELECT category, sentiment, count(*) AS tickets
   FROM bootcamp_dev.dev_<you>_sales.tickets_enriched
   GROUP BY ALL ORDER BY tickets DESC;
   ```
   **+** → **Visualization** → stacked bar: X = category, Y = tickets, colour = sentiment.

💬 The AI was right in X % of cases. For which decisions is that good enough — and for which is it not?

## 3 · Draft replies — with a human in the loop (10 min)
10. 📋
    ```sql
    SELECT ticket_id, body,
           ai_summarize(body, 20) AS summary,
           ai_gen(concat('Write a polite reply in max 50 words. Apologise, give the next step, never promise a refund. Ticket: ', body)) AS draft_reply
    FROM bootcamp_dev.dev_<you>_sales.tickets_enriched
    WHERE sentiment = 'negative' LIMIT 5;
    ```
11. Read the drafts. Would you send them unchanged? What would a reviewer need to check?

## 4 · Ask your data in plain English (10 min)
12. Open your **Genie** agent from lab 03 → **Settings / Data** → add **tickets_enriched** → ask
    *"Which ticket category has the most negative sentiment this month?"* → **Show code**.

## 5 · Guardrails checklist (10 min)
💬 For a customer-support AI in your company, agree as a group:
| Guardrail | Your answer |
|-----------|-------------|
| Which data may the AI read? Which must it never see (PII)? | |
| What must it never promise or decide alone? | |
| How do we measure quality before go-live (test questions, accuracy target)? | |
| Who reviews outputs, and how often, after go-live? | |
| What is the monthly budget cap? (Unity Gateway can enforce it) | |

## Take-aways
- LLMs are strong at reading, classifying and drafting text — at scale, on governed data.
- Always *measure* AI quality (accuracy, judges) and keep a human in the loop for decisions.
- Unity Gateway centralises which models may be used, by whom, and at what cost.
