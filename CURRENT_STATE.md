# CURRENT_STATE.md

## Project

**Name:** Godi Monke Engine  
**Current project stage:** Foundation / specification  
**Document version:** 0.1  
**Status:** Pre-implementation

---

## Current Milestone

**Milestone 0B — Canonical product specification**

The repository skeleton exists. The current focus is defining the product, brand, editorial, source, fact-checking, mascot, and content-format rules before application logic is implemented.

---

## Completed

- Initial repository/directory skeleton created.
- Git repository created and mirrored to the public GitHub repository.
- `AGENTS.md` drafted.
- `docs/canonical/00_PROJECT_CHARTER.md` drafted.
- `docs/canonical/01_BRAND_BIBLE.md` drafted.
- `docs/canonical/02_MASCOT_BIBLE.md` drafted.
- `docs/canonical/03_VOICE_AND_HUMOUR.md` drafted.
- `docs/canonical/04_EDITORIAL_POLICY.md` drafted.
- `docs/canonical/05_SOURCE_POLICY.md` drafted.
- `docs/canonical/06_FACT_CHECKING_PROTOCOL.md` drafted.
- `docs/canonical/07_CONTENT_FORMATS.md` drafted.

---

## In Progress

- Human review and consistency audit of the canonical documentation pack.
- Preparing the engineering specification set.
- Preparing the canonical mascot reference assets.

---

## Not Started

- Python application skeleton.
- Configuration system.
- SQLite schema.
- Workflow state machine.
- Telegram interface.
- Topic discovery integration.
- Research pipeline.
- Claim ledger implementation.
- Independent verification.
- Content planner.
- Mascot-generation pipeline.
- Deterministic HTML/SVG renderer.
- Automated QA.
- API cost accounting.
- VPS deployment.
- Instagram/X publishing integrations.

---

## Current Product Decisions

- Target: approximately **two high-quality posts per day** during launch.
- Quality takes priority over volume.
- Topic discovery runs approximately **three times per day**.
- Each scan should surface approximately **10 candidate topics**.
- Discovery should deliberately include:
  - trending/high-attention topics;
  - under-covered but potentially important topics.
- Research language: **English**.
- Post information language: primarily **English**.
- Humour/commentary may use natural **Hinglish**.
- Posts may be single-page or carousel depending on information density.
- Initial production formats:
  - `GM-SINGLE-01`;
  - `GM-COMPARE-01`;
  - `GM-CAROUSEL-01`.
- Human approval is mandatory before publication.
- Version 1 has **no automatic publishing**.
- Antigravity is a development tool only and is not part of the production runtime.
- Codex may later be used as an independent code reviewer.
- Python will own workflow state.
- LLMs will be replaceable bounded components.
- Important factual infographic text will be rendered deterministically by code.
- Generative image models will primarily create mascot art and supporting visuals.
- Factual claims must map to stored source-backed claim records.
- Commentary and humour must remain separate from locked factual claims.
- High-risk stories require stricter verification and human review.

---

## Infrastructure Decisions

### Development

Run locally first.

Available local machine:
- 16 GB RAM;
- GTX-class consumer GPU;
- model inference expected to use external APIs rather than large local models.

### VPS

No VPS is required during the first implementation stage.

A low-cost VPS should be considered once:
- the workflow is stable;
- scheduled discovery needs to run while local machines are offline;
- the team is ready for always-on operation.

---

## Budget

Approximate total monthly ceiling:

**₹5,000**

Known/expected allocations:

- ChatGPT Plus: approximately ₹2,000;
- X subscription: approximately ₹500;
- optional VPS: approximately ₹400;
- remaining budget available for pay-as-you-go model/search/API usage.

The final cost policy and provider routing are not yet frozen.

---

## Team Workflow

### Human owners
- make product decisions;
- select topics;
- review evidence;
- approve copy;
- approve visuals;
- approve publication.

### ChatGPT
- architecture;
- canonical documentation;
- editorial/system design;
- implementation specifications;
- QA/review support;
- precise Antigravity task prompts.

### Antigravity
- primary implementation agent with controlled computer access;
- implements only defined milestones;
- must obey `AGENTS.md`.

### Codex
- optional independent engineering reviewer after meaningful implementation exists.

---

## Repository Policy

Canonical documents are human-owned.

Coding agents may read but must not silently modify product rules.

Important stable checkpoints should be committed and pushed to GitHub only after review.

Before recommending a major push, the affected specification or implementation should be checked for:

- internal contradictions;
- architecture drift;
- missing safety/verification gates;
- factual-provenance weaknesses;
- unintended scope changes;
- security mistakes;
- test failures;
- secret exposure;
- inconsistency with earlier canonical decisions.

---

## Known Open Items

- Canonical mascot master/reference files have not yet been installed into the repository.
- Exact API/model routing is still provisional.
- Exact discovery scan times are not yet fixed.
- Telegram bot design is specified conceptually but not engineered.
- Final database schemas have not been written.
- Final workflow state transitions have not been written.
- Exact template dimensions and typography are not yet frozen.
- No production code should be written until the engineering specification is sufficiently defined.

---

## Next Planned Work

1. Complete the human review of canonical documents `00`–`07`.
2. Add the locked mascot master asset and begin the mascot reference pack.
3. Draft engineering documents:
   - `08_SYSTEM_ARCHITECTURE.md`;
   - `09_DATA_MODEL.md`;
   - `10_WORKFLOW_STATE_MACHINE.md`;
   - `11_MODEL_ROUTING.md`;
   - `12_QA_GATES.md`;
   - `13_COST_POLICY.md`;
   - `14_SECURITY_AND_SECRETS.md`;
   - `15_ROADMAP.md`.
4. Freeze the first engineering milestone.
5. Give Antigravity the first implementation prompt.

---

## Current Rule

**Do not begin substantive implementation until the current specification checkpoint has been reviewed and deliberately accepted.**
