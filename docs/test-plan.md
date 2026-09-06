# Test Plan and Strategy

Status: Active for the local governance candidate based on public head `8fd5081`. Public CI for this candidate and current-head live automation are pending.

## Objective

Demonstrate that a small Python client can consume public CEX REST and WebSocket market data without silently accepting contract violations or corrupting synchronized local order-book state.

## Scope

Included:

- Binance Spot public `exchangeInfo`, `bookTicker`, and depth REST responses.
- Public `bookTicker` and diff-depth WebSocket streams.
- Order-book numeric, ordering, staleness, continuity, and deletion rules.
- Deterministic unit／contract tests and live integration tests with distinct labels.
- JUnit and versioned execution evidence.

Excluded:

- Authentication, account data, balances, trading, orders, matching-engine execution, deposits, withdrawals, wallets, chain confirmations, funding, liquidation, KYC, AML, UI, performance, load, and security penetration testing.
- Production reconnect／resynchronization loops and cross-exchange compatibility.

## Strategy

| Layer | Current coverage | Purpose | Network |
|---|---:|---|---|
| Unit | 12 pytest results | Order-book state transitions and invariants | No |
| REST contract | 11 pytest results | Request shape, response parsing, schema failures, errors, cardinality, and timeout through `httpx.MockTransport` | No |
| WebSocket contract | 12 pytest results | Control acknowledgments, JSON／schema validation, ordering, synchronization, and timeout through fake connections | No |
| Documentation contract | 5 pytest results | Requirements mapping, case-to-script mapping, Markdown links, public-only scope, and shared governance | No |
| Live integration | 5 pytest results | Current public REST／WebSocket compatibility and snapshot／stream synchronization | Yes |

The local governance candidate contains 40 deterministic results. Public head `8fd5081` passed 39 deterministic results on Python 3.12 and 3.14 in [run 31823105148](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31823105148). Current-head live automation has not run; the latest public live receipt remains the historical `9ce65e0` run. Live tests do not replace deterministic coverage and do not run on every push.

[Exploratory charters](exploratory-charters.md) cover schema drift, disconnect／resynchronization, symbol boundaries, and injected rate-limit or network-policy failures. Their status is Designed, not executed; no human exploratory result is included in the PASS evidence.

## Infrastructure and environment

| Item | Deterministic | Live |
|---|---|---|
| Runtime | Python 3.12 and 3.14 in CI | Python 3.14 in manual CI |
| REST | `httpx.MockTransport` | `https://data-api.binance.vision` |
| WebSocket | In-memory fake connection | `wss://data-stream.binance.vision` |
| Secrets | None | None |
| Persistent data | None | None |
| Result | JUnit XML per Python version | JUnit XML live artifact |

## Entry criteria

- Record the source revision.
- Declared test dependencies install successfully.
- Deterministic tests use only mocks／fakes and require no external service.
- Live execution uses public endpoints and has network access.
- Configure no API key, account credential, or trading permission.

## Exit criteria

- All 40 deterministic results pass on Python 3.12 and 3.14 before publication.
- All requirements in the traceability matrix map to at least one test or explicit inspection gate.
- No known open S0 or S1 defect remains for the published baseline.
- A publication verification includes a manually triggered five-case live automation result. External failures remain visible as Fail or Blocked.
- Retain JUnit artifacts and known limitations.

## Priority model

The canonical definitions are in [Test Governance](test-governance.md).

| Priority | Meaning | Release treatment |
|---|---|---|
| P0 | Safety boundary or state-corruption risk | Must pass |
| P1 | Core functional, contract, synchronization, traceability, or release-evidence behavior | Must pass |
| P2 | Defensive edge behavior with bounded impact | Must pass for regression baseline |
| P3 | Informational or future coverage | Does not block unless promoted |

Test priority controls execution importance. Defect severity rates the impact of the observed failure.

## Defect severity model

The canonical definitions are in [Test Governance](test-governance.md).

| Severity | Impact | Release treatment |
|---|---|---|
| S0 Critical | Safety boundary breach, real-fund exposure, or unrecoverable state corruption | Stop publication and correct before any rerun |
| S1 High | Core contract or synchronization failure with no safe workaround | Block publication |
| S2 Medium | Bounded incorrect behavior, false test result, or diagnosability gap with a safe workaround | Correct or document before baseline approval |
| S3 Low | Minor documentation or low-impact usability defect | Track without blocking the baseline |

## Retry and timeout policy

- REST and WebSocket operations use explicit bounded timeouts.
- Assertions and contract violations are never retried.
- Current CI performs no automatic test retry.
- Keep any future infrastructure retry outside assertions. Record its attempt count and original failure in the Test Run.
