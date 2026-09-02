# 02_MASCOT_BIBLE.md

## Status

Version: 0.1  
Document type: Canonical  
Owner: Human project team  
Purpose: Define the permanent visual identity and behavioural rules of the Godi Monke mascot.

---

## 1. Mascot Role

The Godi Monke mascot is the recurring public character of the brand.

It functions as:

- narrator;
- reaction character;
- visual comedian;
- explainer;
- recurring brand signature;
- themed character inside different stories.

The mascot must never become a random monkey illustration that changes identity from post to post.

---

## 2. Canonical Source of Truth

The mascot must be defined by permanent image references stored in the repository.

Expected location:

`assets/mascot/master/`

The team's locked logo/profile-picture mascot is the primary visual reference.

The system must never rely on:

- chat history;
- model memory;
- a text-only description;
- “make the same monkey as last time”;

as the sole source of character identity.

Every automated custom mascot generation must receive the canonical visual reference images whenever the image model supports them.

---

## 3. Core Physical Identity

The mascot should preserve the following recognizable traits unless the human team explicitly changes the design:

- anthropomorphic ape/monkey character;
- pale/light facial fur or skin area contrasting with darker hair/fur;
- strong, angular face;
- distinctive spiky dark hair/fur silhouette;
- dark sunglasses;
- visible forehead tilak/mark;
- orange/saffron scarf;
- dark clothing base;
- confident posture;
- expressive eyebrows/face where visible;
- stylized comic/anime-poster aesthetic.

The exact reference image takes priority over any written description.

---

## 4. Default Emotional Identity

The mascot's default personality is:

- smug;
- observant;
- unimpressed;
- mildly mischievous;
- confident;
- meme-aware.

It should not default to rage.

Repeated aggressive expressions would make the character visually monotonous and reduce the humour.

---

## 5. Expression Set

The canonical expression library should eventually include at least:

1. neutral/confident;
2. smug;
3. suspicious;
4. confused;
5. shocked;
6. laughing;
7. facepalm;
8. disappointed;
9. serious;
10. curious;
11. “checking the numbers”;
12. “what am I looking at?”;
13. celebratory;
14. tired;
15. deadpan.

These should be generated and approved as a consistent reference set.

---

## 6. Pose Set

The canonical pose library should eventually include:

- pointing left;
- pointing right;
- presenting a board;
- sitting at a desk;
- holding a chart;
- using a calculator;
- reading a document;
- using binoculars;
- holding chai;
- holding popcorn;
- typing at a laptop;
- standing with arms folded;
- thinking;
- shrugging;
- looking at a map;
- examining something with a magnifying glass;
- looking over sunglasses;
- celebrating;
- facepalming.

Approved poses should be reusable without requiring a new image generation call.

---

## 7. Themed Roles

The mascot may change costume, props, or environment to fit the subject while preserving the same core character.

### Builder Monke
Use for:
- roads;
- railways;
- infrastructure;
- construction;
- logistics.

Possible props:
- hard hat;
- blueprint;
- road sign;
- measuring tape.

### Economist Monke
Use for:
- Union Budget;
- GDP;
- inflation;
- taxation;
- trade;
- fiscal policy.

Possible props:
- calculator;
- ledger;
- chart;
- glasses over sunglasses as an intentionally absurd gag.

### Detective Monke
Use for:
- fact checks;
- public claims;
- viral misinformation;
- conflicting numbers.

Possible props:
- magnifying glass;
- evidence board;
- folders;
- red string;
- source documents.

### Professor Monke
Use for:
- history;
- background;
- timelines;
- institutional explainers.

Possible props:
- chalkboard;
- pointer;
- old books;
- maps.

### Diplomat Monke
Use for:
- geopolitics;
- foreign policy;
- summits;
- strategic relations.

Possible props:
- world map;
- flags as contextual objects;
- briefing folder;
- chessboard.

### Lawyer Monke
Use for:
- court decisions;
- legal interpretation;
- constitutional issues.

Possible props:
- file bundle;
- legal book;
- courtroom board.

### Popcorn Monke
Use for:
- political drama;
- public arguments;
- contradictions;
- unfolding spectacle.

This is primarily a commentary asset and should not be used where the underlying event involves serious harm or tragedy.

### Chai Monke
Use for:
- short commentary;
- casual explainers;
- dry humour;
- “let us look at what actually happened” tone.

---

## 8. Prop Rules

Props are allowed to carry humour.

However:

- do not cover the character's defining features;
- do not replace the orange scarf permanently;
- avoid adding random political symbols simply because the post is political;
- do not make every prop contain text;
- do not rely on tiny AI-generated lettering inside props.

Recurring props may become part of the character library after human approval.

---

## 9. “Tears of Liberals” Mug

The mug from early visual experiments may exist as an occasional satire prop.

It is **not** the mascot's default object and must not appear in every post.

Overuse would:

- reduce novelty;
- make the page visually repetitive;
- shift attention away from information;
- make unrelated topics feel forced.

Use only when the editorial team deliberately chooses it.

---

## 10. BJP Lotus / Political Symbols

Political symbols may appear when contextually relevant or as part of established brand artwork.

For the canonical logo, the human team prefers the BJP lotus to be present but visually subtle rather than loudly foregrounded.

Possible treatment:

- partially obscured;
- distressed;
- shadowed;
- eerie;
- integrated into collage/background texture.

This treatment is a logo/art-direction choice and must not automatically be copied into every normal post.

---

## 11. Character Consistency Requirements

Custom mascot generations should preserve:

- facial structure;
- hair/fur silhouette;
- sunglasses shape;
- forehead mark;
- scarf identity;
- general body proportions;
- visual style family.

Small stylistic changes are acceptable if the character remains immediately recognizable.

A generation should be rejected if it looks like a different monkey character wearing similar accessories.

---

## 12. Character Sheet Plan

The mascot reference pack should eventually contain:

`master_logo.png`  
`master_character.png`  
`front.png`  
`three_quarter.png`  
`side.png`  
`full_body.png`  
`expression_sheet.png`  
`pose_sheet.png`  
`palette.json`  
`character_notes.md`

The team should approve this reference pack before heavily automating mascot generation.

---

## 13. Composition Rules

The mascot is usually a supporting element.

Normal information-heavy slides should generally allocate more visual priority to:

- headline;
- statistic;
- chart;
- comparison;
- timeline;
- evidence.

The mascot may become the dominant visual only when:

- the slide is primarily a hook;
- the humour is the intentional focus;
- the information content is deliberately minimal.

---

## 14. Carousel Behaviour

The mascot should not repeat the exact same pose across every slide.

Example:

**Slide 1:** shocked or suspicious Monke  
**Slide 2:** pointing-at-data Monke  
**Slide 3:** Professor/Detective Monke  
**Slide 4:** chai/smug takeaway Monke

This creates a small visual narrative.

---

## 15. Serious-Event Rule

For deaths, communal violence, armed conflict, disasters, sexual violence, or similarly grave topics:

- reduce or remove comedic mascot behaviour;
- avoid popcorn/reaction-meme treatment;
- use a restrained pose or omit the mascot;
- do not use suffering as the punchline.

The mascot is a brand tool, not a requirement on every slide.

---

## 16. Asset Reuse Strategy

Before paying for fresh image generation on every post, build a reusable approved mascot library.

Initial target:

- approximately 20 high-quality recurring poses/roles;
- transparent or easy-to-mask backgrounds where useful;
- consistent dimensions;
- metadata tags.

Example asset metadata:

- `role: detective`;
- `expression: suspicious`;
- `orientation: right`;
- `crop: waist-up`;
- `background: transparent`;
- `approved: true`.

The post planner should prefer an existing approved asset when it fits the story.

---

## 17. Custom Generation Rule

Generate a new mascot asset when:

- the topic needs a unique visual joke;
- no approved pose communicates the concept well;
- a themed environment materially improves the explanation.

Do not generate a custom mascot merely because generation is available.

---

## 18. Approval Rule

No newly generated mascot image becomes canonical automatically.

A human must approve it before it enters:

`assets/mascot/approved/`

Rejected or experimental images should remain outside the approved production library.

---

## 19. Golden Rule

**The audience should recognize Godi Monke from the character before they read the account name.**
