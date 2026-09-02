# 07_CONTENT_FORMATS.md

## Status

Version: 0.1  
Document type: Canonical  
Owner: Human project team  
Purpose: Define the initial post formats, information hierarchy, and rules for choosing between single-page and carousel content.

---

## 1. Format Principle

The format should follow the information.

Do not force a topic into a carousel merely because carousels exist.

Do not compress a complex topic into one slide if doing so removes material context.

The content planner should ask:

> What is the minimum number of slides needed to explain this accurately and clearly?

---

## 2. Initial Production Formats

Version 1 should begin with only three primary formats:

1. `GM-SINGLE-01` — single-page explainer;
2. `GM-COMPARE-01` — comparison/data post;
3. `GM-CAROUSEL-01` — multi-page explainer.

Additional templates should not be added until these are stable.

---

## 3. GM-SINGLE-01 — Single-Page Explainer

### Use when

- one central fact drives the story;
- context can fit in a short explanation;
- no important chronology is required;
- there are at most a few supporting facts.

### Preferred structure

**Top**
- small Godi Monke identifier;
- optional category label.

**Primary**
- short hook/headline.

**Evidence**
- main number, quote fragment, or factual statement.

**Context**
- 1–3 short supporting lines.

**Meaning**
- one concise “why it matters” line.

**Mascot**
- one relevant pose/reaction;
- usually secondary to the information.

**Source**
- concise source line.

### Humour

Default maximum:
- one strong joke/reaction.

---

## 4. GM-COMPARE-01 — Comparison Post

### Use when

The central information is meaningfully expressed as:

- before vs after;
- claim vs evidence;
- two time periods;
- two policies;
- two comparable metrics.

### Requirements

The comparison must pass comparability QA.

### Preferred structure

**Headline**
What is being compared?

**A**
Label + value + period.

**B**
Label + value + period.

**Derived result**
Difference, percentage change, or explanatory note.

**Context**
What the numbers do and do not mean.

**Mascot**
Often placed between or beside the comparison.

**Source**
Underlying source(s).

### Warning

The design must not imply direct comparability when definitions differ.

---

## 5. GM-CAROUSEL-01 — Multi-Page Explainer

### Use when

The topic requires:

- chronology;
- multiple claims;
- contextual explanation;
- evidence plus caveat;
- policy mechanics;
- geopolitical background;
- claim dissection.

### Default slide count

Prefer **3–5 slides**.

More slides are allowed when the subject genuinely requires them.

Avoid filler slides.

---

## 6. Recommended Carousel Narrative

### Slide 1 — Hook

Goal:
Make the question or development immediately clear.

Possible structures:

- `WHAT JUST HAPPENED?`
- `THE CLAIM EVERYONE IS ARGUING ABOUT`
- `THIS NUMBER NEEDS CONTEXT`
- `INDIA–X: WHAT CHANGED?`

The slide may use a stronger mascot visual than later slides.

Do not front-load every detail.

---

### Slide 2 — Evidence

Goal:
Show the strongest factual material.

Possible elements:

- key number;
- comparison;
- short chart;
- quote with attribution;
- official document excerpt represented cleanly;
- timeline start.

Mascot role:
pointing, calculator, detective, builder, etc.

---

### Slide 3 — Context

Goal:
Explain what the raw number or headline misses.

Possible elements:

- denominator;
- historical comparison;
- policy definition;
- second source;
- caveat;
- timeline continuation;
- causal limitation.

Mascot role:
Professor, Detective, or Map Monke.

---

### Slide 4 — Meaning

Goal:
Explain why the development matters.

This should distinguish:

- established implication;
- plausible interpretation;
- editorial commentary.

Mascot role:
smug/chai/serious depending on topic.

---

### Slide 5 — Optional Source / Nuance

Use only where needed.

Possible content:

- detailed sources;
- methodology note;
- unresolved issue;
- “what happens next.”

Do not create a source-only slide if source notes can remain readable elsewhere.

---

## 7. Fact-Check Variant

The first template family may support a structured variant without creating a separate design system.

Possible sequence:

**Slide 1:** exact claim  
**Slide 2:** what the source says  
**Slide 3:** missing context / counter-evidence  
**Slide 4:** verdict + concise explanation

Verdict must come from verified claim data, not the creative copywriter.

---

## 8. Geopolitics Variant

Possible sequence:

**Slide 1:** development  
**Slide 2:** map / actors  
**Slide 3:** India's interest  
**Slide 4:** strategic context  
**Slide 5:** what remains uncertain

Maps must not visually invent disputed territorial facts.

---

## 9. Budget / Economics Variant

Possible sequence:

**Slide 1:** headline  
**Slide 2:** key allocation/indicator  
**Slide 3:** comparison with prior period  
**Slide 4:** what the number actually means  
**Slide 5:** caveat or practical effect

Budget estimate, revised estimate, and actual expenditure must remain distinct.

---

## 10. Information Density

A slide should not become a miniature article.

Prefer:

- one main idea;
- one primary visual;
- a few supporting lines;
- one source note.

If body copy becomes too dense, either:

- simplify;
- move context to another slide;
- use the caption;
- reconsider whether the format is appropriate.

---

## 11. Text Hierarchy

Each template should reserve deterministic typography levels:

- `H1` — hook/headline;
- `H2` — slide subhead;
- `STAT` — primary number;
- `BODY` — short explanation;
- `LABEL` — chart/category label;
- `MONKE_BUBBLE` — humour/commentary;
- `SOURCE` — citation/source note;
- `BRAND` — small account identifier;
- `SLIDE_NO` — slide index.

These roles should later map to concrete CSS/SVG styles.

---

## 12. Mascot Placement

The mascot should not obstruct:

- numbers;
- charts;
- labels;
- citations;
- essential text.

The renderer should support predefined mascot zones.

Example:

- right-lower;
- left-lower;
- side-third;
- header cameo;
- full-slide hook.

---

## 13. Deterministic Rendering Rule

All important text should enter the renderer as structured fields.

Example:

```json
{
  "template": "GM-SINGLE-01",
  "headline": "Example headline",
  "primary_stat": {
    "value": "18%",
    "claim_id": "CLAIM-004"
  },
  "body": [
    "Short explanation."
  ],
  "commentary": "Monke reaction.",
  "source_ids": ["SOURCE-002"],
  "mascot_asset_id": "MASCOT-DETECTIVE-03"
}
```

The renderer must not ask an image model to typeset these values.

---

## 14. Source Presentation

Source text must remain readable.

Possible treatments:

- footer line;
- compact source chip;
- final-slide source block;
- caption support.

Do not reduce source text to decorative illegibility.

---

## 15. Platform Adaptation

The same structured post should be reusable for Instagram and X where practical.

The renderer may later support:

- Instagram square/portrait;
- X image dimensions;
- alternate crops.

Core factual content should remain the same.

---

## 16. Caption Relationship

The image should carry the core information.

The caption may add:

- additional context;
- full source list;
- methodological note;
- restrained commentary.

Do not make the audience depend on the caption to understand the central claim.

---

## 17. Template Versioning

Every rendered post should record:

- template ID;
- template version;
- rendering timestamp.

Example:

`GM-CAROUSEL-01@1.2`

Template changes must not silently alter historical posts.

---

## 18. Quality Questions

Before approving a format:

- Is one page enough?
- Is any slide filler?
- Does each slide have one main job?
- Is the main fact readable immediately?
- Does the mascot support rather than dominate?
- Are source notes readable?
- Are commentary and fact visually distinct?
- Would a reader understand the post without the caption?

---

## 19. Golden Rule

**Use the fewest slides that preserve the truth and make the story easy to understand.**
