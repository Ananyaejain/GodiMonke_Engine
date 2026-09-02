# 04_EDITORIAL_POLICY.md

## Status

Version: 0.1  
Document type: Canonical  
Owner: Human project team  
Purpose: Define what the Godi Monke Engine may publish, how editorial judgement is applied, and where mandatory human review is required.

---

## 1. Editorial Principle

Godi Monke is an information-first current-affairs brand with commentary, humour, and a declared political identity.

The editorial workflow must distinguish:

- factual reporting;
- factual analysis;
- interpretation;
- opinion;
- satire;
- humour.

These categories may coexist in one post, but they must not be blurred in a way that makes commentary look like evidence.

---

## 2. Human Editorial Ownership

The two human owners retain final editorial control.

Version 1 must require human approval before any post is published.

No agent, model, scheduler, or external service may bypass this approval gate.

The engine may recommend, research, draft, render, and package content. It may not independently decide to publish political or current-affairs content.

---

## 3. Topic Eligibility

Topics may include:

- Union Budget and fiscal policy;
- public expenditure;
- infrastructure;
- economics;
- trade;
- foreign policy;
- geopolitics;
- Parliament;
- public institutions;
- major political claims;
- court decisions;
- public protests;
- regulatory decisions;
- official data releases;
- public controversies;
- policy implementation;
- under-covered institutional developments;
- historically relevant context connected to current events.

A topic should normally have at least one of:

- clear current relevance;
- meaningful public importance;
- a factual claim worth checking;
- useful explanatory value;
- a credible under-covered angle;
- evidence that materially changes common understanding.

---

## 4. Topic Discovery Is Not Publication Evidence

Trending feeds, X posts, creator videos, Reddit threads, search trends, headlines, and public chatter may help identify topics.

They do not automatically establish facts.

A selected topic must enter the research workflow before any publishable factual content is produced.

---

## 5. Trending and Under-Covered Balance

Each scheduled discovery scan should attempt to surface both:

### Trending
Subjects receiving substantial current attention.

### Under-covered
Subjects that appear materially important or informative but are receiving comparatively little mainstream attention.

The system should not assume that popularity equals importance.

The system should also not manufacture “under-covered” stories merely because few sources exist. Lack of coverage can also indicate weak evidence or low significance.

---

## 6. Political Claim Dissection

When a politician, party, institution, commentator, or viral account makes a factual claim, the system should identify the exact measurable proposition before evaluating it.

The workflow must not begin with:

> prove this person wrong

or:

> prove this person right.

It must begin with:

> what exactly is the claim, and what evidence would establish or contradict it?

Commentary may follow the factual result.

---

## 7. High-Risk Topic Classes

The following require enhanced review:

- elections and voting;
- protests with violence;
- communal or religious tensions;
- terrorism;
- armed conflict;
- military operations;
- border incidents;
- deaths or casualty claims;
- sexual violence;
- natural disasters;
- court rulings with major legal consequences;
- rapidly changing breaking news;
- allegations of criminal conduct;
- manipulated-media allegations;
- public-health emergencies.

For these topics:

- prefer primary sources and multiple credible confirmations;
- clearly timestamp rapidly changing information;
- label uncertainty;
- avoid humour that trivializes harm;
- require explicit human review of the final factual claims.

---

## 8. Serious-Event Humour Rule

The mascot and humour are optional.

For grave events involving suffering, the engine should automatically recommend a restrained presentation.

Avoid:

- popcorn reactions;
- celebratory expressions;
- “owned” language;
- jokes about victims;
- visual gags that trivialize casualties.

---

## 9. Corrections Policy

If a published factual claim is later found to be materially wrong:

1. preserve the original internal record;
2. identify why the failure occurred;
3. correct or remove the public content as appropriate;
4. record the correction in the project database;
5. update the relevant prompt, source rule, QA gate, or test if the failure exposed a systemic weakness.

Corrections are quality-control data, not something to hide from the internal system.

---

## 10. Uncertainty Policy

Allowed outputs include:

- confirmed;
- likely;
- unclear;
- disputed;
- insufficient evidence;
- still developing.

The engine must never convert uncertainty into confidence merely to make a cleaner post.

If the evidence is not good enough, the correct editorial decision may be:

**do not publish yet.**

---

## 11. Opinion and Commentary

Opinion is allowed as a clearly distinguishable layer.

It should not:

- invent supporting facts;
- misrepresent sources;
- fabricate direct quotes;
- omit a material caveat solely because it weakens the joke;
- present speculation as established fact.

Where useful, commentary may be visually marked as:

- `MONKE'S TAKE`;
- mascot speech bubble;
- `COMMENTARY`;
- another clearly distinct design treatment.

---

## 12. Satire

Satire may exaggerate tone or character reaction.

It may not fabricate a false event or quote in a way likely to be mistaken for genuine reporting.

If a satirical construction could reasonably be mistaken for a factual claim, it should be clearly signaled.

---

## 13. Political Identity and Factual Independence

The brand may have an openly right-leaning, pro-Modi editorial identity.

That identity does not change the evidence standard.

A claim favorable to the brand's viewpoint is not automatically true.

A claim unfavorable to the brand's viewpoint is not automatically false.

The factual pipeline must be capable of returning results that complicate or contradict the preferred narrative.

---

## 14. Source Transparency

Where practical, the post or caption should identify the primary source basis.

For complex posts, the engine should retain a full source list internally even if only the principal sources are displayed publicly.

A source note should not claim stronger support than the source actually provides.

---

## 15. Avoiding False Comparisons

The engine must not compare numbers that measure materially different things without explaining the difference.

Before rendering an A-vs-B comparison, verify:

- same or compatible metric;
- comparable time period;
- same unit;
- same geographic scope;
- same definition;
- no hidden denominator change.

If comparability is imperfect but still informative, disclose the limitation.

---

## 16. Breaking-News Speed Rule

Speed does not override verification.

For a developing story, it is acceptable to publish a smaller, clearly bounded update rather than a confident full explainer.

Example:

> “What is confirmed so far”

is preferable to a speculative definitive narrative.

---

## 17. Editorial Review Checklist

Before final approval, a human reviewer should be able to answer:

- What is the central factual claim?
- Which source supports it?
- What important caveat exists?
- Is the comparison fair?
- Is commentary visually distinguishable?
- Does the joke change the meaning?
- Is the mascot treatment appropriate for the seriousness of the topic?
- Would the post still be useful if the humour were removed?
- Is there any sentence we would be uncomfortable defending with the source open beside us?

If the last answer is yes, revise before publication.

---

## 18. Prohibited System Behaviour

The engine must not implement:

- demographic voter targeting;
- political microtargeting;
- inferred political-profile targeting;
- automated persuasion optimization;
- autonomous political publishing;
- manufactured grassroots personas;
- fabricated source material;
- fake quotations;
- fake screenshots presented as evidence.

---

## 19. Golden Rule

**The brand may have a viewpoint. The evidence pipeline may not have a predetermined verdict.**
