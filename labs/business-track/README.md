# Business track · Genie studio & use-case framing

> 🖱️ UI step-by-step: [UI-GUIDE.md](UI-GUIDE.md)

**Day 3 · 9:15 AM – 12:45 PM · Business participants** (runs in parallel with the DAB deep-dive)

No code. You need a browser, your **Databricks Free Edition** workspace and your GitHub copy of the repository (lab 00).

## Part 0 · Data ready?
You need the business path of [lab 00](../lab-00-prerequisites/UI-GUIDE.md) (`business_quickstart` finished). Labs 01–06
have their own business guides (`UI-GUIDE.md`); this studio goes deeper on Genie and use-case framing for the hackathon.

## Part 1 · Genie studio: from a sales assistant to a customer assistant (90 min)

**Goal:** turn the lab 03 *Sales assistant* into a Genie Agent that answers across sales, churn and support — and prove
it with benchmarks.

1. **Add data.** Open your Genie Agent from lab 03 → **Data** → add `churn_predictions` and `tickets_enriched`.
2. **Instructions** (plain language): *"A customer is 'at risk' when churn_predicted = 1. Negative tickets mean
   sentiment = 'negative'. Revenue always means the governed revenue measure. Answer in EUR."*
3. **Cross-domain questions:** *"Which at-risk enterprise customers opened negative tickets this month?"* ·
   *"Is revenue from at-risk customers growing or shrinking?"* → **Show code** each time.
4. **Trusted SQL:** save the best query as an example so Genie reuses it.
5. **Benchmarks:** 5 new questions with known answers → **Run benchmarks** → fix instructions until ≥ 4/5 pass.
6. **Genie One:** ask the same questions from Genie One. *(Optional)* Google Sheets / Excel add-in; Slack/Teams
   integrations need a company workspace and are shown by the instructor.
7. **Dashboard:** add a *Customers at risk* page to your lab 03 dashboard and **Publish**.

**Done when:** the Genie Agent passes ≥ 4/5 new benchmarks and the dashboard page is published.

## Part 2 · Governed apps without code (30 min)
If **Genie App Builder** (Beta) is available in your workspace (**Apps** → App Space; Free Edition allows up to 3 apps),
describe an app, e.g.
*"A page where regional managers see their region's revenue vs. last month and can flag anomalies with a comment."*
Iterate twice on the prompt. Not available? Sketch the screen on paper or in a dashboard instead.
Note what data and permissions the app needs — you will hand this to engineers.

## Part 3 · Frame your hackathon use case (75 min)
Fill in the [use-case canvas](../hackathon/use-case-canvas.md) in pairs, then pitch it in 2 minutes.
The best 4–6 canvases become the hackathon challenges; each author becomes that team's **product owner**.

Tips for a good canvas:
* One decision or process, one user group — not "a data platform".
* KPIs must be expressible as **metric view measures**.
* Acceptance criteria are what the 5-minute demo must show.

## Why release governance matters to you (10 min, with the tech track)
Engineers ship through **dev → staging → prod** with reviews and an approval step. On Day 3 afternoon *you* are the
approver for production deployments in your team's pipeline: you approve after checking the staging result.
