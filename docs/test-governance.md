# Test Governance

Status: Active for automated and manual testing.

This document defines the shared priority, severity, status, release, timeout, retry, evidence, and defect rules. The [automated Test Plan](test-plan.md), [Manual QA Lifecycle](manual-testing-lifecycle.md), and Test Run templates use these definitions.

## Test priority

| Priority | Meaning | Release treatment |
|---|---|---|
| P0 | Safety boundary or state-corruption risk | Must pass |
| P1 | Core functional, contract, synchronization, traceability, or release-evidence behavior | Must pass |
| P2 | Defensive edge behavior with bounded impact | Must pass for regression baseline |
| P3 | Informational or future coverage | Does not block unless promoted |

Priority sets execution importance. It does not describe the impact of an observed defect.

## Defect severity

| Severity | Impact | Release treatment |
|---|---|---|
| S0 Critical | Safety boundary breach, real-fund exposure, or unrecoverable state corruption | Stop publication and correct before any rerun |
| S1 High | Core contract or synchronization failure with no safe workaround | Block publication |
| S2 Medium | Bounded incorrect behavior, false test result, or diagnosability gap with a safe workaround | Correct or document before baseline approval |
| S3 Low | Minor documentation or low-impact usability defect | Track without blocking the baseline |

## Case and run status

| Level | Allowed values | Meaning |
|---|---|---|
| Case | Pass \| Fail \| Blocked \| Skipped | Pass meets the expected result. Fail contradicts it. Blocked cannot execute because a prerequisite or environment is unavailable. Skipped records a deliberate non-execution and reason. |
| Run | Planned \| Passed \| Failed \| Blocked \| Incomplete | Planned has not started. Passed meets every required gate. Failed contains a required failed case. Blocked has no required failure but at least one required blocked case. Incomplete has a required skipped or missing result. |

Allowed run statuses: `Planned | Passed | Failed | Blocked | Incomplete`.

Run classification follows this order:

1. Any required P0 or P1 Fail makes the run Failed and blocks release.
2. With no required Fail, any required P0 or P1 Blocked makes the run Blocked and produces no release decision.
3. With no required Fail or Blocked, any required P0 or P1 Skipped or missing result makes the run Incomplete and produces no release decision.
4. A run is Passed only when every required P0 and P1 case passes and all other exit criteria are met.

## Timeout and retry

- Automated REST operations default to a 10-second timeout.
- Automated WebSocket receive operations default to a 10-second timeout.
- Each live pytest case has a 30-second timeout.
- Manual runs declare control-acknowledgment, event-receive, and case timeouts before execution. Recommended values are 10, 10, and 30 seconds. A different value requires a reason in the run record.
- Assertions and contract failures receive no retry.
- Infrastructure retry count defaults to zero. A retry requires a recorded reason, the original outcome and evidence, each attempt number, and the final outcome.

## Evidence and storage

Each run records the full source revision, environment, UTC start and end, commands or procedures, expected and actual results, status, warnings, blockers, limitations, retries, defects, and cleanup. Every executed case needs an accessible artifact or an explanation for its absence.

Automated receipts are versioned in `evidence/`; generated JUnit files stay in ignored `reports/` unless a receipt records their hash. Manual artifacts use `evidence/manual/<run-id>/` and include the completed run record plus exported responses, frame logs, screenshots, or worksheets. Evidence paths must not contain credentials or private account data.

## Coverage and release gates

- Map 100% of requirements to scenarios and cases or an explicit inspection gate.
- Execute and pass 100% of planned P0 and P1 cases for a release recommendation.
- Provide accessible evidence for 100% of executed manual cases.
- Keep zero open S0 or S1 defects.
- Treat any required blocked, skipped, or missing result as no release decision.

## Defect lifecycle

Use `New -> Confirmed -> In Progress -> Ready for Retest -> Closed`. Reopen a defect when retest fails. `Deferred` applies only to S2 or S3 with a rationale, owner, and review date. Each defect links the affected requirement, scenario, case, run, and evidence.
