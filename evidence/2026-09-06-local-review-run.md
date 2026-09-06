# Local career-content review run

Status: Passed locally / Unpublished

- Date: 2026-09-06, Asia/Taipei; exact start/end UTC timestamps were not captured. Elapsed durations below are pytest output, not reconstructed timestamps.
- Source: uncommitted local candidate based on `8fd5081254b5429e480ec20a56ef09bcc6f5ab9e`.
- Change: README employment attribution and local/public version clarification. No production-code or test-behavior change.
- Environment: Windows; Python 3.14.2; pytest 9.1.1; pytest-asyncio 1.4.0; httpx 0.28.1; websockets 17.0.1; repository `.venv`.

| Command from this repository | Actual result | Exit |
|---|---|---|
| `.venv/Scripts/python.exe -B -m pytest tests/unit tests/contract tests/meta -q -p no:cacheprovider` | 40 passed in 0.65s; 0 failed, 0 skipped, 0 deselected | 0 |
| `.venv/Scripts/python.exe -B -m pytest tests/live -q -m live -p no:cacheprovider` | 5 passed in 22.61s; 0 failed, 0 skipped, 0 deselected | 0 |

- Retry count: 0 for both CEX runs. No warnings printed by pytest. The documentation-link check preceded creation of this receipt; final documentation validation is recorded separately in the parent review receipt.
- No API key, account, order, or fund movement was used.
- Human exploratory charters and Sanyo's independent coding/explanation exercise: Not run. These are assistant-executed tests.
- Public CI/current-head live: Incomplete for this candidate. No commit, push, workflow dispatch, or publication occurred.
- JUnit: not requested in these commands; console summaries are retained above. No JUnit artifact or timestamp precision is claimed.
- Code/test identity: 10 Python files under `src/` and `tests/`, SHA-256 `7d92873da03f2927bb4db0b80ca7eabd1fb4b6af2e763e00a0f5670b047cf5b6`. Digest input is sorted `src/**/*.py`, then sorted `tests/**/*.py`; for each file, concatenate UTF-8 repository-relative POSIX path, NUL, raw bytes, NUL.

This result does not establish order, wallet, ledger, or production reconnect behavior and does not refresh any downstream release assessment.
