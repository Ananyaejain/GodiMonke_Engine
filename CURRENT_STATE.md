# CURRENT_STATE.md



## Project



**Name:** Godi Monke Engine

**Current project stage:** Engineering specification freeze

**Document version:** 0.2

**Status:** Pre-implementation



---



## Current Milestone



**Milestone 0C — Engineering Specification Freeze**



Canonical product specification `00`–`07` has been reviewed and pushed to `main`.



Engineering specification `08`–`15` has now been drafted and internally consistency-checked. It must be installed on a dedicated specification branch, pushed for remote review, and accepted before substantive application code begins.



---



## Completed



- Initial repository/directory skeleton created.

- Public GitHub repository established.

- Canonical product specification `00`–`07` reviewed and pushed.

- `AGENTS.md` established.

- Brand, mascot, voice, editorial, source, fact-checking, and content-format rules established.

- Engineering architecture drafted:

  - `08_SYSTEM_ARCHITECTURE.md`

  - `09_DATA_MODEL.md`

  - `10_WORKFLOW_STATE_MACHINE.md`

  - `11_MODEL_ROUTING.md`

  - `12_QA_GATES.md`

  - `13_COST_POLICY.md`

  - `14_SECURITY_AND_SECRETS.md`

  - `15_ROADMAP.md`

- Current model/pricing baseline checked against official provider documentation on 2026-09-02.

- Engineering documents internally checked for the major project invariants:

  - ₹5,000 total monthly planning ceiling;

  - quality-first launch;

  - approximately two posts/day;

  - three discovery scans/day;

  - human final approval;

  - no automatic publishing in version 1;

  - evidence-backed claim ledger;

  - separation of facts and commentary;

  - deterministic factual rendering;

  - local-first development;

  - provider-independent architecture.



---



## In Progress



- Install engineering specification `08`–`15` on branch:

  - `spec/engineering-v0.1`

- Push that branch for remote review.

- Verify canonical `00`–`07` remain unchanged.

- Review the remote diff before merging engineering specifications to `main`.



---



## Not Started



- Python application foundation.

- Configuration system.

- Structured logging.

- CLI.

- SQLite schema and migrations.

- Workflow state implementation.

- Audit-event implementation.

- Fake-provider vertical slice.

- Telegram interface.

- Deterministic renderer.

- Gemini topic discovery.

- Safe source retrieval.

- Research-packet generation.

- Claim ledger implementation.

- OpenAI independent verification.

- Copy/humour generation.

- Mascot image API integration.

- End-to-end automated QA.

- VPS deployment.

- Instagram/X publishing integrations.



---



## Current Runtime Architecture Decision



Version 1 will be a small Python application.



Primary baseline:



- Python 3.12+

- Pydantic v2

- SQLAlchemy 2.x

- Alembic

- SQLite

- Telegram long polling

- Jinja2 + HTML/CSS

- Playwright/Chromium for deterministic rendering

- pytest

- provider adapters around external APIs



Python owns workflow state.



Models are bounded workers and cannot bypass state, evidence, budget, or approval rules.



---



## Current Model Routing Baseline



Checked 2026-09-02.



### Topic discovery / grounded research

Primary:

- Gemini 3.7 Flash

- Google Search grounding



### Routine low-cost extraction/classification

Primary:

- local deterministic code first

- Gemini 3.5 Flash-Lite only when semantic model judgement is useful



### Research synthesis / claim extraction

Primary:

- Gemini 3.7 Flash



### Independent claim verification

Primary:

- GPT-5.6 Terra



The verifier must not silently fall back to the same model/provider that produced the research conclusion.



### Optional inexpensive model QA

- GPT-5.6 Luna



### Mascot generation/editing

Primary:

- Gemini 3.1 Flash Image / Nano Banana 2



Reuse approved mascot assets before generating new ones.



### Manual fallback

The human team may manually use existing ChatGPT Plus for difficult editorial or mascot work.



ChatGPT Plus is not treated as API credit.



---



## Current Cost Policy



Total monthly planning ceiling:



**₹5,000**



Planning envelope:



- ChatGPT Plus: ₹2,000

- X subscription: ₹500

- VPS reserve: ₹400

- automated APIs: ₹1,600

- contingency/tax/FX: ₹500



Initial automated API caps:



- Google: ₹900

- OpenAI: ₹600

- miscellaneous: ₹100



Google Search-grounding internal usage policy:



- warning: 3,500 requests/month;

- automatic stop: 4,500 requests/month;

- provider-advertised current free allowance: 5,000/month shared across Gemini 3.x.



No automatic paid grounding overage.



---



## Current Workflow Decisions



Target:

- approximately two high-quality posts/day at launch.



Discovery:

- three configurable scans/day;

- approximately ten candidates/scan;

- balance trending and under-covered topics;

- humans normally select a topic before full research.



Content:

- research in English;

- core information primarily English;

- natural Hinglish allowed for humour/commentary;

- information is primary;

- mascot supports rather than dominates;

- single page when sufficient;

- carousel when context genuinely requires it.



Initial formats:

- `GM-SINGLE-01`

- `GM-COMPARE-01`

- `GM-CAROUSEL-01`



Publishing:

- human final approval mandatory;

- manual publishing in version 1.



---



## Current Reliability Decisions



- Every factual claim intended for publication maps to stored evidence.

- Numeric values are structured.

- Derived arithmetic is performed by Python.

- Research and independent verification use different providers where practical.

- Factual copy is restricted to an approved claim allowlist.

- Important text is rendered by code, not an image model.

- Human approval references exact copy/render versions.

- Editing after approval invalidates the affected approval.

- High-risk stories require enhanced human review.

- Model/provider failures cause the workflow to stop safely rather than fabricate fallback facts.

- Golden Set regression testing will begin after the local pilot produces strong approved cases.



---



## Security Decisions



The GitHub repository is public.



Therefore:



- no secrets in Git;

- operational `data/`, databases, model outputs, logs, and exports must be ignored before runtime data is created;

- Telegram uses a human-user allowlist;

- source retrieval must block SSRF/private-network targets;

- web/source text is untrusted and may contain prompt injection;

- model text is escaped and cannot become raw executable HTML;

- Antigravity/Codex remain development tools only.



---



## Current Git Strategy



Stable reviewed checkpoints:

- `main`



Current specification branch:

- `spec/engineering-v0.1`



Do not merge the engineering branch until the remote diff has been reviewed.



Implementation should later use short-lived feature branches for meaningful milestones.



---



## Next Planned Work



1. Install engineering documents `08`–`15` and this `CURRENT_STATE.md` on `spec/engineering-v0.1`.

2. Run local diff/placeholder checks.

3. Push the branch.

4. Perform remote GitHub review of the exact branch contents.

5. Fix any discrepancy.

6. Merge the reviewed engineering specification to `main`.

7. Begin **Milestone 1 — Application Foundation** with a narrow Antigravity prompt.

8. Do not configure real provider keys until security/.gitignore foundation is in place.



---



## Current Rule



**No substantive production code before engineering specification v0.1 is remotely reviewed and accepted.**
