# 00_PROJECT_CHARTER.md

## Status

Version: 0.1  
Document type: Canonical  
Owner: Human project team  
Purpose: Define what the Godi Monke Engine is, what it is trying to achieve, and the constraints all later engineering decisions must respect.

## 1. Project Definition

Godi Monke Engine is a small-team, AI-assisted current-affairs content production system designed for Instagram and X.

Its purpose is to help the team discover interesting topics, gather evidence, verify factual claims, structure concise informational posts, add a consistent mascot-driven humour layer, and produce high-quality single-page or carousel graphics for human review.

The engine is not intended to replace editorial judgement. It is intended to reduce repetitive work while preserving factual reliability, visual consistency, source traceability, and a stable brand identity over time.

## 2. Team Model

The project is operated by two human owners with ChatGPT used as an architecture, editorial, specification, and quality-support collaborator.

AI coding tools such as Antigravity or Codex are development tools only. They are not part of the production runtime unless explicitly approved in a later architectural decision.

The humans remain final editorial owners.

## 3. Initial Publishing Goal

The launch target is approximately two high-quality posts per day.

The system should choose the appropriate format based on information density:

- a single-page post when the topic can be communicated clearly in one frame;
- a carousel when the topic needs evidence, context, comparison, sequence, or explanation across multiple frames.

Quality takes priority over volume during the initial phase.

Volume may increase only after the workflow demonstrates stable quality and reliability across a meaningful number of posts.

## 4. Content Character

The content style combines concise current-affairs information, evidence-backed factual explanation, simple English for core information, occasional Hinglish for humour or personality, a recurring Godi Monke mascot, meme-aware visual language, and commentary or satire that remain visibly separate from factual claims.

The mascot should behave like a recurring character rather than a static logo pasted onto every design.

Humour should support readability and personality. It must not obscure, alter, or replace the underlying information.

## 5. Topic Scope

The discovery system should look for both trending topics — subjects that are currently receiving substantial public attention — and under-covered topics — matters with credible importance, evidence, or public relevance that are receiving comparatively little attention.

Likely subject areas include Indian public policy, budgets, economics, infrastructure, foreign policy, geopolitics, political claims, major public controversies, institutional decisions, protests, court developments, official data, and other current-affairs topics relevant to the audience.

Topic discovery is not itself evidence. Every selected topic must go through research and verification before becoming publishable content.

## 6. Research Philosophy

The engine should prefer evidence over narrative.

Research should prioritize primary and authoritative material when available, including official documents, government publications, regulators, courts, statistical agencies, parliamentary material, budget documents, institutional reports, and direct original statements.

Secondary reporting may be used for context, discovery, or corroboration.

Social platforms, commentary channels, creators, and viral posts may be used as discovery signals, but they must not automatically be treated as factual evidence.

## 7. Claim-Checking Model

When a public figure, party, institution, or commentator makes a factual claim, the system should evaluate the measurable claim rather than start from a desired conclusion.

The workflow should identify what was actually said, which parts are factual or measurable, what evidence supports the claim, what evidence contradicts it, what context is missing, and whether the conclusion is supported, partly supported, mixed, contradicted, or not established.

Humour and commentary may be added only after the factual assessment is complete.

## 8. Separation of Facts and Creative Layers

The production system must maintain separate internal layers for facts, analysis, commentary, and humour.

Facts are locked, evidence-backed claims. Analysis is interpretation or explanatory context. Commentary is editorial framing. Humour includes punchlines, Hinglish lines, mascot reactions, and meme-style presentation.

Creative models must never be allowed to rewrite locked facts.

## 9. Source and Claim Provenance

Every factual claim intended for publication should be traceable to a stored source.

The system should maintain a claim ledger containing, where applicable, claim ID, claim text, numeric values, dates, entities, source ID, supporting evidence, verification result, and confidence or risk status.

Published numbers should be rendered from structured records rather than regenerated by a language or image model.

## 10. Visual Production Philosophy

AI should generate creative assets, especially mascot poses, scenes, expressions, and optional backgrounds.

AI image models should not be trusted to typeset important factual information.

Headlines, numbers, charts, labels, citations, slide numbers, and source text should be rendered deterministically using code-driven templates such as HTML/CSS, SVG, or another reproducible rendering system.

The first production template set should stay deliberately small: single-page explainer, comparison post, and carousel explainer.

Additional formats should be added only after the core set is stable.

## 11. Mascot Consistency

The Godi Monke mascot must have a permanent reference set stored in the repository.

The system should not depend on chat history or model memory to remember the character.

The mascot reference set should eventually include a master image, front and three-quarter views, a full-body reference, an expression sheet, clothing/accessory rules, a colour palette, and approved recurring poses.

Generated mascot art must reference the canonical character assets whenever consistency matters.

## 12. Human Approval

Version 1 must not automatically publish content.

The intended workflow is:

**topic discovery → human selection → research → verification → draft → human copy review → mascot/art generation → deterministic rendering → QA → human approval → manual publishing**

Automatic platform publishing may be considered only after the system has demonstrated reliable operation and the human owners explicitly approve that change.

## 13. Daily Discovery Cadence

The initial discovery goal is three scans per day.

Each scan should produce approximately ten candidate topics, ideally balancing currently hot or widely discussed subjects with under-covered but potentially important subjects.

The system should avoid wasting expensive research tokens on every discovered topic. Full research should begin primarily after human selection.

## 14. Budget Constraint

The project has an approximate total monthly operating ceiling of ₹5,000.

Current expected commitments include ChatGPT Plus, X-related subscription costs, optional low-cost hosting, and pay-as-you-go AI/API usage.

Architecture decisions must be compatible with this budget.

The engine should favour free or open-source infrastructure and use paid APIs selectively. A second large AI subscription should not be assumed.

## 15. Hosting Strategy

The initial development system may run locally on the team's existing laptop.

A VPS is optional during development.

A low-cost VPS should be considered when the workflow becomes stable and reliable three-times-daily scheduling is important enough that the system should operate independently of the laptop being awake.

The production application must not depend on Antigravity, Codex, or any coding agent being installed.

## 16. Memory and Long-Term Consistency

Chat history is not project memory. The repository is the project memory.

Canonical documentation, prompt versions, schemas, approved mascot references, templates, research packets, claim records, and current project state must be stored as files or structured data.

The project must include a `CURRENT_STATE.md` file summarizing the current version, current milestone, completed work, work in progress, not-yet-started work, active decisions, and known issues.

This allows a new AI session or human contributor to regain project context without relying on a long conversation.

## 17. Quality Stability

The system should improve through controlled versioning rather than vague long-term model memory.

The team should build a Golden Set of approved posts and research cases.

Changes to prompts, models, templates, rendering, or verification rules should be evaluated against representative Golden Set examples before they are treated as production improvements.

A change that increases novelty but reduces factual reliability, readability, brand consistency, or source traceability should not be deployed.

## 18. Safety and Editorial Boundaries

The system is intended to support information-first publishing with commentary and satire.

It must not be designed for political microtargeting, voter profiling, demographic persuasion optimization, or automated attempts to manipulate the political beliefs of specific groups.

High-risk breaking-news topics require stricter verification and more human attention.

When reliable evidence is unavailable, the correct output is uncertainty, delay, or rejection — not confident invention.

## 19. Version 1 Success Criteria

Version 1 is successful when the team can reliably:

1. receive useful topic candidates three times per day;
2. select a topic for research;
3. produce a structured research packet;
4. maintain a claim-to-source ledger;
5. independently verify claims;
6. generate a structured post plan;
7. create a consistent mascot asset;
8. render a single-page or carousel post from deterministic templates;
9. receive the preview for human review;
10. approve or reject the final output without relying on hidden chat memory.

The system should reach this state before automatic publishing or significant volume scaling is considered.

## 20. Guiding Principle

**Automate repetition. Preserve judgement. Lock facts. Keep creativity flexible.**
