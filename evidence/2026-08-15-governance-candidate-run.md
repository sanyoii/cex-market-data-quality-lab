# Test Run Record: 2026-08-15 Governance Candidate

Status: Passed locally. Public CI and current-head live workflow verification are pending.

## Run identity

- Deterministic start: `2026-08-14T18:17:20.962415Z`
- Live start: `2026-08-14T18:17:27.202730Z`
- Live completion observed: `2026-08-14T18:17:51Z`
- Source revision: uncommitted local candidate based on `8fd5081254b5429e480ec20a56ef09bcc6f5ab9e`
- Branch: `main`
- Source-state note: task-related governance, documentation, meta-test, and evidence changes were uncommitted

## Environment

- Execution location: local Windows host
- Python: `3.14.2`
- pytest: `9.1.1`
- httpx: `0.28.1`
- websockets: `17.0.1`
- External service for live cases: Binance public market-data REST and WebSocket hosts

## Commands and outcomes

| Command | Exit code | Collected | Passed | Failed | Skipped | Deselected | Warnings／blockers | Retry count |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `.\.venv\Scripts\python.exe -m pytest tests\unit tests\contract tests\meta -q --junitxml=reports\deterministic-2026-08-15-governance.xml` | 0 | 40 | 40 | 0 | 0 | 0 | None | 0 |
| `.\.venv\Scripts\python.exe -m pytest tests\live -q -m live --junitxml=reports\live-2026-08-15-governance.xml` | 0 | 5 | 5 | 0 | 0 | 0 | None | 0 |

## Artifacts

| Artifact | Path | SHA-256 | Retention／availability |
|---|---|---|---|
| Deterministic JUnit XML | `reports/deterministic-2026-08-15-governance.xml` | `0c02652532410ffaca98902f060b342602ab75cc8b0d1f31c8fd7fc5877edd52` | Local generated artifact; reports are not versioned |
| Live JUnit XML | `reports/live-2026-08-15-governance.xml` | `8a6226185fc36881e8800d4962105d18be5dfe440183221cd2db8c9aa9b47484` | Local generated artifact; reports are not versioned |

## Observed result

- Final local state: Passed.
- Deterministic result: 40 passed, including five documentation contracts.
- Live result: 5 passed against current public services.
- Failed／blocked cases: none.
- Retries: zero.
- Human manual or exploratory session: not executed.

## Limitations

- Local PASS does not establish GitHub-hosted behavior.
- The live result verifies the uncommitted local candidate, not a public revision.
- No manual `MTC-*` case or exploratory charter was executed.
