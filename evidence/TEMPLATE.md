# Test Run Record: YYYY-MM-DD

Status: Planned, Passed, Failed, Blocked, or Incomplete. See [Test Governance](../docs/test-governance.md).

## Run identity

- Start UTC: `YYYY-MM-DDTHH:MM:SSZ`
- End UTC: `YYYY-MM-DDTHH:MM:SSZ`
- Elapsed: `0.00s`
- Source revision: `<full Git SHA>` or `uncommitted local candidate at <HEAD>`
- Branch: `<branch>`
- Source-state note: `<clean, or list task-related modified files>`

## Environment

- Execution location: `<local or CI provider／runner>`
- OS: `<OS and version>`
- Python: `<version>`
- pytest: `<version>`
- Relevant dependencies: `<name and version>`
- External services: `<none, or named public service and endpoint class>`

## Commands and outcomes

| Command | Exit code | Collected | Passed | Failed | Skipped | Deselected | Warnings／blockers | Retry count |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `<exact command>` | `<code>` | `<count>` | `<count>` | `<count>` | `<count>` | `<count>` | `<none or details>` | `0` |

Record every attempt. Keep an earlier Fail or Blocked row after a later pass.

## Artifacts

| Artifact | Path or URL | SHA-256 | Retention／availability |
|---|---|---|---|
| JUnit XML | `<path or URL>` | `<hash, or unavailable with reason>` | `<policy or local-only>` |
| Log or screenshot | `<path or URL>` | `<hash, or unavailable with reason>` | `<policy or local-only>` |

## Observed result

- Final state: `<Passed, Failed, Blocked, or Incomplete>`
- Failed／blocked cases: `<IDs and concise causes>`
- Warnings: `<warnings or none>`
- External-service conditions: `<observed conditions or not applicable>`
- Human exploratory session: `<charter ID and tester, or not executed>`

## Limitations

- `<What this run does not prove>`
