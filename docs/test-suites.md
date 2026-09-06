# Test Suites

Suites group Test Cases for execution. Requirements and Test Cases define expected behavior.

| Suite ID | Purpose and cases | Trigger | Dependencies／order | Setup／teardown |
|---|---|---|---|---|
| SUITE-UNIT | Twelve results covering `OB-001`–`OB-009`, including parameterized invalid and empty snapshots. | Local and every CI push／PR | Cases are independent; no required order | Construct in-memory `OrderBook`; no global state |
| SUITE-REST-CONTRACT | Eleven results covering `REST-001`–`REST-009`, including cardinality and schema parameters. | Local and every CI push／PR | Independent and parallel-safe | Inject `httpx.MockTransport`; context manager closes the client |
| SUITE-WS-CONTRACT | Twelve results covering `WS-001`–`WS-012`, including three invalid-event parameters. | Local and every CI push／PR | Independent; fake message order is case-local | Create a new fake connection per case; async context exits after the case |
| SUITE-DOC-CONTRACT | Five results covering `DOC-001`–`DOC-005`. | Local and every CI push／PR | Read-only repository inspection | Parse canonical Markdown, Python AST, configured endpoints, workflow text, and governance contracts |
| SUITE-REGRESSION | Union of unit, REST contract, WebSocket contract, and documentation contract suites: 40 results. | Push, pull request, and `workflow_dispatch` | Python 3.12／3.14 matrix jobs run independently | Fresh GitHub-hosted job; install package; upload JUnit even on failure |
| SUITE-LIVE | Five cases: `LIVE-REST-001`–`003`, `LIVE-WS-001`, `LIVE-SYNC-001`. | Manually triggered workflow only | pytest executes the job sequentially; cases share no persistent state | New public clients／connections per case; bounded 30-second case timeout; no cleanup data |

## Commands

```powershell
& '.\.venv\Scripts\python.exe' -m pytest tests/unit -v
& '.\.venv\Scripts\python.exe' -m pytest tests/contract/test_rest_contract.py -v
& '.\.venv\Scripts\python.exe' -m pytest tests/contract/test_websocket_contract.py -v
& '.\.venv\Scripts\python.exe' -m pytest tests/meta -v
& '.\.venv\Scripts\python.exe' -m pytest tests/unit tests/contract tests/meta -v
& '.\.venv\Scripts\python.exe' -m pytest tests/live -v -m live
```

The live suite can fail because of external availability, rate limits, DNS, regional policy, or runner network policy. Those outcomes remain live evidence and do not change the deterministic suite result.
