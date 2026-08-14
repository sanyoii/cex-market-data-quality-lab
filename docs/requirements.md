# Requirements and Business Rules

Status: Local review candidate. The published baseline was verified against the implementation and public contracts on 2026-08-14.

This portfolio project has no Jira project, so it uses stable project-local requirement IDs instead of invented issue keys. Binance's official Spot API documentation defines external contracts. Project policies define local quality rules.

## Requirements

| ID | Requirement | Acceptance criteria | Source |
|---|---|---|---|
| REQ-SAFE-001 | The project must use public market-data interfaces only. | A deterministic scope gate verifies the allowlisted public base URLs and endpoint paths and rejects configured credentials, account endpoints, trading actions, balances, orders, or real-fund operations in source, executable tests, and CI. | Project safety boundary |
| REQ-REST-001 | The REST client must validate a symbol book ticker. | Normalize the requested symbol; parse bid／ask prices and quantities as `Decimal`; require positive values and `best bid <= best ask`. | Binance REST: Symbol order book ticker |
| REQ-REST-002 | The REST client must validate a depth snapshot before returning it. | Send the normalized symbol and requested limit; require a positive update ID, positive levels, both sides, and a non-crossed book. | Binance REST: Order book |
| REQ-REST-003 | The REST client must return the requested symbol's exchange metadata. | Require a single symbol and retain its symbol, trading status, and filter types. | Binance REST: Exchange information |
| REQ-REST-004 | REST failures must remain diagnosable. | Preserve HTTP status, exchange error code, and exchange message for an error response; preserve the bounded `httpx.ReadTimeout` type for a transport timeout. | Binance REST error response contract plus project timeout policy |
| REQ-WS-001 | The WebSocket client must bound subscription waits and correlate control messages. | Send subscribe／unsubscribe requests, accept only the matching acknowledgement ID, tolerate an in-flight market event while waiting, and stop on timeout. | Binance WebSocket live subscribing／unsubscribing |
| REQ-WS-002 | Book-ticker stream events must satisfy the expected contract. | Require the expected symbol, positive prices and quantities, a non-crossed market, and non-decreasing update IDs. | Binance Individual Symbol Book Ticker Streams |
| REQ-SYNC-001 | A REST snapshot and diff-depth stream must create a consistent local order book. | Discard stale events, apply continuous updates in order, delete zero-quantity levels, reject crossed or empty state, and fail before mutation on a sequence gap. | Binance local order-book synchronization procedure plus project invariants |
| REQ-EVID-001 | Deterministic and live evidence must remain distinguishable. | Deterministic tests run without network access; live tests run in a distinct job; each published run records revision, environment, result, limitations, and JUnit artifacts. | Project evidence policy |

## Business rules

| ID | Rule | Classification |
|---|---|---|
| BR-001 | Prices must be positive. Snapshot quantities must be positive; a diff-depth quantity of zero deletes the price level. | External contract plus project validation |
| BR-002 | A valid local book must contain bids and asks, with `best bid <= best ask`. | Project market invariant |
| BR-003 | An event whose final update ID is not newer than local state is stale and must not mutate state. | Synchronization rule |
| BR-004 | If the next event starts after the expected update ID, synchronization has a gap and must stop before mutation. | Synchronization rule |
| BR-005 | Record a live network failure, rate limit, DNS failure, or regional block as live failure or blocked evidence. Never convert it into deterministic PASS. | Project evidence rule |
| BR-006 | Do not retry assertions. Allow a retry only for an identified transient infrastructure operation, and disclose it in the Test Run. | Project execution rule |

## External contract sources

- [Binance Spot REST API](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md)
- [Binance Spot WebSocket streams](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)

External behavior can change. Review each requirement update against the official source, then update the traceability matrix.
