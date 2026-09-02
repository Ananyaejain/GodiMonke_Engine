# 13_COST_POLICY.md



## Status



Version: 0.1

Document type: Engineering specification

Owner: Human project team

Market baseline checked: 2026-09-02

Purpose: Keep Godi Monke Engine inside the team's ₹5,000/month total operating budget while preserving quality.



---



## 1. Total Budget



Approximate monthly ceiling:



**₹5,000**



Current planning envelope:



| Category | Monthly planning amount |

|---|---:|

| ChatGPT Plus | ₹2,000 |

| X subscription | ₹500 |

| VPS reserve | ₹400 |

| Automated API budget | ₹1,600 |

| Contingency / tax / FX / unexpected usage | ₹500 |

| **Total** | **₹5,000** |



During local development, the VPS reserve may remain unspent.



It must not be automatically reallocated by software.



Budget changes require a human configuration change.



---



## 2. API Budget Allocation



Initial API caps:



| Provider/category | Monthly hard planning cap |

|---|---:|

| Google Gemini / image / grounding-related model usage | ₹900 |

| OpenAI API | ₹600 |

| Miscellaneous provider/tool allowance | ₹100 |

| **Automated API envelope** | **₹1,600** |



These are safety ceilings, not spending targets.



The expected objective is to remain materially below them.



---



## 3. Cost Accounting Principle



Every paid external call must create a usage record.



The system must record, where available:



- provider;

- model;

- token usage;

- search-grounding query count;

- image count/resolution;

- provider-reported usage;

- estimated USD cost;

- configured FX rate;

- estimated INR cost;

- workflow stage;

- timestamp.



Cost cannot be reconstructed only from end-of-month card statements.



---



## 4. Pricing Catalog



Provider pricing changes.



Therefore, runtime code must not scatter prices across application logic.



Use one versioned pricing catalog/configuration object.



Each price entry should include:



- provider;

- model/tool;

- unit;

- rate;

- currency;

- effective date;

- last-verified date;

- reference note.



When provider pricing changes, update the catalog rather than business logic.



---



## 5. Currency Conversion



Provider pricing is commonly denominated in USD.



Use a configurable USD→INR conversion rate for estimates.



Do not hard-code a permanent exchange rate.



To avoid underestimating spend, the estimator may apply a configurable FX/tax safety multiplier.



Card/network taxes and provider billing details may differ from token estimates, so the ₹500 global contingency remains outside the automated API envelope.



---



## 6. Budget Enforcement Levels



### Normal



Usage < 70% of API envelope.



Operate normally.



### Warning



Usage ≥ 70%.



- notify humans;

- include forecast;

- prefer cheaper approved routes where quality impact is negligible.



### Restricted



Usage ≥ 85%.



- disable nonessential experimental generation;

- strongly prefer asset reuse;

- reduce optional model QA;

- do not reduce mandatory factual verification.



### Hard Stop



Usage ≥ 100% of configured automated API envelope.



Block new paid calls unless a human explicitly changes/overrides the budget.



Already stored work remains accessible.



Do not silently use an unapproved weaker model simply to continue.



---



## 7. Per-Call Guard



Before each paid call:



1. estimate worst-reasonable cost where possible;

2. check provider cap;

3. check global API cap;

4. check stage/usage limits;

5. proceed or block.



A single call with estimated cost above a configurable threshold should require explicit approval.



Initial suggested per-call manual-approval threshold:



**₹50 estimated cost**



This value is configurable.



---



## 8. Search-Grounding Budget



Google currently advertises 5,000 free Gemini 3.x Search-grounding requests per month on the paid tier before overage.



Internal policy:



- soft warning at 3,500;

- automatic stop at 4,500;

- no automatic paid overage.



The engine must track the underlying grounding search count reported by the provider.



If provider metadata cannot reliably identify usage:



- use a conservative estimate;

- warn humans earlier.



---



## 9. Discovery Cost Control



Discovery runs three times daily.



Cost controls:



- do not deeply research all ten candidates;

- use grounded discovery only to generate/justify candidates;

- normalize/dedupe locally where possible;

- research primarily after human selection;

- cache retrieved source metadata;

- do not repeatedly search the same topic inside one scan unless needed.



This is a major budget-saving design.



---



## 10. Research Cost Control



For selected topics:



- retrieve source documents directly;

- parse straightforward text locally;

- send only relevant evidence to models;

- avoid repeatedly resending entire long documents;

- use hashes/caching;

- stop research when evidence is sufficient for the selected format.



Do not equate “more tokens” with “better research.”



---



## 11. Verification Cost Control



Independent verification is quality-critical.



Do not remove it merely to save money.



Instead:



- verify atomic claims;

- send focused excerpts;

- avoid full duplicated research packets where unnecessary;

- verify only claims actually intended for use or needed to establish the verdict.



High-risk claims may justify more expensive reasoning.



---



## 12. Copy Cost Control



Copy generation occurs only for selected, researched topics.



Limit:



- number of full rewrites;

- number of humour alternatives;

- automatic regeneration loops.



Humans can directly edit text rather than paying for repeated model attempts.



---



## 13. Image Cost Control



Primary principles:



1. approved asset reuse first;

2. custom generation only when useful;

3. default to 1K assets initially;

4. generate a small number of candidates;

5. do not generate entire final infographics through an image model.



Initial operational limits:



- soft warning after 80 custom mascot/image generations in a month;

- hard automatic stop after 120 unless humans override.



These limits may be lowered after real usage data exists.



---



## 14. Current Price Baseline



Checked 2026-09-02:



### Gemini 3.7 Flash

Promotional through 2026-12-31:

- $0.75 / 1M input tokens

- $3.75 / 1M output tokens



### Gemini 3.5 Flash-Lite

- $0.30 / 1M input tokens

- $2.50 / 1M output tokens



### GPT-5.6 Terra

- $2.00 / 1M input tokens

- $12.00 / 1M output tokens



### GPT-5.6 Luna

- $0.20 / 1M input tokens

- $1.20 / 1M output tokens



### Gemini 3.1 Flash Image

- approximately $0.067 / 1K image on Standard processing



These values are references for the initial catalog, not permanent constants.



---



## 15. Provider Cap Behavior



If Google cap is reached:



- stop Google paid calls;

- discovery may pause;

- existing research remains accessible;

- do not automatically move all work to OpenAI.



If OpenAI cap is reached:



- do not silently remove independent verification;

- block affected verification or route to human review;

- optionally pause new draft generation.



Provider caps protect the overall budget and prevent outage/failure loops from becoming billing incidents.



---



## 16. Retry and Billing



Retries can multiply cost.



Every external retry must:



- increment attempt count;

- retain same workflow operation ID;

- be included in cost records.



Do not retry non-transient failures indefinitely.



Budget checking happens again before each retry.



---



## 17. Cache Policy



Use caching only when it reduces cost without creating stale factual output.



Safe examples:



- canonical brand prompt content;

- static source parsing;

- stable source documents;

- approved mascot assets.



Unsafe example:



- caching “latest” current-affairs results beyond an appropriate freshness window.



Cache metadata should include creation/freshness information.



---



## 18. Monthly Cost Report



The Telegram/admin interface should eventually provide:



- total API spend estimate;

- spend by provider;

- spend by workflow stage;

- search-grounding usage;

- image generations;

- average cost per completed post;

- failed/retry cost;

- remaining budget.



This is more useful than a single provider bill.



---



## 19. Quality Protection Rule



The system must not trade away mandatory evidence or human approval to stay under budget.



When the budget cannot support a safe post:



**publish less.**



Do not degrade factual standards.



---



## 20. Golden Rule



**The budget controls how much work the system performs, not whether the system tells the truth.**
