# 06_FACT_CHECKING_PROTOCOL.md

## Status

Version: 0.1  
Document type: Canonical  
Owner: Human project team  
Purpose: Define the mandatory process for converting raw sources into verified publishable claims.

---

## 1. Core Principle

The fact-checking system evaluates claims, not people.

Its job is not to make a political side win.

Its job is to determine what the available evidence actually supports.

---

## 2. Claim Unit

A claim should be atomic enough to verify.

Bad claim:

> “The government completely transformed infrastructure.”

This combines interpretation, scale, causality, and judgement.

Better claims:

- `National highway network length was X in year A.`
- `National highway network length was Y in year B.`
- `The stated increase between A and B is Z%.`

Each can be verified independently.

---

## 3. Claim Record

Each claim should eventually support fields such as:

```json
{
  "claim_id": "CLAIM-0001",
  "text": "Example factual claim",
  "claim_type": "numeric",
  "entities": [],
  "period": null,
  "value": null,
  "unit": null,
  "source_ids": [],
  "evidence": [],
  "verification_status": "UNVERIFIED",
  "confidence": null,
  "risk_level": "LOW",
  "notes": null
}
```

The final schema will be defined in the engineering specification.

---

## 4. Verification Statuses

Use controlled statuses:

- `UNVERIFIED`
- `SUPPORTED`
- `MOSTLY_SUPPORTED`
- `PARTLY_SUPPORTED`
- `MIXED`
- `MISLEADING_WITHOUT_CONTEXT`
- `CONTRADICTED`
- `NOT_ESTABLISHED`
- `STALE`
- `REQUIRES_HUMAN_REVIEW`

Do not create new verdict labels ad hoc in model output.

---

## 5. Verification Workflow

### Step 1 — Identify the exact claim

Capture the original wording when checking a public statement.

Separate factual propositions from:

- opinion;
- prediction;
- rhetoric;
- value judgement.

### Step 2 — Define what evidence would answer it

Before searching, state what would support or contradict the claim.

This reduces confirmation bias.

### Step 3 — Gather primary evidence

Look for the authoritative document, dataset, original statement, or record.

### Step 4 — Gather corroborating/context evidence

Use credible secondary or specialist sources as needed.

### Step 5 — Check definitions

Confirm:

- unit;
- period;
- denominator;
- geographic scope;
- data series;
- methodology;
- whether values are nominal/real, budgeted/spent, sanctioned/completed, etc.

### Step 6 — Check arithmetic

Where the post uses derived values:

- calculate them programmatically;
- store the formula;
- store the input claim IDs;
- never rely on mental arithmetic from the LLM.

### Step 7 — Search for counter-evidence

Actively look for evidence that would weaken the provisional conclusion.

### Step 8 — Assign status

Use the controlled verdict set.

### Step 9 — Record caveats

Any caveat that materially changes interpretation must travel with the claim.

### Step 10 — Independent verification

A separate verification pass should assess the claim/evidence package without being instructed to reach a preferred political conclusion.

### Step 11 — Human review where required

High-risk, disputed, breaking, or legally sensitive claims require human review before publication.

---

## 6. Numeric Verification

For every published number:

- preserve original source value;
- preserve unit;
- preserve data period;
- preserve source;
- preserve any transformation.

Example:

```text
SOURCE VALUE: 100
SOURCE PERIOD: 2020
COMPARISON VALUE: 125
COMPARISON PERIOD: 2025
DERIVED CHANGE: +25%
FORMULA: ((125 - 100) / 100) * 100
```

The renderer should receive the approved derived result from code, not ask a language model to recalculate it.

---

## 7. Comparison Verification

Before an A-vs-B card is approved, verify:

- same metric;
- same definition;
- same or intentionally comparable period;
- same unit;
- same denominator where applicable;
- no policy-definition change hidden between dates.

If not directly comparable, the post must explain the difference.

---

## 8. Budget / Government Data Distinctions

The system must distinguish terms such as:

- budget estimate;
- revised estimate;
- actual expenditure;
- allocation;
- sanction;
- release;
- expenditure;
- completion;
- target.

These are not interchangeable.

A claim that says “spent” must not be sourced only to a budget allocation.

---

## 9. Infrastructure Distinctions

Where relevant, distinguish:

- announced;
- approved;
- sanctioned;
- under construction;
- completed;
- operational;
- network length;
- lane-kilometres;
- project length.

Do not compare incompatible definitions.

---

## 10. Geopolitics Verification

For geopolitical developments:

- identify the original government or institutional statement;
- distinguish confirmed action from media speculation;
- avoid inferring secret motive as fact;
- separate observed event from strategic interpretation;
- timestamp rapidly developing claims.

---

## 11. Protest and Casualty Verification

For protests, violence, conflict, or casualties:

- avoid relying on one partisan estimate when multiple estimates exist;
- attribute numbers explicitly;
- preserve ranges when necessary;
- update stale figures;
- identify whether the number is official, media-reported, organizer-reported, or independently verified.

---

## 12. Quote Verification

For direct quotes:

- use the original full statement where possible;
- verify speaker;
- verify date;
- verify context;
- do not combine separate sentences into a misleading quotation;
- keep paraphrases visually distinct from direct quotations.

---

## 13. Time Sensitivity

Every claim should have a freshness expectation.

Examples:

- live protest casualty count: very high freshness requirement;
- monthly inflation rate: tied to latest official release;
- historical constitutional fact: low freshness requirement.

The system should be able to mark a previously verified claim as stale when the underlying value is expected to change.

---

## 14. Independent Verifier Rules

The independent verifier should receive:

- claim;
- source metadata;
- supporting evidence;
- relevant caveats.

Where feasible, it should not receive:

- desired headline;
- preferred political framing;
- humour;
- intended verdict.

Its job is narrow:

> Does this evidence support this claim?

---

## 15. Verification Failure

If a claim fails verification:

- it must not remain in publishable copy;
- dependent derived claims must also be invalidated;
- the content planner may revise the post around the remaining supported evidence;
- the system must log the failure reason.

---

## 16. Hallucination Defense

The engine should treat model-generated facts as untrusted until grounded in a claim record.

Creative copy generation should receive immutable factual fields.

If the creative model outputs:

- a new number;
- a new date;
- a new named factual assertion;

that does not map to the claim ledger, the draft should fail QA.

---

## 17. Human Review Triggers

Mandatory human factual review should be triggered by:

- high-risk topic classification;
- unresolved source conflict;
- `MIXED`;
- `MISLEADING_WITHOUT_CONTEXT`;
- `NOT_ESTABLISHED`;
- legal allegation;
- casualty/death claim;
- election-related factual claim;
- breaking military/geopolitical development;
- substantial reliance on translated or ambiguous material.

---

## 18. Golden Rule

**No claim becomes true because a model said it twice. It becomes publishable because the evidence supports it.**
