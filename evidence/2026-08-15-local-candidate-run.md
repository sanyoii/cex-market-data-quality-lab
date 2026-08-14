# Local Candidate Test Run: 2026-08-15

Status: Passed locally. Public CI verification pending.

## Run identity

- Start UTC: `2026-08-14T16:44:04.0258238Z`
- End UTC: `2026-08-14T16:48:35.3611121Z`
- Overall elapsed: `271.335s`, including the intervals between commands and the final deterministic confirmation
- Source revision: uncommitted local candidate on `9ce65e03b834c79c95bf2488c471be68cb7b1166`
- Branch: `main`
- Source state: task-related production, test, workflow, README, documentation, and evidence changes were uncommitted

## Environment

- Execution location: local
- OS: Windows
- Python: `3.14.2`
- pytest: `9.1.1`
- pytest-asyncio: `1.4.0`
- pytest-timeout: `2.4.0`
- httpx: `0.28.1`
- websockets: `17.0.1`
- External service for live run: Binance public Spot market-data REST and WebSocket interfaces

## Commands and outcomes

| Command | Exit code | Collected | Passed | Failed | Skipped | Deselected | Elapsed | Warnings／blockers | Retry count |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| `.\.venv\Scripts\python.exe -m pytest tests\unit tests\contract tests\meta -v --junitxml=reports\deterministic-2026-08-15-local.xml` | 0 | 39 | 39 | 0 | 0 | 0 | pytest `0.61s`; command `1.368s` | None | 0 |
| `.\.venv\Scripts\python.exe -m pytest tests\live -v -m live --junitxml=reports\live-2026-08-15-local.xml` | 0 | 5 | 5 | 0 | 0 | 0 | pytest `24.51s`; command `25.421s` | None | 0 |
| Final deterministic confirmation after documentation and formatting edits: `.\.venv\Scripts\python.exe -m pytest tests\unit tests\contract tests\meta -q --junitxml=reports\deterministic-2026-08-15-local.xml` | 0 | 39 | 39 | 0 | 0 | 0 | pytest `0.53s`; command `1.676s` | None | 0 |

## Artifacts

| Artifact | Path | SHA-256 | Availability |
|---|---|---|---|
| Deterministic JUnit XML | `reports/deterministic-2026-08-15-local.xml` | `a96084a02eea974f58c58aaa812acacd4bfaa519d080cd214bc23ed868fd988e` | Local generated artifact from final confirmation; reports are not versioned |
| Live JUnit XML | `reports/live-2026-08-15-local.xml` | `450825dfa0b71b321ab2c1be613e249c390dcb61b51c08d845e05c43144eed72` | Local generated artifact; reports are not versioned |

## Observed result

- Final state: Pass for the local candidate.
- Deterministic unit, REST contract, WebSocket contract, and documentation contract results: 39 passed.
- Live public REST, WebSocket ticker, and REST snapshot／diff-depth synchronization results: 5 passed.
- Failed, blocked, skipped, or deselected cases: none.
- Human exploratory session: not executed. The charter status remains Designed, not executed.

## Limitations

- This receipt does not prove Python 3.12 or GitHub-hosted runner compatibility for the local candidate.
- The live result proves observed public-service behavior only during the recorded window.
- The local candidate remains uncommitted and has no public workflow artifact.
