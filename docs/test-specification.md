# Test Specification

Status: Local review candidate. Public CI verification pending.

This specification indexes the project's QA lifecycle. The Test Plan defines scope and execution strategy.

```text
Requirement and Business Rules
  -> Test Plan and Strategy
  -> Test Scenarios
  -> Test Cases and Test Data
  -> Test Suites
  -> Test Scripts
  -> Test Runs
  -> Defect History and Test Summary
```

| Lifecycle artifact | Canonical document／path |
|---|---|
| Requirements and business rules | [requirements.md](requirements.md) |
| Acceptance and completion gate | [acceptance-criteria.md](acceptance-criteria.md) |
| Test Plan and strategy | [test-plan.md](test-plan.md) |
| Test Scenarios | [test-scenarios.md](test-scenarios.md) |
| Test Cases | [test-cases.md](test-cases.md) |
| Test Data Profiles | [test-data-profiles.md](test-data-profiles.md) |
| Test Suites | [test-suites.md](test-suites.md) |
| Test Scripts and assertions | [automation-map.md](automation-map.md), `tests/` |
| Requirements traceability | [traceability-matrix.md](traceability-matrix.md) |
| Test Runs and artifacts | [`evidence/`](../evidence/README.md) |
| Exploratory test charters | [exploratory-charters.md](exploratory-charters.md) |
| Defect history and release conclusion | [test-summary-report.md](test-summary-report.md) |
| Risks and exclusions | [risk-analysis.md](risk-analysis.md), [limitations.md](limitations.md) |

## Identification conventions

- Requirements: `REQ-*`
- Business rules: `BR-*`
- Scenarios: `SCN-*`
- Test Cases: `OB-*`, `REST-*`, `WS-*`, `DOC-*`, `LIVE-*`
- Test Data Profiles: `DATA-*`
- Test Suites: `SUITE-*`
- Defects: `DEF-*`
- Exploratory charters: `EXP-*`

No Jira integration exists for this portfolio project. Project-local IDs provide stable traceability without implying an external ticket record.

Human exploratory testing has not been executed. The charter document records planned sessions without claiming test evidence.
