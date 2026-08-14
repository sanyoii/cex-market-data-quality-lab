# Market-Data Risk Analysis

| Risk | Failure signal | Test response |
|---|---|---|
| Stale REST snapshot | Snapshot update ID trails buffered events | Discard stale events and require the first applicable event to overlap the snapshot boundary |
| Dropped WebSocket event | Next first update ID exceeds the expected ID | Raise a sequence-gap error and require a new snapshot |
| Duplicate event | Final update ID does not exceed local state | Ignore the event without changing the book |
| Crossed book | Best bid exceeds best ask | Reject the state and report both prices |
| Invalid numeric data | Price or quantity cannot be parsed or violates its domain | Fail the contract check with the field name |
| External timeout | REST or WebSocket response exceeds the configured limit | Stop with a bounded timeout; do not wait without a limit |
| Rate limit or network policy | HTTP 418／429, disconnect, DNS failure, or runner block | Record the live test as failed or blocked; do not convert it to a deterministic PASS |

The first release covers public market data. Authentication, balances, orders, matching-engine execution, funding, liquidation, KYC, wallets, and chain confirmations remain outside scope.
