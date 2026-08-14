# Manual Test Run: YYYY-MM-DD

Status: Planned, Pass, Fail, Blocked, or Mixed.

## Run identity

- Tester: `<name>`
- Reviewer: `<name or pending>`
- Start UTC: `YYYY-MM-DDTHH:MM:SSZ`
- End UTC: `YYYY-MM-DDTHH:MM:SSZ`
- Elapsed: `<duration>`
- Branch: `<branch>`
- Full revision: `<Git SHA>`
- Worktree: `<clean or disclosed changes>`

## Environment

- OS: `<name and version>`
- REST client and version: `<tool>`
- WebSocket client and version: `<tool>`
- Network／region: `<relevant condition>`
- REST base URL: `<URL>`
- WebSocket base URL: `<URL>`
- Credential check: `<none configured or stop the run>`

## Case results

| Case ID | Start／end UTC | Actual result | Status | Evidence path | Defect ID | Retry count | Cleanup |
|---|---|---|---|---|---|---:|---|
| `MTC-*` | `<times>` | `<observed values and behavior>` | `<Pass／Fail／Blocked／Skipped>` | `<path or URL>` | `<ID or none>` | `0` | `<completed／not required／blocked>` |

## Defects

| Defect ID | Severity | Case ID | Summary | Reproducibility | Evidence | Status／owner |
|---|---|---|---|---|---|---|
| `<DEF-MAN-*>` | `<S0／S1／S2／S3>` | `<MTC-*>` | `<observed failure>` | `<rate and steps>` | `<path>` | `<state and owner>` |

## Session summary

- Planned: `<count>`
- Executed: `<count>`
- Passed: `<count>`
- Failed: `<count>`
- Blocked: `<count>`
- Skipped: `<count>`
- Open S0／S1 defects: `<count>`
- External-service conditions: `<observed conditions>`
- Retries: `<count and reason>`
- Coverage gaps: `<unexecuted cases or unavailable evidence>`
- Release recommendation: `<recommend, reject, or no decision>`

## Review

- Tester conclusion: `<statement>`
- Reviewer conclusion: `<statement or pending>`
- Evidence accessibility check: `<Pass／Fail／Blocked>`
