# 10_WORKFLOW_STATE_MACHINE.md

## Status

Version: 0.1  
Document type: Engineering specification  
Owner: Human project team  
Depends on: `08_SYSTEM_ARCHITECTURE.md`, `09_DATA_MODEL.md`  
Purpose: Define legal workflow states, transitions, human gates, failure behavior, and retry rules.

---

## 1. State Machine Principle

Python owns state.

A model may recommend an action, but only application code may execute a transition after:

- validating the current state;
- validating required data;
- checking human approval where required;
- checking risk rules;
- appending an audit event.

Illegal transitions must fail loudly.

---

## 2. Why State Is Split by Entity

Do not create one giant string that attempts to describe the entire project state.

Version 1 uses coordinated state machines for:

- discovery runs;
- topics;
- research packets;
- claims;
- posts;
- model runs.

This keeps failures and retries local.

---

## 3. DiscoveryRun States

```text
CREATED
  ↓
RUNNING
  ├──→ COMPLETED
  └──→ FAILED
```

Allowed transitions:

- `CREATED -> RUNNING`
- `RUNNING -> COMPLETED`
- `RUNNING -> FAILED`
- `FAILED -> RUNNING` only through an explicit retry operation

A scheduled trigger must not start a second `RUNNING` scan for the same configured scan window.

---

## 4. Topic States

Initial `TopicStatus` values:

- `DISCOVERED`
- `SAVED`
- `SELECTED`
- `RESEARCHING`
- `RESEARCHED`
- `REJECTED`
- `ARCHIVED`

Core transitions:

```text
DISCOVERED
  ├──→ SAVED
  ├──→ SELECTED
  ├──→ REJECTED
  └──→ ARCHIVED

SAVED
  ├──→ SELECTED
  ├──→ REJECTED
  └──→ ARCHIVED

SELECTED
  ├──→ RESEARCHING
  ├──→ REJECTED
  └──→ ARCHIVED

RESEARCHING
  ├──→ RESEARCHED
  └──→ SELECTED      (research failed / safe rollback)

RESEARCHED
  ├──→ SELECTED      (explicit re-research request)
  └──→ ARCHIVED
```

`REJECTED` and `ARCHIVED` are terminal for normal operation, but a human may explicitly restore an item later through a dedicated action.

---

## 5. ResearchPacket States

Initial values:

- `DRAFTING`
- `READY_FOR_REVIEW`
- `CHANGES_REQUESTED`
- `ACCEPTED`
- `REJECTED`
- `FAILED`

Flow:

```text
DRAFTING
  ├──→ READY_FOR_REVIEW
  └──→ FAILED

READY_FOR_REVIEW
  ├──→ ACCEPTED
  ├──→ CHANGES_REQUESTED
  └──→ REJECTED

CHANGES_REQUESTED
  └──→ DRAFTING
```

A post plan may only use an `ACCEPTED` research packet.

---

## 6. Claim Verification States

Use the canonical verification statuses from `06_FACT_CHECKING_PROTOCOL.md`:

- `UNVERIFIED`
- `SUPPORTED`
- `MOSTLY_SUPPORTED`
- `PARTLY_SUPPORTED`
- `MIXED`
- `MISLEADING_WITHOUT_CONTEXT`
- `CONTRADICTED`
- `NOT_ESTABLISHED`
- `STALE`
- `REQUIRES_HUMAN_REVIEW`

These values are evidence conclusions, not simple process states.

Process metadata should separately indicate whether verification is currently running.

A claim begins as:

`UNVERIFIED`

After verification it may enter any allowed verdict state.

---

## 7. Publishability of Claim Verdicts

Default policy:

### Directly usable with ordinary QA

- `SUPPORTED`
- `MOSTLY_SUPPORTED`

### Usable only with explicit contextual wording and/or human review

- `PARTLY_SUPPORTED`
- `MIXED`
- `MISLEADING_WITHOUT_CONTEXT`

### Not usable as an asserted factual claim

- `CONTRADICTED`
- `NOT_ESTABLISHED`
- `STALE`

### Blocked pending human decision

- `REQUIRES_HUMAN_REVIEW`

A `CONTRADICTED` claim may still appear in a fact-check post as the **claim being evaluated**, but must not be presented as established fact.

---

## 8. Post States

Initial `PostStatus` values:

- `PLANNING`
- `DRAFTING`
- `COPY_REVIEW`
- `CHANGES_REQUESTED`
- `COPY_APPROVED`
- `ART_PREPARING`
- `RENDERING`
- `QA_REVIEW`
- `QA_FAILED`
- `FINAL_REVIEW`
- `APPROVED`
- `REJECTED`
- `EXPORTED`
- `PUBLISHED_MANUAL`
- `ARCHIVED`

---

## 9. Normal Post Flow

```text
PLANNING
   ↓
DRAFTING
   ↓
COPY_REVIEW
   ├──→ CHANGES_REQUESTED ─→ DRAFTING
   ├──→ REJECTED
   └──→ COPY_APPROVED
             ↓
       ART_PREPARING
             ↓
         RENDERING
             ↓
         QA_REVIEW
          ├──→ QA_FAILED ─→ RENDERING / DRAFTING
          └──→ FINAL_REVIEW
                    ├──→ REJECTED
                    ├──→ CHANGES_REQUESTED
                    └──→ APPROVED
                              ↓
                           EXPORTED
                              ↓
                      PUBLISHED_MANUAL
```

`PUBLISHED_MANUAL` is informational: a human indicates that an approved exported post was manually published.

The engine itself does not publish in version 1.

---

## 10. Entry Requirements by Post State

### `PLANNING`

Requires:

- selected topic;
- accepted research packet;
- sufficient verified claims.

### `DRAFTING`

Requires:

- chosen format family;
- post plan;
- locked claim references.

### `COPY_REVIEW`

Requires:

- structured post copy;
- claim-lock QA passed;
- no unsupported new factual assertions.

### `COPY_APPROVED`

Requires:

- human approval record;
- unresolved copy changes = none.

### `ART_PREPARING`

Requires:

- approved copy;
- mascot/art brief;
- approved/reusable asset or bounded generation request.

### `RENDERING`

Requires:

- valid render specification;
- exact template version;
- all referenced assets available.

### `QA_REVIEW`

Requires:

- render output exists;
- render hash recorded.

### `FINAL_REVIEW`

Requires:

- automated QA passed;
- high-risk factual review passed where required.

### `APPROVED`

Requires:

- explicit human final-render approval.

### `EXPORTED`

Requires:

- approved post;
- final files copied to export location;
- hashes recorded.

---

## 11. Human Gates

Mandatory human decisions in version 1:

### Topic
A human selects a candidate before full research normally begins.

### Research
A human may be required to accept the research packet before drafting. During early rollout, this should be mandatory.

### Copy
A human must approve copy.

### High-Risk Facts
A human must explicitly review high-risk claims.

### Final Render
A human must approve the final visual.

No provider output may simulate these approvals.

---

## 12. High-Risk Override

If topic risk becomes `HIGH` or `CRITICAL` at any point:

- current workflow may continue gathering evidence;
- final publishability is blocked until required human review exists.

If a post becomes high-risk after copy approval due to new information:

- invalidate prior final approval;
- return to an appropriate review state;
- append an audit event.

---

## 13. Stale Evidence

When a claim becomes `STALE`:

- any draft or post depending on that claim becomes non-finalizable;
- if already in `FINAL_REVIEW`, return it to `DRAFTING` or `COPY_REVIEW` depending on impact;
- if already `APPROVED` but not published, invalidate approval;
- if marked `PUBLISHED_MANUAL`, open a correction/review task.

Do not silently replace the claim with a newer number.

---

## 14. Failure States and Rollback

External failures must not corrupt workflow state.

Examples:

### Research provider failure

Topic:
`RESEARCHING -> SELECTED`

Research packet:
`DRAFTING -> FAILED`

### Image generation failure

Post remains:
`ART_PREPARING`

No copy approval is lost.

### Render failure

Post remains or returns:
`RENDERING`

### QA failure

Post:
`QA_REVIEW -> QA_FAILED`

Then an explicit remediation chooses:

- `QA_FAILED -> RENDERING` for layout/art problems;
- `QA_FAILED -> DRAFTING` for factual/copy problems.

---

## 15. Retry Rules

Every external call should have a bounded retry policy.

Default philosophy:

- transient network/provider error: limited automatic retry;
- schema-validation failure: at most one bounded repair/retry unless otherwise configured;
- factual verification failure: no blind retry to obtain a more favorable verdict;
- source unavailable: try alternate retrieval method/source, but record failure;
- budget blocked: no retry until budget condition changes or human override is explicit.

Retries must reuse or record a stable operation/workflow ID.

---

## 16. Telegram Callback Idempotency

Each review action should have a stable callback/action ID.

If Telegram delivers the same callback twice:

- the second operation must not create duplicate approvals;
- it must not repeat a state transition;
- it should return the current state or an “already processed” response.

---

## 17. Concurrent Operations

Version 1 should prevent conflicting operations on the same entity.

Examples:

- do not run two research jobs for the same selected topic version simultaneously;
- do not render while copy is being changed;
- do not approve a render that is no longer the latest render version.

Use transaction checks and version fields where needed.

---

## 18. Optimistic Versioning

Mutable review entities should include an integer revision/version where useful.

Examples:

- research packet version;
- copy version;
- render version.

A human approval must reference the version actually reviewed.

Changing the content after approval invalidates the approval for the newer version.

---

## 19. Approval Invalidation

Approval is not permanent across edits.

Examples:

- change factual copy after `COPY_APPROVED` → copy approval invalid;
- regenerate a materially different final render after `APPROVED` → final approval invalid;
- change source/claim mapping → factual review may be invalid.

The system must not carry approval forward silently.

---

## 20. Audit Requirements

Every successful state transition must append an `AuditEvent` containing:

- entity;
- old state;
- new state;
- actor;
- reason/action;
- timestamp.

Failed illegal transitions should also be logged at an appropriate level.

---

## 21. CLI and Telegram Must Share Workflow Logic

The CLI may perform maintenance or manual operations.

Telegram may trigger editorial operations.

Both must call the same service/workflow methods.

Do not implement a second set of transition rules inside Telegram handlers.

---

## 22. Discovery Scheduling State

Three daily scans should be configured as named windows rather than hard-coded application assumptions.

Conceptually:

- `SCAN_A`
- `SCAN_B`
- `SCAN_C`

Each window has:

- configured local time;
- timezone;
- enabled flag.

Changing scan time must not require code changes.

---

## 23. State Machine Tests

Before feature implementation is considered complete, tests must cover:

- every legal transition;
- representative illegal transitions;
- duplicate approval callbacks;
- approval invalidation;
- stale claim invalidation;
- high-risk human gate;
- retry rollback behavior;
- version mismatch during approval;
- failed render recovery.

These tests should not call external APIs.

---

## 24. Initial Implementation Order

The state machine should be implemented before AI integrations.

Milestone sequence:

1. enums;
2. domain entities/schemas;
3. transition rules;
4. persistence;
5. audit events;
6. fake-provider vertical workflow;
7. Telegram actions;
8. real providers later.

This allows the mechanical spine to be tested without spending API money.

---

## 25. Golden Rule

**A model may fail, retry, or hallucinate; the state machine must remain boring, explicit, and correct.**
