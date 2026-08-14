# Local Test Record: 2026-08-14

Status: Publication candidate. Public repository and CI verification are pending.

## Environment

- Recorded: `2026-08-14T14:40:36Z`
- OS: Windows
- Python: `3.14.2`
- pytest: `9.1.1`
- pytest-asyncio: `1.4.0`
- httpx: `0.28.1`
- websockets: `17.0.1`
- Source state: uncommitted project under parent repository HEAD `b18c9b9c95de`
- Source files: `18`
- Source manifest SHA-256: `df6ab71b68dd60558f469e955003a5085a8e1e75693dc93d6175da5e742ad495`

The source-manifest hash excludes `.venv`, caches, generated reports, generated egg metadata, and this dated receipt.

## Deterministic suite

Command:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest tests/unit tests/contract -v --junitxml=reports/deterministic-local.xml
```

Result:

```text
25 passed in 0.16s
Exit code: 0
```

JUnit: `reports/deterministic-local.xml`
SHA-256: `9965d429e9aa52fe8c31f9065f02908fca89832e0179448038e9bdf7ae15fa92`

## Live suite

Command:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest tests/live -v -m live --junitxml=reports/live-local.xml
```

Result:

```text
5 passed in 21.92s
Exit code: 0
```

The live run checked Binance public `exchangeInfo`, `bookTicker`, REST depth, the book-ticker stream, and REST snapshot／diff-depth synchronization for `BTCUSDT`.

JUnit: `reports/live-local.xml`
SHA-256: `78f3b5d2f08d301a6bb08e99379e984ee598f371e8aed292a2902e5e3d446fce`

## Failed attempt retained

An earlier live command collected four tests and returned:

```text
3 passed, 1 failed in 9.71s
Exit code: 1
```

The unsubscribe request received another valid `bookTicker` event before the acknowledgement. The client treated that in-flight event as an invalid acknowledgement. A deterministic regression test now reproduces the ordering. The client waits past market events for the matching request ID, while still rejecting an acknowledgement with the wrong ID. The final five-case live suite passed after that change.

## Additional checks

```text
python -m compileall -q src tests: exit 0
python -m pip check: No broken requirements found.
Secret-pattern scan: 0 candidate assignments or token patterns.
stop-slop phrase and em-dash scan: 0 hits.
```

## Skipped／not proven

- GitHub Actions was not run because no public repository or commit exists.
- Python 3.12 CI compatibility remains unverified. Local execution used Python 3.14.2.
- Public CI verification, CI badges, Portfolio links, resume links, and LinkedIn Featured links remain pending.
