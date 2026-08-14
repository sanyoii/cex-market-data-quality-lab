# Acceptance Criteria

Status: Local review candidate. Public CI and live evidence remain available for the 2026-08-14 baseline.

Requirement IDs and business-rule sources are defined in [Requirements and Business Rules](requirements.md).

## Scope

The project checks Binance Spot public market data through REST and WebSocket interfaces. It uses no API key, account data, order placement, or real funds.

## Required behavior

- Build an order book from a REST depth snapshot using `Decimal` values.
- Apply buffered WebSocket diff-depth events in update-ID order.
- Ignore stale events and stop on a sequence gap.
- Remove a price level when an update sets its quantity to zero.
- Reject an empty or crossed order book.
- Validate REST success and structured error responses.
- Validate WebSocket subscription acknowledgement, event schema, symbol, prices, quantities, timeout, and unsubscribe acknowledgement.
- Produce separate deterministic and live test results.

## Completion gate

- A clean environment can install the declared dependencies and run the documented commands.
- Deterministic tests pass without network access.
- A fresh live REST and WebSocket run records its timestamp, Python version, source revision or local-state identifier, exact command, outcome, warnings, and limitations.
- CI runs deterministic tests and uploads JUnit XML. Live automation runs through a separate manually triggered workflow job.
- Public copy labels this work as a personal portfolio project. It must not imply Binance or BTSE employment ownership.
