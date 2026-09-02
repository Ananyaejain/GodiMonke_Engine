# Fixture Review Sheet

## Status

These five fixtures are **provisional human-review fixtures**.

Do not run the paid benchmark until both human owners accept the gold logic.

## Proposed fixtures

| Fixture | Family | Proposed gold verdict | Main trap |
|---|---|---|---|
| F01 | Union Budget / finance | SUPPORTED | Direct capex vs effective capex; BE vs actual |
| F02 | Infrastructure | SUPPORTED | Network length vs kilometres physically constructed |
| F03 | Political claim-check | MISLEADING_WITHOUT_CONTEXT | Cut vs BE, while nominal year-on-year capex rose |
| F04 | India geopolitics | SUPPORTED | Border-management measures vs final boundary settlement |
| F05 | Under-covered institutional/policy | MISLEADING_WITHOUT_CONTEXT | Unfulfilled defence offsets vs overdue/default |

## Human review questions

For each fixture, confirm:

1. Is the verification claim phrased fairly?
2. Is the proposed verdict defensible from the frozen evidence?
3. Is any material caveat missing?
4. Are the prohibited claims genuinely unsupported?
5. Are the locked copy claims safe to use verbatim?
6. Is the fixture representative of a real Godi Monke production task?
7. Would a model need outside knowledge to answer it? If yes, revise the fixture.
8. Is the risk level appropriate?

## Important

The model must never see the `gold` object during inference.

The harness should create a provider request from a copy of the fixture with `gold` removed.
