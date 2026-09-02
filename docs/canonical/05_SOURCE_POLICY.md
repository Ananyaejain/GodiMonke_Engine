# 05_SOURCE_POLICY.md

## Status

Version: 0.1  
Document type: Canonical  
Owner: Human project team  
Purpose: Define how sources are discovered, ranked, stored, cited, and used as evidence.

---

## 1. Source Principle

Not all sources serve the same purpose.

The system must distinguish between:

- discovery sources;
- primary evidence;
- secondary reporting;
- analysis/context;
- social signals;
- unsupported commentary.

A source useful for discovering a story may be unacceptable as evidence for a factual claim.

---

## 2. Source Tiers

### Tier A — Primary / Authoritative Evidence

Preferred whenever directly relevant.

Examples include:

- Union Budget documents;
- Ministry publications;
- PIB releases when reporting official government positions or data;
- RBI publications;
- CAG reports;
- Parliament questions, answers, bills, committee reports, and debates where relevant;
- Supreme Court and High Court judgments/orders;
- Election Commission materials;
- official statistical agencies;
- MEA statements;
- official foreign-government documents for their own actions;
- UN, World Bank, IMF, WTO, and similar institutional datasets/reports;
- company filings for company-specific financial claims;
- original speeches, transcripts, press conferences, or verified statements;
- official datasets and dashboards.

A Tier A source can still be incomplete, self-interested, provisional, or later revised. “Official” does not mean “infallible.”

---

### Tier B — High-Quality Independent Reporting

Use for:

- corroboration;
- chronology;
- interviews;
- local reporting;
- context;
- developments not yet documented in primary material.

The engine should prefer outlets with:

- transparent attribution;
- corrections policies;
- named reporters/editors;
- direct source links where possible;
- a record of original reporting.

For disputed political claims, do not rely on one outlet when independent corroboration is reasonably available.

---

### Tier C — Specialist / Research Context

Examples:

- academic papers;
- think tanks;
- policy institutes;
- sector research;
- domain experts;
- technical reports.

Useful for interpretation and background.

Check:

- publication date;
- methodology;
- author/institution;
- funding or conflicts where material;
- whether the analysis is being cited outside its intended scope.

---

### Tier D — Discovery / Social Signals

Examples:

- X posts;
- Reddit;
- YouTube;
- Instagram;
- political creators;
- viral screenshots;
- trending lists;
- community discussions.

Use primarily to answer:

> What are people discussing?

Do not automatically use these as proof that the underlying factual claim is true.

An original post by the person or institution making a claim may be primary evidence of **what they said**, but not necessarily evidence that the claim itself is correct.

---

### Tier E — Weak / Unverified

Examples:

- anonymous screenshots;
- unattributed graphics;
- repost chains with no original source;
- SEO aggregation pages;
- AI-generated summaries with no evidence trail;
- edited clips without provenance;
- “forwarded as received” material.

These should not support publishable factual claims.

They may trigger a research task to locate the original source.

---

## 3. Primary-Source Preference

When a claim concerns a number produced by an institution, prefer the institution's underlying document or dataset over a news article summarizing it.

Example:

For Union Budget allocation numbers:

**prefer:** Budget documents / Ministry of Finance  
**then use:** news reporting for explanation or reactions

This reduces citation drift and transcription errors.

---

## 4. Source Diversity

For significant contested claims, the research packet should attempt to include:

- original statement or primary source;
- authoritative data/document;
- credible secondary reporting;
- contrary or qualifying evidence where available.

The goal is not artificial “both-sides” symmetry.

The goal is to avoid evaluating a disputed claim using only evidence selected from one narrative.

---

## 5. Source Freshness

The system must record:

- publication date;
- retrieval date/time;
- revision date where visible.

For fast-moving stories, old background sources must not be mistaken for current-state evidence.

For stable historical facts, older authoritative sources may be appropriate.

---

## 6. Direct Evidence Capture

When feasible, store:

- source title;
- publisher/author;
- URL;
- publication date;
- retrieval timestamp;
- relevant excerpt;
- page/table/section identifier;
- source tier;
- source type;
- content hash or archive metadata where practical.

The excerpt should be limited to the portion needed to support the claim.

---

## 7. PDF / Report Rules

For long reports:

- record page number where possible;
- record table/figure number where applicable;
- distinguish report publication date from underlying data period;
- do not infer a value from a chart if the exact table exists;
- check footnotes and methodology before using comparisons.

---

## 8. Public Statement Rules

If a politician or public figure makes a statement:

Store the original source when possible:

- official video;
- transcript;
- verified account;
- press release;
- parliamentary record;
- full interview.

Avoid evaluating a clipped quote without checking surrounding context when context could materially change its meaning.

---

## 9. Screenshot Rule

A screenshot is not a sufficient source merely because it looks official.

The engine should attempt to locate the underlying webpage, document, post, dataset, or video.

If provenance cannot be established, treat the screenshot as unverified.

---

## 10. Secondary Reporting Conflicts

If credible outlets disagree:

- do not silently choose the preferred number;
- identify the disagreement;
- inspect whether they are using different definitions or update times;
- locate primary evidence if possible;
- preserve uncertainty if conflict remains unresolved.

---

## 11. Government Source Caveat

Official government material is authoritative evidence of:

- what the government states;
- official allocations;
- official administrative data;
- official policy;
- official methodology.

It may not independently establish:

- political interpretation;
- causal success claims;
- contested estimates outside the underlying methodology.

Where the claim goes beyond the official document, additional evidence may be required.

---

## 12. Social Discovery Strategy

The discovery system may monitor high-signal social content to identify:

- viral political claims;
- emerging controversies;
- new speeches;
- questions people are asking;
- topics accelerating faster than traditional reporting.

The research system must then move outward to stronger evidence.

---

## 13. Source Quality Score

The software may assign an internal quality score, but it must not treat the score as absolute truth.

Possible factors:

- primary vs secondary;
- original vs copied;
- direct relevance;
- recency;
- transparency;
- methodology;
- independence;
- corroboration.

The score should assist review, not replace judgement.

---

## 14. Citation-to-Claim Mapping

Every publishable factual claim should reference one or more source IDs.

Example:

`CLAIM-004 -> SOURCE-002, SOURCE-005`

A post should never contain a factual statement that exists only in free-form creative copy and has no corresponding claim record.

---

## 15. Source Display

Public-facing source display may use a concise form:

> Source: Ministry of Finance, Union Budget 2026–27

Internal records should retain the complete source details.

For carousels, detailed source lists may appear on the final slide, in the caption, or in a linked source note depending on readability.

---

## 16. Source Failure Rule

If the system cannot retrieve or verify the underlying evidence:

- mark the source unavailable;
- do not silently substitute an unrelated summary;
- flag the claim for review;
- downgrade confidence;
- reject publication when the missing source is essential.

---

## 17. Golden Rule

**Use social media to discover the question. Use evidence to answer it.**
