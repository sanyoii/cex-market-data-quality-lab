# Manual Test Run: YYYY-MM-DD

Status: Planned, Passed, Failed, Blocked, or Incomplete. See [Test Governance](../docs/test-governance.md).

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
- Control acknowledgment timeout: `<10 seconds recommended, or value and reason>`
- Event receive timeout: `<10 seconds recommended, or value and reason>`
- Case timeout: `<30 seconds recommended, or value and reason>`

## Case results

| Case ID | Requirement／scenario | Start／end UTC | Expected result | Actual result | Status | Evidence path | SHA-256／availability | Defect ID | Retry count | Cleanup |
|---|---|---|---|---|---|---|---|---|---:|---|
| `MTC-*` | `<REQ-*／MSCN-*>` | `<times>` | `<observable expectation>` | `<observed values and behavior>` | `<Pass／Fail／Blocked／Skipped>` | `<evidence/manual/run-id/path>` | `<hash or unavailable with reason>` | `<ID or none>` | `0` | `<completed／not required／blocked>` |

## Artifact inventory

| Artifact | Related case | Relative path or URL | SHA-256 | Accessibility／retention |
|---|---|---|---|---|
| `<response, frame log, screenshot, or worksheet>` | `<MTC-*>` | `<path or URL>` | `<hash or unavailable with reason>` | `<checked status and retention>` |

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
- Warnings／blockers: `<none or details>`
- Release recommendation: `<recommend, reject, or no decision>`

## Review

- Tester conclusion: `<statement>`
- Reviewer conclusion: `<statement or pending>`
- Evidence accessibility check: `<Pass／Fail／Blocked>`
