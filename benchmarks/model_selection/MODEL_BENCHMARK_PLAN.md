# MODEL_BENCHMARK_PLAN.md

## Status

Version: 0.1
Type: Pre-merge engineering benchmark specification
Owner: Human project team
Purpose: Select the most cost-effective model routing for Godi Monke Engine using controlled evidence rather than assumptions.

---

## 1. Why This Benchmark Exists

The current engineering branch has not yet been merged to `main`.

Before freezing `11_MODEL_ROUTING.md` and `13_COST_POLICY.md`, the team wants empirical evidence about whether DeepSeek can replace most or all OpenAI API usage while preserving factual reliability and Godi Monke copy quality.

The benchmark must answer:

1. Which model is safest and most consistent for independent claim verification?
2. Which model is best for factual, concise Godi Monke copy from locked facts?
3. Is DeepSeek V4 Flash good enough for the default path?
4. When, if ever, is DeepSeek V4 Pro materially better?
5. Does Gemini 3.7 Flash remain preferable for copy even if DeepSeek is better for verification?
6. What is the actual cost per successful task on our workload?

The benchmark must **not** optimize political persuasion, voter targeting, outrage, or belief change.

We are testing:
- factual obedience;
- evidence use;
- clarity;
- consistency;
- structured-output reliability;
- latency;
- cost;
- brand-style fit.

---

## 2. Models in Round 1

Round 1 compares:

### A. Gemini 3.7 Flash
Use as:
- benchmark research/copy model;
- same static evidence input as every other model;
- **Search grounding disabled** during the static benchmark.

### B. DeepSeek V4 Flash
Use as:
- low-cost verification candidate;
- low-cost copy candidate.

### C. DeepSeek V4 Pro
Use as:
- higher-reasoning DeepSeek candidate;
- potential escalation verifier/copy model.

### OpenAI
Not included in Round 1.

Reason:
- the team has experienced unexpectedly high OpenAI API spend;
- Round 1 should first determine whether Gemini + DeepSeek can meet the required quality bar;
- an OpenAI baseline may be added later if the results are inconclusive.

### Exact API IDs checked for Round 1

- Gemini: `gemini-3.7-flash`
- DeepSeek Flash: `deepseek-v4-flash`
- DeepSeek Pro: `deepseek-v4-pro`
- DeepSeek base URL: `https://api.deepseek.com`

These identifiers were checked against official provider documentation on 2026-09-02.

The harness should optionally query the provider model-list endpoint during `doctor`/preflight and fail before spending money if a configured model is unavailable.

---

## 3. Benchmark Philosophy

### Static evidence only

No model may browse the web, search, call tools, or use prior conversation history.

Every model receives the **same frozen evidence packet**.

This isolates model quality from search quality.

### Stateless requests

Each benchmark call contains only:

- benchmark system instructions;
- one fixture;
- output schema.

Do not send:
- previous runs;
- chat history;
- unrelated project documents;
- complete source archives when only excerpts are required.

### Same task, same evidence

Provider-specific syntax may differ, but the substantive instructions must remain equivalent.

### Repeated runs

One good output is not enough.

Each model runs each fixture **3 times**.

This measures consistency.

### Quality before price

A model must meet the factual-quality threshold before cost becomes a selection advantage.

The cheapest model does not win if it hallucinates.

---

## 4. Benchmark Tracks

There are two independent tracks.

### Track A — Claim Verification

Input:
- one atomic claim;
- source metadata;
- relevant evidence excerpts;
- definitions;
- caveats;
- no intended headline;
- no Godi Monke humour;
- no preferred verdict.

Output:
- structured verification verdict.

### Track B — Post Copy

Input:
- accepted research summary;
- locked claim allowlist;
- exact display values;
- selected post format;
- Godi Monke voice rules;
- commentary/humour constraints.

Output:
- structured single-page or carousel copy.

The copy model is not asked to verify facts. It must obey the locked facts.

---

## 5. Required Fixtures

Create five representative real-world evidence fixtures.

All fixtures must be based on already-retrieved public sources and manually reviewed before model testing.

### Fixture 01 — Union Budget / Government Finance

Purpose:
- test numeric discipline;
- test distinctions such as allocation vs expenditure / BE vs RE / actuals;
- test derived percentage handling;
- test concise explanation.

Should contain:
- at least two budget values;
- one important definitional caveat;
- one derived comparison precomputed by Python/humans.

### Fixture 02 — Infrastructure Data

Purpose:
- test before/after comparison;
- test units and time periods;
- test risk of misleading apples-to-oranges comparisons.

Should contain:
- two comparable infrastructure values;
- one source footnote or definition;
- one tempting but invalid comparison the model must avoid.

### Fixture 03 — Political Claim Check

Purpose:
- test whether the model can return a non-binary result.

The gold verdict should ideally be:
- `PARTLY_SUPPORTED`,
- `MIXED`, or
- `MISLEADING_WITHOUT_CONTEXT`.

This prevents a trivial “true/false” benchmark.

Should contain:
- original statement;
- supporting evidence;
- contradicting or qualifying evidence;
- missing context.

### Fixture 04 — India Geopolitics

Purpose:
- test separation of confirmed event from interpretation;
- test uncertainty;
- test strategic nuance.

Should contain:
- one confirmed official development;
- one media interpretation;
- one uncertain or disputed element.

The model must not turn strategic interpretation into fact.

### Fixture 05 — Under-Covered Institutional / Policy Story

Purpose:
- test explanation of a technically important but less viral issue.

Should contain:
- one primary institutional source;
- one contextual source;
- enough evidence for a useful explainer;
- limited meme value, to test whether the model can stay information-first.

---

## 6. Gold Standard Creation

Before running any model, the humans must approve a gold record for each fixture.

Each fixture requires:

- `gold_verdict`;
- `gold_supported_claims`;
- `gold_prohibited_claims`;
- `gold_material_caveats`;
- `gold_display_values`;
- `gold_source_ids`;
- `risk_level`;
- `copy_format`;
- optional `editor_notes`.

The gold record is not shown to the model.

It is used only for scoring.

If the human team is uncertain about the gold answer, the fixture is not ready for benchmarking.

---

## 7. Fixture File Format

Recommended fixture path:

`benchmarks/model_selection/fixtures/<fixture_id>.json`

Conceptual shape:

```json
{
  "fixture_id": "F03_POLITICAL_CLAIM",
  "title": "Example",
  "risk_level": "MEDIUM",
  "claim": {
    "claim_id": "CLM-1",
    "text": "Exact atomic claim",
    "claim_type": "numeric"
  },
  "definitions": [
    "Definition required to interpret the metric"
  ],
  "evidence": [
    {
      "source_id": "SRC-1",
      "source_tier": "A",
      "publisher": "Example",
      "locator": "Table 4",
      "role": "SUPPORTS",
      "excerpt": "Relevant excerpt"
    }
  ],
  "research_summary": "Neutral accepted summary for the copy track.",
  "locked_claims": [
    {
      "claim_id": "CLM-1",
      "text": "Approved factual statement",
      "display_value": "18%"
    }
  ],
  "gold": {
    "verdict": "MIXED",
    "material_caveats": [],
    "prohibited_claims": [],
    "required_claim_ids_for_copy": ["CLM-1"]
  }
}
```

Do not put API keys or private material in fixture files.

---

## 8. Verification Prompt Contract

The verification system prompt is stored in:

`benchmarks/model_selection/prompts/verification_system.md`

Requirements:

- evaluate evidence, not political identity;
- use only supplied evidence;
- do not use memory;
- do not infer missing numbers;
- preserve uncertainty;
- output only the required structured object;
- concise rationale only;
- no chain-of-thought;
- no humour.

### Verification Output Schema

Required fields:

- `verdict`
- `confidence`
- `evidence_assessment`
- `material_caveats`
- `missing_evidence`
- `requires_human_review`
- `rationale_summary`

Allowed verdicts:

- `SUPPORTED`
- `MOSTLY_SUPPORTED`
- `PARTLY_SUPPORTED`
- `MIXED`
- `MISLEADING_WITHOUT_CONTEXT`
- `CONTRADICTED`
- `NOT_ESTABLISHED`

---

## 9. Copy Prompt Contract

The copy system prompt is stored in:

`benchmarks/model_selection/prompts/copy_system.md`

Requirements:

- facts are immutable;
- use only locked claim IDs;
- no new numbers;
- no new factual dates;
- no invented quotes;
- no new causal claims;
- core information in clear English;
- optional natural Hinglish commentary;
- humour is commentary only;
- information must remain the focus;
- no political microtargeting or persuasion-optimization objective;
- output only the required structured object.

---

## 10. Generation and Reasoning Settings

The benchmark compares **production-like routes**, not merely model names.

Provider reasoning controls differ, so the harness must record exact settings rather than pretending parameters are equivalent.

### Verification routes

**Gemini 3.7 Flash**
- thinking level: `medium`;
- max visible output target: 1,200 tokens;
- no tools;
- no web;
- Search grounding disabled.

**DeepSeek V4 Flash**
- thinking: explicitly enabled;
- reasoning effort: `low`;
- `max_output_tokens`: 1,200;
- no tools;
- no web.

**DeepSeek V4 Pro**
- thinking: explicitly enabled;
- reasoning effort: `high`;
- `max_output_tokens`: 1,800;
- no tools;
- no web.

DeepSeek currently enables thinking by default at high effort, so the harness **must set the requested effort explicitly**. Do not rely on provider defaults.

For DeepSeek Responses API calls, `max_output_tokens` includes both visible answer tokens and reasoning tokens. Therefore the harness must record whether a response was truncated/incomplete due to the cap.

### Copy routes

**Gemini 3.7 Flash**
- thinking level: `low`;
- max visible output target: 1,800 tokens;
- no tools;
- no web.

**DeepSeek V4 Flash**
- thinking: explicitly disabled for the default copy benchmark;
- temperature: approximately `0.4`;
- max output: 1,800 tokens;
- no tools;
- no web.

**DeepSeek V4 Pro**
- thinking: explicitly enabled;
- reasoning effort: `low`;
- max output: 1,800 tokens;
- no tools;
- no web.

DeepSeek temperature controls do not apply while thinking mode is enabled. The harness must not report a temperature value as effective when the provider ignores it.

### General

- no previous-message history;
- no hidden browsing;
- no provider-specific system prompt advantages;
- record all actual parameters sent;
- if a provider does not expose an equivalent control, record the difference explicitly.

---

## 11. Input Size Limits

The benchmark harness must measure request size before every call.

Initial hard limits:

### Verification
- maximum input: 15,000 estimated tokens;
- maximum output setting: 1,200 tokens.

### Copy
- maximum input: 18,000 estimated tokens;
- maximum output setting: 1,800 tokens.

If a fixture exceeds the limit:
- fail the fixture preparation;
- do not truncate evidence silently.

The solution is to improve the evidence packet.

---

## 12. Repetitions

For each track:

5 fixtures × 3 models × 3 repetitions = 45 calls.

Two tracks:

**90 calls total.**

Each run must have a stable unique run ID.

Example:

`COPY_F03_DEEPSEEK_V4_FLASH_R2`

---

## 13. Benchmark Spend Limit

Round 1 global hard cap:

**₹200**

Before each paid call:
- estimate cost if possible;
- check remaining benchmark budget;
- block the call if the remaining budget is insufficient.

If total estimated/recorded cost reaches ₹200:
- stop;
- save partial results;
- report which runs remain.

Do not auto-override.

Because Search grounding is disabled, this benchmark should normally remain well below the cap.

---

## 14. Verification Scoring

Maximum: 100 points.

### A. Verdict correctness — 30
- exact gold-equivalent verdict: 30
- adjacent acceptable verdict with equivalent meaning: partial credit
- materially wrong verdict: 0

### B. Evidence fidelity — 25
Does the rationale accurately reflect supplied evidence?
- 15 points: Deterministic source/assessment integrity (no invented source IDs, expected source coverage, assessment-role correctness)
- 10 points: NEEDS_HUMAN_SCORE for semantic rationale fidelity.
(Final score completed after blinded human review.)

### C. Caveat retention — 20
Does the model preserve material limitations?

### D. Unsupported-assertion discipline — 15
No invented facts, dates, values, quotes, or unsupported causal statements.

### E. Schema compliance — 10
Valid structured output with correct enums/types.

### Critical factual failure

Any of the following marks the run as a **CRITICAL_FAIL** regardless of numeric score:

- invented numeric value;
- invented direct quote;
- claims a source says something materially absent from the excerpt;
- converts an explicitly uncertain point into confirmed fact;
- uses outside factual knowledge not present in the frozen packet.

---

## 15. Copy Scoring

Maximum: 100 points.

### A. Factual obedience — 35
Uses only locked factual content.

A. Deterministic factual-safety gate — 20 points
   - valid claim IDs
   - no invented numbers
   - no changed locked numbers
   - no invented dates
   - no invented quotes
   - FACT blocks have claim IDs

B. Semantic factual fidelity — 15 points
   - NEEDS_HUMAN_SCORE
   - human checks whether factual prose genuinely corresponds to the referenced locked claim(s)
   - human checks unsupported named assertions / causal claims

### B. Clarity / information hierarchy — 20
Reader can understand what happened and why it matters.

### C. Godi Monke voice fit — 15
Feels like the approved information-first mascot brand.

### D. Humour / Hinglish naturalness — 10
Funny when appropriate, not forced.

### E. Concision / template fit — 10
Copy fits the requested single/carousel format.

### F. Variation / non-generic quality — 5
Avoids generic AI phrasing.

### G. Schema compliance — 5

### Critical factual failure

Any new:
- number;
- factual date;
- direct quote;
- named factual assertion;
- causal claim

that is not supported by the locked input marks the run as `CRITICAL_FAIL`.

---

## 16. Consistency Score

For each model/fixture/track across the 3 repetitions, calculate:

- verdict agreement rate;
- critical-failure count;
- schema-validity rate;
- score standard deviation;
- repeated factual deviations.

A model that occasionally produces an excellent answer but frequently fails should not become the default production model.

---

## 17. Cost Metrics

Record per run:

- provider;
- model;
- input tokens;
- output tokens;
- cached tokens if reported;
- provider usage units;
- latency;
- estimated USD cost;
- estimated INR cost;
- success/failure;
- retry count.

Aggregate:

- average cost/run;
- average cost/successful run;
- cost/100 quality points;
- projected monthly verification cost;
- projected monthly copy cost.

Use a configurable FX rate.

---

## 18. Latency Metrics

Record:

- request start;
- response end;
- total milliseconds.

Report:
- mean;
- median/p50;
- p95.

Latency is secondary to factual safety and cost, but it matters for workflow usability.

---

## 19. Retry Policy

Benchmark results must not be artificially improved by unlimited retries.

Allowed:
- one retry for transient network/rate-limit failure;
- one structured-output repair only if the provider response is syntactically invalid.

Not allowed:
- rerunning because the verdict is politically inconvenient;
- rerunning until the model matches the gold answer;
- discarding valid but poor outputs.

All retries remain part of cost reporting.

---

## 20. Human Scoring

Human scorers should not see the provider/model name while rating copy quality where practical.

Recommended:
- export model outputs with anonymous labels such as `MODEL_A`, `MODEL_B`, `MODEL_C`;
- score clarity, style, humour, and copy fit;
- reveal model identity after scoring.

Factual/schema scoring may be automated where deterministic.

---

## 21. Model Qualification Thresholds

### Verification default-model qualification

A model qualifies only if:

- zero critical factual failures across the full verification benchmark;
- mean verification score >= 90/100;
- schema-validity rate >= 98% after permitted repair;
- all high-risk/uncertain fixtures preserve material caveats;
- no systematic verdict drift toward one political conclusion.

Among qualifying models:
- prefer lower real cost;
- then lower latency;
- then simpler integration.

### Copy default-model qualification

A model qualifies only if:

- zero critical factual failures;
- mean copy score >= 85/100;
- factual-obedience component >= 33/35 average;
- schema-validity rate >= 98% after permitted repair;
- human style rating is acceptable.

Among qualifying models:
- prefer the model with the best quality/cost balance.

---

## 22. Routing Decision Rules

Possible outcomes:

### Outcome A
DeepSeek V4 Flash qualifies for verification and copy.

Then:
- default verification = V4 Flash;
- difficult/high-risk escalation = V4 Pro or human review;
- default copy may be V4 Flash if it beats/equals Gemini at lower cost.

### Outcome B
V4 Flash qualifies for verification but not copy.

Then:
- verifier = V4 Flash;
- copy = Gemini 3.7 Flash.

### Outcome C
V4 Pro materially outperforms Flash only on difficult cases.

Then:
- Flash default;
- Pro escalation triggered by risk/uncertainty.

### Outcome D
Neither DeepSeek model qualifies for verification.

Then:
- do not force DeepSeek into production;
- retain independent-provider requirement;
- run a second benchmark including an OpenAI baseline.

---

## 23. Reasoning / Chain-of-Thought Handling

The benchmark does not need model chain-of-thought.

If a provider returns separate reasoning content:
- do not print it to the console;
- do not include it in the benchmark report;
- do not use it for human scoring;
- do not preserve it as a required artifact.

Store only:
- final structured output;
- token/usage metadata;
- concise provider error information.

The system evaluates results, not hidden reasoning.

---

## 24. Output Artifacts

The harness must produce:

```text
benchmarks/model_selection/results/<timestamp>/
├── run_manifest.json
├── raw/
├── normalized/
├── scores/
├── summary.csv
├── summary.json
└── BENCHMARK_REPORT.md
```

The report should include:

- model rankings;
- critical failures;
- average scores;
- consistency;
- actual spend;
- latency;
- recommendation;
- unresolved issues.

Do not commit API keys or sensitive raw logs.

---

## 25. What Gets Committed

Safe to commit:

- benchmark plan;
- schemas;
- prompts;
- sanitized public-source fixtures;
- scoring code;
- benchmark harness;
- final summarized results if the team wants the repository public.

Do not automatically commit:

- secrets;
- provider raw request headers;
- `.env`;
- private runtime logs;
- accidental sensitive data.

---

## 26. Decision Freeze

Do not modify production `11_MODEL_ROUTING.md` or `13_COST_POLICY.md` based on expectation alone.

After the benchmark:

1. review results;
2. agree on routing;
3. update 11 and 13;
4. rerun diff checks;
5. push the amended engineering branch;
6. perform remote review;
7. only then merge to `main`.

---

## 27. Golden Rule

**Benchmark the exact jobs we need, with the exact evidence we will use, and choose the cheapest model that first clears the factual-quality bar.**
