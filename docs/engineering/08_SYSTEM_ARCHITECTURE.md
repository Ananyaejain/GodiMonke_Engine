# 08_SYSTEM_ARCHITECTURE.md



## Status



Version: 0.1

Document type: Engineering specification

Owner: Human project team

Depends on: `AGENTS.md`, canonical documents `00`–`07`

Purpose: Define the runtime architecture of Godi Monke Engine before implementation begins.



---



## 1. Architecture Goal



Godi Monke Engine should be a small, inspectable Python application that automates repetitive editorial work while keeping factual provenance, workflow state, cost, and final approval under explicit control.



The architecture should optimize for:



- reliability over novelty;

- easy local development;

- low operating cost;

- replaceable AI providers;

- deterministic state management;

- transparent audit trails;

- human review;

- simple migration to a low-cost VPS later.



The application must continue to work even if Antigravity, Codex, or any coding assistant is unavailable.



---



## 2. Version 1 Runtime Boundary



Version 1 includes:



1. scheduled topic discovery;

2. topic review through Telegram;

3. source collection;

4. research packet creation;

5. claim extraction;

6. claim verification;

7. post planning;

8. copy drafting;

9. mascot asset selection/generation;

10. deterministic post rendering;

11. automated QA;

12. human approval;

13. export of final assets for manual publishing.



Version 1 does **not** include:



- autonomous Instagram publishing;

- autonomous X publishing;

- political microtargeting;

- voter profiling;

- demographic persuasion optimization;

- automatic editing of canonical product rules;

- a large local language model;

- a required VPS;

- Hermes Agent as a runtime dependency.



---



## 3. High-Level Architecture



```text

                    ┌──────────────────────┐

                    │  Scheduler / Manual  │

                    │       Trigger        │

                    └──────────┬───────────┘

                               │

                               v

                    ┌──────────────────────┐

                    │  Workflow Controller │

                    │  Python owns state   │

                    └──────────┬───────────┘

                               │

          ┌────────────────────┼────────────────────┐

          │                    │                    │

          v                    v                    v

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐

│ Discovery/Search │  │ AI Provider Layer│  │ Telegram Adapter │

│     Providers    │  │ text/image calls │  │ human decisions  │

└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘

         │                     │                     │

         └──────────────┬──────┴──────────────┬──────┘

                        │                     │

                        v                     v

              ┌──────────────────┐  ┌──────────────────┐

              │ Domain Services  │  │ Asset / Renderer │

              │ research, verify │  │ HTML/CSS + PNG   │

              └────────┬─────────┘  └────────┬─────────┘

                       │                     │

                       └──────────┬──────────┘

                                  v

                         ┌─────────────────┐

                         │ Persistence     │

                         │ SQLite + files  │

                         └─────────────────┘

```



---



## 4. Architectural Rule: Python Owns the Workflow



LLMs are workers.



They may:



- propose topic candidates;

- extract structured facts;

- summarize evidence;

- classify risk;

- draft copy;

- propose humour;

- recommend visual ideas;

- verify claim/source support.



They may **not**:



- decide application state directly;

- mutate the database outside validated service calls;

- skip workflow stages;

- publish content;

- silently replace failed evidence;

- change locked facts.



All state transitions are executed by Python after validation.



---



## 5. Recommended Technology Baseline



The initial implementation should use:



- **Python 3.12+**

- **Pydantic v2** for validated domain/API schemas

- **SQLAlchemy 2.x** for persistence

- **Alembic** for database migrations

- **SQLite** for initial local and low-volume production storage

- **python-telegram-bot** or an equivalent mature Telegram library

- **httpx** for HTTP integrations

- **Jinja2 + HTML/CSS** for deterministic visual templates

- **Playwright/Chromium** for fixed-dimension screenshots, unless later benchmarking identifies a simpler deterministic renderer

- Python standard `logging` with structured fields

- `pytest` for tests



A dependency should not be added merely because it is convenient. Each new runtime dependency must have a clear role.



---



## 6. Database Strategy



### Initial database



SQLite is sufficient for:



- two human users;

- approximately two posts per day;

- three discovery scans per day;

- low concurrent write volume;

- local development;

- a small VPS later.



SQLite should run with:



- foreign keys enabled;

- WAL mode where appropriate;

- migrations;

- UTC timestamps;

- explicit transactions.



### Future migration



The persistence layer should avoid SQLite-specific application logic where practical so PostgreSQL can be introduced later if concurrency or scale requires it.



PostgreSQL is **not** required for version 1.



---



## 7. File Storage Strategy



Large or versioned artifacts should live on disk rather than inside SQLite blobs.



Examples:



```text

data/

├── discovery/

├── sources/

│   ├── raw/

│   └── extracted/

├── research_packets/

├── model_outputs/

├── renders/

├── exports/

└── cache/

```



Repository-controlled permanent brand assets remain under:



```text

assets/

```



Database records should store:



- stable IDs;

- paths;

- hashes;

- metadata;

- provenance.



Generated or downloaded artifacts under `data/` should generally remain outside Git unless explicitly selected as fixtures or Golden Set examples.



---



## 8. Application Package Layout



Target layout:



```text

src/godi_monke/

├── __init__.py

├── config/

│   ├── settings.py

│   └── logging.py

├── db/

│   ├── base.py

│   ├── session.py

│   ├── models.py

│   └── repositories/

├── domain/

│   ├── enums.py

│   ├── schemas.py

│   └── errors.py

├── services/

│   ├── discovery.py

│   ├── source_collection.py

│   ├── research.py

│   ├── claims.py

│   ├── verification.py

│   ├── post_planning.py

│   ├── copywriting.py

│   ├── mascot.py

│   ├── rendering.py

│   ├── qa.py

│   ├── budget.py

│   └── audit.py

├── workflows/

│   ├── controller.py

│   ├── transitions.py

│   └── scheduler.py

├── integrations/

│   ├── base/

│   ├── ai/

│   ├── search/

│   ├── image/

│   └── telegram/

├── rendering/

│   ├── context.py

│   └── renderer.py

├── cli/

│   └── main.py

└── utils/

```



The existing repository skeleton may be adjusted to match this layout during implementation, but canonical docs must not be changed to hide implementation conflicts.



---



## 9. Layer Responsibilities



### 9.1 Domain Layer



Contains:



- enums;

- validated data shapes;

- domain errors;

- state definitions.



Must not know about Telegram, Gemini, OpenAI, Playwright, or filesystem implementation details.



### 9.2 Persistence Layer



Contains:



- ORM models;

- migrations;

- repositories;

- transactions.



Must not contain editorial logic.



### 9.3 Service Layer



Contains business rules.



Examples:



- scoring a topic;

- creating a research packet;

- mapping claims to evidence;

- deciding whether a claim requires human review;

- validating a post against locked claims;

- selecting a reusable mascot asset.



Services should depend on provider interfaces, not vendor-specific clients.



### 9.4 Integration Layer



Contains adapters for:



- model providers;

- search providers;

- image providers;

- Telegram;

- source retrieval.



Vendor-specific behavior must remain here.



### 9.5 Workflow Layer



Coordinates services and moves entities between allowed states.



The workflow layer should not contain model prompts or image-layout CSS.



### 9.6 Rendering Layer



Converts a validated `PostRenderSpec` into deterministic visual output.



It may receive an approved mascot image.



It must not invent factual content.



---



## 10. Provider Abstractions



Version 1 should define narrow interfaces.



Conceptual examples:



```python

class TextModelProvider:

    async def generate_structured(self, request, output_schema): ...



class SearchProvider:

    async def search(self, query, *, freshness=None, limit=10): ...



class ImageProvider:

    async def generate_or_edit(self, request): ...



class NotificationProvider:

    async def send_review_item(self, item): ...

```



Do not create a universal “AI agent” interface that hides all provider behavior.



Each provider call must expose enough metadata for:



- model/provider identity;

- cost;

- tokens;

- errors;

- timestamps;

- traceability.



---



## 11. Structured-Output Rule



Any model output used by application logic must be validated against a Pydantic or JSON schema.



Free-form prose may be stored as editorial content, but it must never be parsed informally to drive critical state transitions.



Invalid structured output should:



1. fail validation;

2. be logged;

3. optionally receive a bounded repair/retry;

4. fail safely after the retry limit.



It must not silently become accepted data.



---



## 12. Topic Discovery Flow



```text

Scheduled/manual trigger

        ↓

Discovery provider(s)

        ↓

candidate normalization

        ↓

deduplication

        ↓

scoring/classification

        ↓

persist Topic records

        ↓

Telegram topic cards

        ↓

human SELECT / SAVE / SKIP

```



Each scan should aim for approximately ten useful candidates.



Full research should not automatically run for all candidates.



---



## 13. Research Flow



```text

SELECTED topic

      ↓

source discovery

      ↓

source retrieval

      ↓

source metadata + hash

      ↓

evidence extraction

      ↓

research packet

      ↓

claim extraction

      ↓

claim/source mapping

      ↓

verification

```



The research service must preserve:



- source provenance;

- uncertainty;

- conflicting evidence;

- missing evidence;

- retrieval failures.



---



## 14. Verification Flow



The verifier should evaluate narrow claim/evidence packages.



Where practical, it should not receive:



- desired headline;

- intended joke;

- preferred political conclusion.



Verification output must be structured.



The Python service decides whether a claim is:



- publishable;

- blocked;

- human-review-required.



---



## 15. Post Creation Flow



```text

verified research packet

        ↓

format planner

        ↓

structured post plan

        ↓

copy draft

        ↓

claim-lock validation

        ↓

human copy review

        ↓

mascot asset selection/generation

        ↓

render specification

        ↓

deterministic render

        ↓

automated QA

        ↓

human final review

        ↓

export

```



No post may enter final review while unsupported factual assertions remain in its structured content.



---



## 16. Rendering Architecture



The renderer should accept a structured object, not a paragraph prompt.



Example conceptual input:



```json

{

  "template_id": "GM-CAROUSEL-01",

  "template_version": "1.0",

  "slides": [

    {

      "role": "HOOK",

      "headline": "Example",

      "claim_refs": [],

      "commentary": null,

      "mascot_asset_id": "..."

    }

  ]

}

```



The rendering pipeline should:



1. load the template;

2. resolve claim-backed values from structured post data;

3. resolve approved assets;

4. render at fixed dimensions;

5. export PNG;

6. compute output hash;

7. store render metadata.



The image model should never be asked to reproduce the final infographic text.



---



## 17. Telegram Architecture



Telegram is the version 1 human control surface.



Initial interactions should support:



- view topic candidates;

- select topic;

- save topic;

- skip topic;

- request research;

- view research summary;

- approve/reject research;

- request draft;

- approve/edit/reject copy;

- request art change;

- approve/reject final render.



Telegram commands/buttons must call workflow services.



Telegram callback code must not directly mutate database models.



---



## 18. Scheduling



The exact three daily scan times remain configurable.



Scheduling requirements:



- timezone-aware;

- idempotent;

- no duplicate scan if a previous run is still active;

- manual discovery must remain available;

- failures must be logged and surfaced.



The scheduler should invoke the same workflow entry point used by a manual trigger.



---



## 19. Idempotency



Externally-triggered operations must be safe against retries.



Examples:



- Telegram callback received twice;

- discovery job retried;

- model request timed out after provider accepted it;

- renderer rerun.



Where meaningful, operations should use stable request IDs or workflow IDs.



Repeated approval callbacks must not create duplicate posts or transitions.



---



## 20. Audit Logging



Important actions should generate an audit event:



- topic discovered;

- human selected/skipped;

- source retrieved;

- claim created;

- claim verified;

- model call made;

- workflow state changed;

- copy approved/rejected;

- render approved/rejected;

- final asset exported.



Audit logs should identify actor type:



- `HUMAN`;

- `SYSTEM`;

- `MODEL`.



Do not store private model chain-of-thought. Store only concise, reviewable rationale where needed.



---



## 21. Error Handling



Errors should be categorized.



Examples:



- validation error;

- provider unavailable;

- rate limit;

- budget blocked;

- source unavailable;

- verification failed;

- rendering failed;

- Telegram delivery failed.



A workflow must stop safely at the failed stage.



A provider error must never cause the engine to fabricate substitute facts.



---



## 22. Cost Enforcement



All paid provider calls must pass through a budget-aware wrapper.



Before a paid call:



1. identify provider/model;

2. estimate or bound cost where possible;

3. check monthly/provider budget;

4. reject or route differently if blocked.



After the call:



1. record actual token/usage data where available;

2. record estimated INR cost;

3. update the monthly ledger.



Budget enforcement must not depend on human memory.



---



## 23. Security Boundary



Version 1 is not a public web service.



Preferred initial operation:



- local machine;

- Telegram long polling;

- no public inbound HTTP port;

- secrets in environment variables;

- database and assets local.



When moved to a VPS, public exposure should remain minimal.



Source fetchers must later implement:



- HTTP/HTTPS-only rules;

- private/local IP rejection;

- timeouts;

- download-size limits;

- redirect limits.



---



## 24. Testing Architecture



Required test layers:



### Unit

- state transitions;

- validation;

- cost rules;

- claim-lock checks;

- deduplication;

- format selection.



### Integration

- SQLite repositories;

- migrations;

- fake provider adapters;

- Telegram callback routing;

- deterministic renderer.



### Golden / Regression

Later, approved cases should verify:



- research packet structure;

- claim extraction;

- copy quality constraints;

- rendering consistency.



Tests should use fake providers by default and must not spend paid API credits unless explicitly marked.



---



## 25. Local-First Deployment



Development should run from a Python virtual environment on the team's laptop.



Version 1 should support commands similar to:



```text

godi-monke db upgrade

godi-monke bot

godi-monke discover --manual

godi-monke render <post-id>

godi-monke doctor

```



Exact command syntax is implementation detail, but a basic CLI is required for troubleshooting without Telegram.



---



## 26. VPS Migration



The future VPS deployment should require minimal architectural change.



Expected migration:



```text

local Python process

        ↓

same Python package on VPS

        ↓

same database abstraction

        ↓

same Telegram long polling

        ↓

scheduled jobs run continuously

```



A process supervisor such as systemd may be used later.



Docker is optional and not required for version 1.



---



## 27. Architecture Non-Goals



Do not introduce during initial implementation unless a later spec explicitly requires them:



- Kubernetes;

- microservices;

- Kafka;

- Redis;

- Celery;

- vector databases;

- multi-agent orchestration frameworks;

- event buses;

- distributed queues;

- separate web frontend;

- GraphQL;

- cloud object storage.



The expected workload does not justify them.



---



## 28. Definition of Architectural Success



The architecture is successful when:



- one provider can be replaced without rewriting the workflow;

- a failed model cannot corrupt workflow state;

- every factual claim can be traced to evidence;

- every post can be reproduced from stored structured data and template version;

- every expensive API call can be accounted for;

- the system can run locally;

- a human can operate it through Telegram;

- a new ChatGPT/Antigravity session can understand the project from repository state.



---



## 29. Golden Rule



**Keep the workflow deterministic around the AI. Use AI where judgement or generation helps; use software where correctness and repeatability matter.**
