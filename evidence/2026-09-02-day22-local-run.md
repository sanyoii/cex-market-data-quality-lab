# Day 22 local completion run — 2026-09-02

- Status: Passed locally / Unpublished
- Recorded at: `2026-09-02T02:22:44Z`
- Project type: Personal portfolio project; this does not claim Binance, BTSE, or other exchange employment or ownership.
- Public CI/current-head live: Incomplete

## Evidence boundary

This run validates a small, repeatable public CEX market-data testing project. It covers public REST and WebSocket contracts, deterministic order-book logic, documentation governance, and five short-lived live checks. No API key, account, order, or fund movement was used. No confidential employer material or production incident data was used.

The evidence does not cover authenticated trading, deposits, withdrawals, balances, KYC, production reliability, or long-running socket operation. Current Binance WebSocket documentation also describes a 24-hour connection limit, ping/pong requirements, and a `serverShutdown` event; those lifecycle behaviors are outside this short-lived mini-project and remain unverified.

## Public contract freshness

Checked on `2026-09-02` against current primary sources:

- [Binance Spot REST API](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md): `exchangeInfo`, order-book depth, and symbol book-ticker public contracts.
- [Binance Spot WebSocket streams](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md): market-data-only endpoint, lowercase stream names, `bookTicker`, diff-depth sequencing, snapshot synchronization, zero-quantity deletion, and gap handling.
- Fresh public REST observations confirmed `BTCUSDT` was `TRADING`, included `PRICE_FILTER` and `LOT_SIZE`, and returned positive, non-crossed order-book values. Volatile prices are intentionally not retained as portfolio evidence.

## Environment and source state

- Base revision: `8fd5081254b5429e480ec20a56ef09bcc6f5ab9e`
- Branch: `main`
- Candidate state: Uncommitted local working tree based on the revision above; pre-existing dirty changes were preserved and nothing was staged.
- Runtime: Python `3.14.2`
- Dependencies: `httpx 0.28.1`, `websockets 17.0.1`, `pytest 9.1.1`

## Commands and results

Deterministic suite:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; .\.venv\Scripts\python.exe -m pytest tests\unit tests\contract tests\meta -q -p no:cacheprovider --junitxml=reports\deterministic-2026-09-02-day22.xml
```

- Result: `40 passed in 0.30s`
- JUnit SHA-256: `5f2d9eb48b64f1c385121b248d2bce508a0964352abc5c8b752b2ebf8c8a9927`

Live public market-data suite:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; .\.venv\Scripts\python.exe -m pytest tests\live -q -m live -p no:cacheprovider --junitxml=reports\live-2026-09-02-day22.xml
```

- Result: `5 passed in 22.29s`
- JUnit SHA-256: `ed76c909837cff44ad68a6f265fc3d7a61228d088afa4436b39b1863dc037d4c`
- Retry count: 0

Parent Portfolio verification retained three distinct outcomes:

1. Unscoped `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` — **Fail during collection**. The parent environment discovered the nested lab but did not contain its `httpx` dependency or installed `cex_quality` package. This command is not a valid aggregate runner for the two independent environments.
2. Scoped `.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider` inside the sandbox — **Blocked by environment**, `17 passed, 13 errors`; Playwright could not launch Chromium because `spawn EPERM` was returned.
3. The same scoped command outside the sandbox — **Pass**, `30 passed in 10.79s`.

The later PASS does not erase either earlier result. The lab's own deterministic and live suites were run separately with the lab `.venv`, as recorded above.

## Completion decision

Day 22 is complete as a local, unpublished portfolio artifact: the public interfaces, reusable checks, acceptance criteria, source links, and fresh local run evidence are present. This is not evidence that public CI ran against the uncommitted candidate. Manual charters remain designed but not executed, and no deploy or publication was attempted.
