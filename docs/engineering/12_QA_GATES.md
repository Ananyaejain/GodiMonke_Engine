# 12_QA_GATES.md



## Status



Version: 0.1

Document type: Engineering specification

Owner: Human project team

Depends on: canonical documents `04`–`07`, engineering documents `08`–`10`

Purpose: Define automatic pass/fail conditions and mandatory human-review gates for every publishable post.



---



## 1. QA Philosophy



Quality assurance is not one final model prompt.



It is a sequence of gates.



A later gate cannot repair missing provenance from an earlier gate by inventing information.



The engine should distinguish:



- **HARD FAIL** — workflow cannot continue;

- **HUMAN REVIEW REQUIRED** — automation may prepare material but cannot finalize;

- **WARNING** — human may proceed after seeing the issue;

- **PASS**.



---



## 2. Gate Order



Version 1 QA order:



1. Topic Gate

2. Source Gate

3. Research Packet Gate

4. Claim Gate

5. Verification Gate

6. Post Plan Gate

7. Copy Claim-Lock Gate

8. Editorial/Style Gate

9. Mascot/Asset Gate

10. Render Integrity Gate

11. High-Risk Gate

12. Human Final Gate



---



## 3. Topic Gate



### Hard fail



- topic is empty or incoherent;

- candidate has no current relevance and no under-covered rationale;

- duplicate topic already active for the same event/angle;

- topic is based only on an obviously unverifiable rumor with no researchable source trail.



### Warning



- topic is highly saturated;

- event is old but being resurfaced;

- under-covered classification is uncertain.



Topic selection remains human-controlled during version 1.



---



## 4. Source Gate



### Hard fail



For a factual explainer:



- zero retrievable sources;

- source provenance is unknown;

- essential claim depends only on Tier E material;

- source content is unavailable and no adequate replacement exists.



### Human review required



- major source conflict;

- source authenticity unclear;

- only partisan/advocacy sources are available for a contested claim;

- source is a clipped statement where context may matter.



### Pass expectations



Where practical:



- original/primary evidence for the central claim;

- secondary corroboration or context for contested/current claims;

- recorded retrieval metadata.



No fixed source count overrides quality.



---



## 5. Research Packet Gate



### Hard fail



- packet does not reference stored source IDs;

- central conclusion has no evidence trail;

- packet suppresses known contradictory evidence;

- material caveat is missing;

- unresolved retrieval error affects the main claim;

- structured output fails schema validation after bounded repair.



### Warning



- primary source was not found but strong secondary evidence exists;

- key context relies on an older stable source;

- under-covered significance is partly interpretive.



---



## 6. Claim Gate



Every factual claim used in publishable content must exist as a `Claim` record.



### Hard fail



- factual statement has no claim ID;

- numeric claim lacks unit or period when those are necessary for meaning;

- derived claim lacks stored inputs/formula;

- direct quote has no original/traceable source;

- comparison uses incompatible metrics without explicit limitation;

- claim refers to a source that does not contain supporting evidence.



### Human review required



- claim is materially ambiguous;

- legal allegation;

- casualty count;

- election/voting fact;

- rapidly changing military or protest claim;

- translated statement where nuance may affect meaning.



---



## 7. Verification Gate



Default automated policy:



### Pass



- `SUPPORTED`

- `MOSTLY_SUPPORTED`



subject to risk rules.



### Human review required



- `PARTLY_SUPPORTED`

- `MIXED`

- `MISLEADING_WITHOUT_CONTEXT`

- `REQUIRES_HUMAN_REVIEW`



### Hard fail as an asserted fact



- `CONTRADICTED`

- `NOT_ESTABLISHED`

- `STALE`



A contradicted claim may appear only as the claim being evaluated in a clearly structured fact-check.



---



## 8. Post Plan Gate



### Hard fail



- format chosen does not fit information density;

- carousel contains filler slides with no distinct informational role;

- slide requires unsupported facts;

- source note has no mapped source;

- plan turns an uncertain research conclusion into a definitive claim.



### Warning



- more than five slides in the base carousel;

- single-page post is approaching excessive text density;

- mascot concept is visually dominant over evidence without a deliberate hook reason.



---



## 9. Copy Claim-Lock Gate



This is one of the most important gates.



The draft receives an allowlist of approved claim IDs.



### Hard fail



- copy introduces a new numeric value not present in allowed structured data;

- copy introduces a new factual date not supported by a claim/source;

- copy invents a quotation;

- copy adds a factual causal assertion not present in accepted research;

- copy changes a locked number;

- copy strengthens a qualified verdict;

- source attribution is altered.



### Secondary model-assisted lint



A low-cost model may inspect copy for factual-looking assertions not recognized by deterministic checks.



Its output is advisory unless mapped to a concrete violation.



### Human review



Humans review whether a sentence sounds factual even if automation missed it.



---



## 10. Editorial and Style Gate



### Hard fail



- satire likely to be mistaken for a fabricated factual event;

- victim/suffering is used as a punchline;

- hateful/slur content;

- commentary is visually represented as a sourced quote;

- serious topic is rendered using an obviously inappropriate reaction-meme treatment.



### Warning



- too many jokes;

- repeated running gag;

- unnatural Hinglish;

- generic AI language;

- headline is vague or overclaiming;

- commentary dominates information.



Style warnings should not automatically regenerate the post indefinitely.



---



## 11. Mascot / Asset Gate



### Hard fail



- asset file missing;

- custom asset is corrupt;

- asset contains important factual infographic text generated inside the image;

- custom mascot is clearly a different character and human has rejected it;

- serious-event treatment violates mascot policy.



### Human review required



For a newly generated mascot asset:



- character identity;

- expression;

- political symbolism;

- visual appropriateness;

- accidental text/artifacts.



Existing approved assets may bypass repeated asset approval.



---



## 12. Render Integrity Gate



The renderer should inspect layout data directly; OCR should not be required for deterministic text.



### Hard fail



- wrong output dimensions for selected platform/template;

- text overflow;

- clipped headline/stat/source;

- missing referenced asset;

- missing source text;

- overlapping essential information;

- missing slide number where required;

- render hash not recorded;

- render produced from an outdated copy/render version.



### Accessibility/readability checks



Template-defined minimums should enforce:



- minimum font sizes;

- safe margins;

- adequate line height;

- normal-text contrast target of approximately WCAG 4.5:1 where practical;

- source note visibly readable at normal phone viewing size.



Exact template thresholds are defined during renderer implementation and regression-tested.



---



## 13. Data / Chart Gate



### Hard fail



- chart value differs from claim ledger;

- chart axis/label misrepresents units;

- truncated axis materially exaggerates a comparison without clear indication;

- incompatible data series are presented as equivalent;

- chart uses an outdated claim version.



Charts should be generated from structured verified data.



---



## 14. Source Display Gate



### Hard fail



- public source label names the wrong institution/source;

- source note implies evidence stronger than stored provenance;

- citation is unreadable due to clipping.



### Warning



- detailed source list is too dense for the slide and should move to caption/final source block.



---



## 15. High-Risk Gate



If topic or claim risk is `HIGH` or `CRITICAL`:



### Mandatory



- explicit human factual review;

- fresh source check;

- uncertainty check;

- final copy review;

- final render approval.



### Additional recommendation



For breaking claims:



- display “as of” timestamp where material;

- prefer bounded wording such as “confirmed so far.”



No automated QA score can bypass this gate.



---



## 16. Human Final Gate



The final reviewer must see:



- rendered post;

- core claim list;

- principal sources;

- unresolved warnings;

- risk label;

- latest version number.



Required human decision:



- `APPROVED`;

- `CHANGES_REQUESTED`;

- `REJECTED`.



Final approval references the exact render version/hash.



Any material edit after approval invalidates it.



---



## 17. QA Score



The engine may show a convenience score, but scores never replace hard gates.



Possible dashboard dimensions:



- source coverage;

- claim support;

- readability;

- visual consistency;

- mascot consistency;

- style fit;

- risk completeness.



A post with a high average score still fails if one hard gate fails.



---



## 18. Regeneration Limits



Do not create infinite “AI fixes AI” loops.



Initial policy:



- structured-output repair: maximum 1 automatic repair;

- copy regeneration after style failure: maximum 2 automatic attempts per version;

- mascot regeneration: configurable, default maximum 2 per request before human decision;

- factual verification: do not repeatedly rerun models seeking a desired verdict.



After limits are reached, surface the issue to humans.



---



## 19. Golden Set Regression



Before major changes to:



- prompts;

- model routing;

- templates;

- claim-lock logic;

- renderer;

- QA rules;



run representative Golden Set cases.



Regression should check:



- schema success;

- unsupported-fact rate;

- claim/source mapping;

- render stability;

- human-rated style where applicable.



---



## 20. QA Audit Record



Each post should retain:



- gates executed;

- gate version;

- pass/fail/warning result;

- timestamp;

- relevant issue codes;

- human overrides;

- final approval version.



Human override must be explicit and auditable.



---



## 21. Golden Rule



**A post is ready only when evidence, copy, layout, risk handling, and the exact final render all pass their own gates.**
