# Test Cases

## Deterministic cases

| ID | Area | Expected result |
|---|---|---|
| OB-001 | REST depth snapshot | Highest bid and lowest ask become the visible top of book |
| OB-002 | Diff-depth update | New levels are added and zero-quantity levels are removed |
| OB-003 | Stale event | Event is ignored and local update ID does not change |
| OB-004 | Sequence gap | Client raises `SequenceGapError` before applying the event |
| OB-005 | Crossed snapshot | Client raises `MarketInvariantError` |
| OB-006 | Buffered synchronization | Stale events are discarded and continuous events update the book |
| OB-007 | Invalid snapshot values | Zero／negative price or quantity is rejected |
| OB-008 | Invalid update value | Negative quantity is rejected; zero remains the deletion signal |
| REST-001 | Book ticker | Client returns normalized symbol and `Decimal` values |
| REST-002 | Crossed ticker | Client rejects best bid above best ask |
| REST-003 | Depth request | Client sends normalized symbol and requested limit, then validates the snapshot |
| REST-004 | Invalid symbol | Client retains HTTP status, Binance error code, and message |
| REST-005 | Exchange info | Client returns the requested symbol, status, and filter types |
| REST-006 | Invalid ticker values | Client rejects non-positive price or quantity |
| WS-001 | Subscription lifecycle | Client subscribes, validates one event, and unsubscribes |
| WS-002 | Update ordering | Client rejects a decreasing update ID |
| WS-003 | Symbol contract | Client rejects an event for another symbol |
| WS-004 | Numeric contract | Client rejects non-positive price or quantity |
| WS-005 | Market invariant | Client rejects best bid above best ask |
| WS-006 | Bad acknowledgement | Client rejects an acknowledgement with the wrong request ID |
| WS-007 | In-flight event | Client waits past market events for the unsubscribe acknowledgement |
| WS-008 | Snapshot／stream integration | Client buffers the stream, loads a snapshot, discards stale events, and applies continuous updates |
| WS-009 | Receive timeout | Client stops when the configured receive limit expires |

Parameterized cases count as separate pytest results. The fresh receipt records pytest's collected count rather than relying on this table.

## Live cases

| ID | Interface | Expected result |
|---|---|---|
| LIVE-REST-001 | `exchangeInfo` | `BTCUSDT` is available for trading with price and lot-size filters |
| LIVE-REST-002 | `bookTicker` | Positive quantities and a non-crossed top of book |
| LIVE-REST-003 | Depth snapshot | Positive update ID and valid order-book state |
| LIVE-WS-001 | `bookTicker` stream | Three valid events with non-decreasing update IDs |
| LIVE-SYNC-001 | REST depth plus diff-depth stream | Three continuous stream events apply after snapshot alignment |
