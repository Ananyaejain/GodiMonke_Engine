# 15_ROADMAP.md



## Status



Version: 0.1

Document type: Engineering specification

Owner: Human project team

Purpose: Define the implementation sequence for Antigravity and the human review checkpoints that prevent architecture drift.



---



## 1. Roadmap Principle



Build vertically and incrementally.



Do not attempt to build the complete AI pipeline in one prompt.



Every milestone should:



1. have a narrow scope;

2. start from a reviewed Git checkpoint;

3. implement only its specification;

4. include tests;

5. produce an Antigravity completion report;

6. receive human/ChatGPT review;

7. be committed only when stable;

8. be pushed at meaningful checkpoints.



---



## 2. Current Stage



Canonical product specification `00`–`07` is established.



Engineering specification `08`–`15` must be reviewed and accepted before substantive implementation.



No runtime API integration should be built before the mechanical application spine works with fake providers.



---



## 3. Milestone 0C — Engineering Specification Freeze



### Scope



Install reviewed:



- `08_SYSTEM_ARCHITECTURE.md`

- `09_DATA_MODEL.md`

- `10_WORKFLOW_STATE_MACHINE.md`

- `11_MODEL_ROUTING.md`

- `12_QA_GATES.md`

- `13_COST_POLICY.md`

- `14_SECURITY_AND_SECRETS.md`

- `15_ROADMAP.md`



Update `CURRENT_STATE.md`.



### No code.



### Exit criteria



- no placeholders in `08`–`15`;

- canonical `00`–`07` unchanged;

- engineering documents cross-checked;

- Git diff clean;

- remote branch reviewed before merge.



### Git checkpoint



Yes.



Use dedicated branch:



`spec/engineering-v0.1`



---



## 4. Milestone 1 — Application Foundation



### Scope



Create the runnable Python project foundation only.



Implement:



- `pyproject.toml`;

- local virtual environment instructions;

- package initialization;

- settings/config layer;

- structured logging;

- CLI shell;

- test configuration;

- safe directory/path configuration;

- `.env.example` variable names;

- `.gitignore` runtime-data hardening;

- basic `doctor` command.



### Do not implement



- Gemini/OpenAI;

- Telegram;

- database domain entities;

- rendering;

- discovery.



### Tests



- configuration validation;

- storage-root/path safety;

- logging redaction basics;

- CLI starts.



### Exit criteria



`pytest` passes and no external paid API is called.



---



## 5. Milestone 2 — Domain Model, Database, and State Machine



### Scope



Implement:



- enums;

- Pydantic domain schemas;

- SQLAlchemy base/session;

- SQLite;

- Alembic migrations;

- core tables from `09_DATA_MODEL.md`;

- repositories;

- workflow transition engine;

- audit event writing;

- optimistic/version checks.



### Do not implement



real external providers.



### Tests



- all legal transitions;

- illegal transitions;

- approval invalidation;

- transactions;

- foreign keys;

- stale-claim behavior;

- high-risk block;

- duplicate approval safety.



### Exit criteria



Mechanical state engine is reliable using local fixtures.



### Git checkpoint



Yes. This is a major architecture checkpoint.



---



## 6. Milestone 3 — Fake-Provider Vertical Slice



### Goal



Prove one complete mechanical path before real AI.



### Flow



```text

fake discovered topic

        ↓

human-like CLI selection

        ↓

fake research packet

        ↓

fake verified claims

        ↓

fake post plan

        ↓

fake approved mascot asset

        ↓

render specification

        ↓

placeholder render/export

```



### Scope



- fake provider interfaces;

- workflow orchestration;

- fixture data;

- CLI commands;

- audit trail.



### Exit criteria



A complete fake post can travel through legal states without external services.



---



## 7. Milestone 4 — Telegram Editorial Control Plane



### Scope



Implement private Telegram bot using long polling.



Features:



- configured allowlisted users;

- topic cards;

- select/save/skip;

- research-review actions using fake data;

- copy approval/rejection using fake data;

- final approval using fake render;

- idempotent callbacks.



### Security



Unauthorized users rejected.



### Tests



Handlers call workflow services; they do not mutate persistence directly.



### Exit criteria



The two owners can operate the fake workflow from Telegram.



### Git checkpoint



Yes.



---



## 8. Milestone 5 — Deterministic Renderer v1



### Scope



Implement:



- `GM-SINGLE-01`;

- `GM-COMPARE-01`;

- `GM-CAROUSEL-01`;

- Jinja2/HTML/CSS;

- fixed template dimensions configured explicitly;

- Playwright screenshot/export;

- local fonts/assets;

- text escaping;

- no external network during final render where practical;

- layout QA hooks.



Use fixture claims and mascot assets only.



### Exit criteria



Same render specification produces reproducible output.



Text/numbers come from structured data.



### Human design checkpoint



Yes.



The team should approve typography, spacing, visual hierarchy, source-note style, and mascot zones before real content automation.



---



## 9. Milestone 6 — Topic Discovery v1



### First paid/provider integration



Implement Google Gemini adapter.



Scope:



- Gemini 3.7 Flash;

- Search grounding;

- structured discovery output;

- trending + under-covered candidates;

- candidate normalization;

- deduplication;

- cost/search usage records;

- three configurable scan windows;

- manual discovery trigger.



### Safety



Do not research every candidate.



### Pilot



Run discovery manually first.



Evaluate several scans before enabling schedule.



### Exit criteria



Humans consistently consider the candidate list useful.



---



## 10. Milestone 7 — Source Retrieval and Research Packet



### Scope



Implement:



- safe HTTP fetcher;

- SSRF protections;

- source canonicalization;

- metadata;

- HTML/text extraction;

- bounded PDF handling;

- source file hashing;

- source-tier classification assistance;

- Gemini research synthesis;

- research packet schema.



### Prompt-injection boundary



Fetched source text is data only.



### Exit criteria



A selected topic produces a traceable research packet whose claims can be checked against stored source material.



### Git checkpoint



Yes.



---



## 11. Milestone 8 — Claim Ledger and Independent Verification



### Scope



Implement:



- atomic claim extraction;

- claim evidence mapping;

- numeric structured values;

- Python-derived arithmetic;

- verification adapter for GPT-5.6 Terra;

- verdict schema;

- human-review triggers;

- claim-lock service.



### Important



The OpenAI verifier is independent of the Gemini research conclusion.



### Exit criteria



Every factual assertion intended for a post can be traced to a verified claim/evidence record.



### Git checkpoint



Yes. This is one of the most important reliability checkpoints.



---



## 12. Milestone 9 — Post Planner, Copy, and Humour Layer



### Scope



Implement:



- format selection;

- structured slide plan;

- claim allowlist;

- informational copy;

- optional commentary/humour;

- Hinglish style constraints;

- unsupported-fact lint;

- human copy approval.



### Safety



No political microtargeting or persuasion-optimization objective.



### Exit criteria



Drafts are readable, on-brand, and cannot change locked factual values.



---



## 13. Milestone 10 — Mascot Library and Image Generation



### Before automation



Humans install/approve:



- locked logo;

- master mascot reference;

- initial reference sheet;

- initial reusable pose library.



### Scope



Implement:



- asset metadata/index;

- approved asset search;

- reuse-before-generate;

- Gemini 3.1 Flash Image adapter;

- reference-image generation;

- generation limits/cost tracking;

- new-asset human approval.



### Exit criteria



Custom generations consistently look like the same Godi Monke character.



---



## 14. Milestone 11 — End-to-End QA and Final Preview



### Scope



Implement all gates in `12_QA_GATES.md`.



Include:



- source/claim checks;

- claim-lock;

- risk rules;

- render layout checks;

- source-note checks;

- final Telegram preview;

- warnings;

- exact render-version approval.



### Exit criteria



No unsupported factual claim can reach `APPROVED` through the normal workflow.



---



## 15. Milestone 12 — Local Pilot



### Duration



At least enough time to produce approximately 20–30 serious test/production-candidate posts.



### Operation



- local laptop;

- manual/scheduled discovery;

- human topic selection;

- human approval;

- manual Instagram/X posting.



### Measure



- candidate usefulness;

- research corrections;

- verification disagreements;

- cost per completed post;

- API failures;

- time per post;

- mascot consistency;

- human edits required;

- recurring template issues.



### Golden Set



Select the strongest approved cases as regression fixtures.



### Exit criteria



The workflow is stable enough that failures are understood and quality is consistent.



### Git checkpoint



Yes.



---



## 16. Milestone 13 — VPS Decision / Always-On Deployment



Only after local pilot.



Questions:



- Are scheduled scans being missed because laptop is offline?

- Is local operation inconvenient?

- Is monthly API usage within budget?

- Is the application stable enough for unattended scheduling?



If yes:



- acquire low-cost VPS;

- install same Python application;

- configure systemd or equivalent;

- migrate SQLite/database safely;

- configure backup;

- keep Telegram long polling;

- expose no unnecessary public ports.



---



## 17. Milestone 14 — Publishing Automation



Deferred.



Version 1 manual publishing remains acceptable.



Only consider automated Instagram/X publishing if:



- platform API access is practical;

- economics make sense;

- human final approval remains mandatory;

- credentials can be stored safely;

- posting automation adds meaningful value.



Never make publishing autonomous merely because it is technically possible.



---



## 18. Antigravity Working Protocol



For each implementation milestone:



### Before work



- confirm correct branch;

- `git status`;

- create/checkpoint clean commit;

- read `AGENTS.md`;

- read relevant canonical/engineering docs.



### Prompt



Antigravity receives one milestone only.



Prompt must specify:



- files/specs to read;

- allowed scope;

- prohibited scope;

- tests required;

- no automatic commit/push unless explicitly requested.



### After work



Antigravity reports:



1. files created;

2. files modified;

3. dependencies added;

4. migrations added;

5. tests run;

6. test results;

7. deviations;

8. unresolved questions;

9. security concerns.



Then stop.



---



## 19. Codex Review Protocol



Codex is optional during early milestones.



Use it at important checkpoints as an independent reviewer.



Default review instruction:



- read-only;

- compare implementation against specifications;

- identify architecture drift;

- identify security/reliability issues;

- identify missing tests;

- do not rewrite code automatically.



Relevant findings are then deliberately sent back to Antigravity.



---



## 20. Git / Branch Policy



Recommended:



- `main` — reviewed stable checkpoints;

- short-lived `spec/...` branches for specification changes;

- short-lived `feature/...` branches for meaningful implementation milestones.



Do not create complicated GitFlow.



Push when:



- specification set is stable;

- major mechanical subsystem is complete;

- a risky change needs remote review;

- a rollback checkpoint would be valuable.



Do not push after every trivial local edit merely for ceremony.



---



## 21. Definition of “Done” for a Milestone



A milestone is not done because Antigravity says “done.”



It is done when:



- requested scope exists;

- prohibited scope was not added;

- tests pass;

- no secrets are exposed;

- diff is understandable;

- implementation matches spec;

- humans/ChatGPT have reviewed material deviations;

- Git checkpoint is made where appropriate.



---



## 22. Golden Rule



**Small milestone, tested implementation, reviewed diff, stable checkpoint — then move forward.**
