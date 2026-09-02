AGENTS.md

Purpose

This file defines the engineering rules for all AI coding agents, human contributors, and automation tools working on the Godi Monke Engine repository.

The repository specification is authoritative. Implementation must conform to the specification; specifications must not be silently changed to fit an implementation.

Repository Scope

Agents may work only inside the Godi Monke Engine repository unless a human explicitly authorizes otherwise.

Agents must not:

inspect unrelated personal files;

modify files outside the repository;

use sudo without explicit human approval;

expose, print, commit, or transmit secrets;

publish content to external platforms unless a human explicitly authorizes that capability in a later milestone;

silently alter canonical product rules;

add services, dependencies, APIs, or infrastructure that are outside the current milestone.

Canonical Documentation

Files under docs/canonical/ are human-owned product documents.

Agents may read them, but must not modify them unless a human explicitly instructs them to do so.

If code conflicts with a canonical requirement, stop and report the conflict. Do not rewrite the requirement to match the code.

Engineering documents under docs/engineering/ may evolve, but material architectural changes still require human approval.

Core Engineering Principles

Python owns workflow state. LLMs do not own application state.

Every external model call must be bounded, logged, and attributable to a prompt version.

Every factual claim intended for publication must originate from an evidence-backed claim record.

Creative generation must not modify locked factual values, dates, names, quantities, or source attributions.

Generative image models must not be responsible for rendering important factual infographic text.

Important text, numbers, citations, charts, and labels must be rendered deterministically by code.

No publishable post may bypass the verification stage.

No automatic publishing is allowed in version 1.

Every external integration must fail safely.

A failed model call must never silently fall back to unverified generated content.

Human approval is required before publication.

The system must preserve provenance: source, model, prompt version, timestamp, and workflow state.

Factual Integrity Rules

The engine must keep factual material separate from commentary, humour, and visual styling.

A publishable factual claim must have:

a stable claim ID;

exact claim text;

supporting source ID;

source URL or document reference;

supporting evidence or excerpt;

verification status;

confidence or risk status where applicable.

Numeric values must be stored as structured data and rendered from the claim ledger. They must not be regenerated from memory by a creative model.

If evidence is incomplete, conflicting, stale, or ambiguous, the system must preserve that uncertainty rather than inventing certainty.

Editorial Safety Rules

The engine is an information-first current-affairs publishing system with humour and commentary as presentation layers.

It must not implement:

political microtargeting;

voter profiling;

demographic persuasion optimization;

engagement manipulation aimed at changing political beliefs;

autonomous political publishing without human review.

For high-risk topics such as elections, protests, communal incidents, armed conflict, deaths, court decisions, or rapidly developing breaking news, the workflow must require stricter review and human approval.

Model Usage Rules

Models are replaceable components, not sources of truth.

Each model call must record, where available:

provider;

model name;

model snapshot/version;

prompt version;

input/output token usage;

estimated cost;

timestamp;

workflow stage;

success/failure state.

No model may be allowed to modify application state except through validated structured outputs accepted by the Python workflow.

Cost Rules

The application must support hard or configurable monthly API spending limits.

No implementation should assume unlimited paid API access.

Prefer low-cost models for discovery, extraction, classification, and routine transformation. Reserve more capable models for tasks where their quality materially improves reliability.

Security and Secrets

Secrets belong in environment variables or an approved secret store.

Never commit:

.env;

API keys;

Telegram bot tokens;

OAuth credentials;

cookies;

session files;

private certificates;

platform access tokens.

.env.example may contain variable names only, never real values.

Any accidental secret exposure must be reported immediately.

Git Discipline

Before substantial agent-driven changes, create or confirm a clean Git checkpoint.

Agents should make focused changes aligned with one milestone.

Do not rewrite large unrelated parts of the repository while implementing a small feature.

Do not force-push, rewrite history, or push to remote repositories unless explicitly instructed by a human.

Testing Requirements

Every implemented feature must include appropriate tests.

At minimum, test:

workflow state transitions;

validation of structured model outputs;

failure behaviour;

claim-to-source integrity;

deterministic rendering inputs;

cost-budget enforcement;

secrets/configuration handling where relevant.

A milestone is not complete if tests fail.

Milestone Discipline

Implement only the requested milestone.

Do not proactively build future features unless required to satisfy the current specification.

At the end of every milestone, report:

files created;

files modified;

tests added or changed;

tests executed and results;

unresolved questions;

deviations from specification;

security or reliability concerns discovered.

Then stop and wait for further instruction.

Current Product Rule

Until a later canonical document explicitly changes this rule:

The Godi Monke Engine may prepare and render content, but it must not automatically publish to Instagram, X, or any other external platform. A human must review and approve the final output.
