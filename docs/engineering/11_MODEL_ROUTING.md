# 11_MODEL_ROUTING.md



## Status



Version: 0.1

Document type: Engineering specification

Owner: Human project team

Market baseline checked: 2026-09-02

Depends on: `08_SYSTEM_ARCHITECTURE.md`, `13_COST_POLICY.md`

Purpose: Define which model/provider is used for each task, why it is used, how fallbacks work, and how model changes are controlled.



---



## 1. Routing Principle



Godi Monke Engine must not depend on one model doing everything.



Models are assigned narrow jobs according to:



- factual reliability;

- tool/search capability;

- cost;

- structured-output reliability;

- multimodal capability;

- provider independence;

- consistency.



Model IDs and prices are configuration, not hard-coded business logic.



The routing table may change over time without changing the workflow state machine.



---



## 2. Current Production Baseline



The initial recommended providers are:



### Google Gemini API



Primary uses:



- current-topic discovery;

- Google Search grounding;

- research synthesis;

- low-cost extraction/classification;

- mascot image generation.



### OpenAI API



Primary uses:



- independent claim verification;

- high-quality post copy from already verified facts;

- optional low-cost structured QA.



### ChatGPT Plus



Human-operated editorial support only.



ChatGPT Plus is not an API entitlement and must not be treated as one by the runtime.



The team may manually use ChatGPT for:



- difficult editorial review;

- difficult high-risk research review;

- mascot/art experiments;

- architecture and prompt review.



---



## 3. Current Model Facts



The following market facts were checked against official provider documentation on 2026-09-02.



### Gemini 3.7 Flash



Model ID:



`gemini-3.7-flash`



Current status:



- stable / generally available;

- supports Search grounding;

- supports structured outputs;

- supports URL context and multimodal inputs;

- approximately 1M input context;

- configurable thinking levels.



Promotional API price through 2026-12-31:



- $0.75 / 1M input tokens;

- $3.75 / 1M output tokens.



The price is scheduled to increase after the promotional period, so the pricing catalog must not assume this rate permanently.



### Gemini 3.5 Flash-Lite



Model ID:



`gemini-3.5-flash-lite`



Current role:



- low-cost classification;

- normalization;

- simple extraction;

- high-volume routine transformations.



Price checked 2026-09-02:



- $0.30 / 1M input tokens;

- $2.50 / 1M output tokens.



### Google Search Grounding



Gemini 3.x paid-tier projects currently include:



- 5,000 free Search-grounding requests per month, shared across Gemini 3.x models;

- additional usage is billed after that threshold.



One model prompt may create multiple underlying search queries.



The engine must therefore track Search-grounding query usage, not merely count model prompts.



### GPT-5.6 Terra



Model ID:



`gpt-5.6-terra`



Current role:



- independent claim verification;

- high-quality structured editorial drafting where justified.



Price checked 2026-09-02:



- $2.00 / 1M input tokens;

- $12.00 / 1M output tokens.



### GPT-5.6 Luna



Model ID:



`gpt-5.6-luna`



Current role:



- optional inexpensive structured QA;

- lightweight formatting/classification where using a second provider is useful.



Price checked 2026-09-02:



- $0.20 / 1M input tokens;

- $1.20 / 1M output tokens.



### Gemini 3.1 Flash Image / Nano Banana 2



Model ID:



`gemini-3.1-flash-image`



Current role:



- primary automated Godi Monke mascot generation/editing.



Important capability:



- supports multiple reference images;

- official documentation supports character-consistency workflows using reference characters;

- suitable for preserving a recurring mascot more reliably than text-only prompting.



Price checked 2026-09-02:



- approximately $0.067 for a 1K image on Standard processing;

- resolution-dependent.



---



## 4. Initial Routing Table



| Workflow stage | Primary | Thinking / mode | Fallback | Notes |

|---|---|---|---|---|

| Discovery: trending | Gemini 3.7 Flash + Search grounding | low/medium | Gemini 3.6 Flash + grounding | Search is required for freshness |

| Discovery: under-covered | Gemini 3.7 Flash + Search grounding | medium | Gemini 3.6 Flash + grounding | Must return evidence signals, not invented topics |

| Topic normalization/dedupe helper | Local Python first | deterministic | Gemini 3.5 Flash-Lite | Model only when semantic judgment is needed |

| Source discovery for selected topic | Gemini 3.7 Flash + Search grounding | medium | Gemini 3.6 Flash + grounding | Finds candidate primary/context/counter sources; URLs are then retrieved directly |

| Source classification | Local rules first | deterministic | Gemini 3.5 Flash-Lite | Tier is later reviewable |

| Source text extraction | Local parser first | deterministic | Gemini 3.5 Flash-Lite | Do not pay a model to parse simple HTML/text |

| Research synthesis | Gemini 3.7 Flash | medium | Gemini 3.6 Flash | Uses retrieved evidence package |

| Claim extraction | Gemini 3.7 Flash | medium | Gemini 3.5 Flash-Lite for simple cases | Structured output required |

| Derived arithmetic | Python | deterministic | none | Never delegate authoritative arithmetic to an LLM |

| Claim verification | GPT-5.6 Terra | medium/high based on risk | human review | Do not silently fall back to the same research model/provider |

| Low-risk structure QA | Local rules first | deterministic | GPT-5.6 Luna | Optional |

| Post format planning | Local rules + Gemini 3.7 Flash | low | GPT-5.6 Luna | Must use accepted research packet |

| Informational copy draft | GPT-5.6 Terra | low/medium | Gemini 3.7 Flash | Facts are locked; no engagement-optimization objective |

| Humour alternatives | GPT-5.6 Terra or Gemini 3.7 Flash | low | human | Commentary only; cannot alter facts |

| Mascot asset selection | Local asset index | deterministic | none | Reuse preferred |

| Mascot generation/edit | Gemini 3.1 Flash Image | standard | manual ChatGPT image workflow | No silent automatic provider substitution initially |

| Final deterministic render | HTML/CSS/Playwright | deterministic | none | AI does not typeset factual infographic text |

| Final factual QA | Local claim-lock checks + human | deterministic | GPT-5.6 Luna/Terra as supplementary | Model QA never replaces human final gate |



---



## 5. Discovery Routing



Discovery is freshness-sensitive.



Therefore, the discovery provider must have live Search grounding enabled.



The model should return structured candidate objects containing:



- candidate title;

- short description;

- why it is current;

- trending or under-covered classification;

- initial supporting URLs/citations;

- event time where known;

- confidence;

- suggested risk class.



The model output itself is not a source.



Search-grounding citations are used to identify candidate sources for retrieval.



---



## 6. Search-Grounding Usage Limits



The application should enforce configurable limits.



Initial policy:



- monthly soft warning: 3,500 Google Search-grounding requests;

- monthly automatic-stop threshold: 4,500 requests;

- provider-advertised free allowance currently: 5,000 requests/month.



This preserves a safety margin because:



- one prompt can issue multiple queries;

- billing behavior can change;

- other Gemini stages may use grounding;

- usage metadata may arrive after execution.



After the automatic-stop threshold:



- do not automatically incur paid overage;

- alert the humans;

- allow a deliberate temporary override.



---



## 7. Research Routing



Research should use a two-step approach:



### Retrieval



Use actual source retrieval wherever possible.



Do not ask the model to “remember” current facts.



### Synthesis



Gemini 3.7 Flash receives:



- retrieved source material;

- source metadata;

- topic question;

- canonical research instructions.



It returns a structured research packet.



It must preserve:



- contradictory evidence;

- uncertainty;

- missing evidence;

- source IDs.



---



## 8. Independent Verification Routing



Claim verification deliberately uses OpenAI rather than the same Gemini research model.



Reason:



- provider independence reduces correlated model failure;

- the verifier can evaluate claim/evidence support without the original creative framing.



GPT-5.6 Terra should receive only what it needs:



- atomic claim;

- evidence excerpts;

- source metadata;

- relevant definitions/caveats.



Where possible, omit:



- intended joke;

- desired headline;

- preferred political conclusion.



If Terra is unavailable or budget-blocked:



- do not silently substitute the Gemini researcher;

- mark verification blocked;

- route to human review or wait.



---



## 9. Copy Routing



Copy generation happens only after facts are locked.



The model receives:



- accepted research packet;

- approved claim IDs;

- format specification;

- brand voice rules;

- exact values to display;

- explicit instruction that facts are immutable.



The copy stage may:



- simplify;

- order;

- explain;

- propose commentary;

- propose humour.



It may not:



- create a new factual statistic;

- create a new factual date;

- invent a quote;

- silently strengthen an uncertain verdict.



New factual-looking assertions detected by QA are rejected unless they are added through the research/claim workflow.



---



## 10. Humour Routing



Humour is not a separate research stage.



The humour request receives a clean factual payload and produces commentary-only alternatives.



The objective is:



- clarity;

- natural Godi Monke voice;

- occasional Hinglish;

- memorable personality.



The objective must not be framed as:



- persuading a demographic;

- optimizing voter belief change;

- political microtargeting;

- maximizing outrage.



Humour outputs are optional and human-reviewable.



---



## 11. Image Routing



### Primary



`gemini-3.1-flash-image`



Use canonical mascot reference images.



Prefer:



- 1K production assets initially;

- simple or transparent/easy-to-mask backgrounds;

- no important factual text inside the generated image;

- one clearly described pose/scene per request.



### Reuse Before Generate



Before any image call:



1. search approved mascot asset metadata;

2. use an existing asset if it fits;

3. generate only when a custom scene adds value.



### New Asset Approval



A new custom mascot image is not automatically approved for reuse.



It must pass human review before being promoted to the approved asset library.



---



## 12. Manual ChatGPT Fallback



The team already pays for ChatGPT Plus.



For unusual mascot art or difficult editorial review, a human may manually use ChatGPT.



This is not part of the automated runtime.



The runtime records such assets/reviews as human-provided inputs.



No software should attempt to automate the ChatGPT consumer interface.



---



## 13. Model Version Control



Model aliases can change behavior over time.



Therefore:



- every model call records the exact requested model ID;

- record provider-returned version metadata when available;

- prompts are versioned;

- Golden Set tests are run before intentional model migrations;

- routing changes are committed to Git;

- major provider/model changes require human approval.



If a provider offers a pinned snapshot for a model used in production, prefer the snapshot when stability materially outweighs access to automatic improvements.



---



## 14. Fallback Rules



Fallbacks must be explicit.



### Allowed automatic fallback examples



- discovery: Gemini 3.7 Flash → Gemini 3.6 Flash;

- low-risk formatting helper: local → Luna.



### Not allowed automatically



- independent verifier → same model that created the research conclusion;

- image generator → arbitrary second provider producing a materially different character;

- budget-blocked expensive model → unverified cheaper model with weaker quality;

- source retrieval failure → model memory.



Every fallback must be logged.



---



## 15. Provider Outage Behavior



If discovery is unavailable:



- skip/mark the scan failed;

- alert humans;

- allow manual retry.



If research is unavailable:



- preserve selected topic;

- do not fabricate packet.



If independent verification is unavailable:



- block claims that require it.



If image generation is unavailable:



- use an approved existing mascot asset or wait/manual-create.



The system should degrade by doing less, not by inventing more.



---



## 16. Prompt Versioning



Each model stage must load its prompt from the repository.



Prompts must have:



- stable filename;

- explicit version in metadata/header;

- hash recorded in `ModelRun`.



Do not hide large production prompts in Python strings.



Prompt changes affecting factual behavior require regression review.



---



## 17. Evaluation Before Model Change



Before replacing a model:



1. run representative Golden Set cases;

2. compare schema-validity rate;

3. compare factual support;

4. compare cost;

5. compare latency;

6. compare brand-quality output where relevant;

7. inspect failure modes;

8. record decision.



Do not migrate solely because a newer model name exists.



---



## 18. Market-Change Review



Review `11_MODEL_ROUTING.md` and the pricing catalog:



- at least monthly during early operation;

- immediately after a provider announces a model retirement;

- before January 2027 because Gemini 3.7/3.6 Flash promotional pricing is scheduled to change;

- whenever monthly cost deviates materially from expectations.



---



## 19. Official References Used for v0.1



Checked 2026-09-02:



- OpenAI API Platform pricing and GPT-5.6 model documentation;

- Google Gemini API model overview;

- Google Gemini 3.7 Flash documentation;

- Google Gemini Developer API pricing;

- Google Gemini Search grounding documentation;

- Google Gemini image-generation documentation.



Pricing is operational metadata, not a permanent canonical truth. The runtime pricing catalog must be configurable.



---



## 20. Golden Rule



**Use cheap models for repetition, strong independent models for consequential verification, deterministic code for facts, and humans for final judgement.**
