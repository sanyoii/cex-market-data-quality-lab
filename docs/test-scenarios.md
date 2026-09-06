# Test Scenarios

Scenarios describe user-visible or system-level intent. They do not duplicate individual test steps.

| ID | Type | Scenario and purpose | Requirements | Service boundaries |
|---|---|---|---|---|
| SCN-001 | Positive／safety | Read a public symbol book ticker and reject unusable top-of-book data. | REQ-SAFE-001, REQ-REST-001 | Caller → REST client → Binance REST／mock transport |
| SCN-002 | Positive／state | Request public depth and construct a valid local order-book snapshot. | REQ-REST-002, REQ-SYNC-001 | Caller → REST client → order-book state |
| SCN-003 | Positive | Read exchange metadata needed to interpret a public symbol. | REQ-REST-003 | Caller → REST client → Binance REST／mock transport |
| SCN-004 | Negative | Preserve a structured exchange error for diagnosis. | REQ-REST-004 | Binance REST／mock transport → REST client → caller |
| SCN-005 | Positive／protocol | Subscribe to a symbol stream, validate events, and unsubscribe safely. | REQ-WS-001, REQ-WS-002 | Caller → WebSocket client → Binance stream／fake connection |
| SCN-006 | Negative | Reject malformed JSON, wrong payload shape, missing fields, wrong-symbol, invalid-number, crossed, or out-of-order stream events. | REQ-WS-002 | Stream payload → WebSocket validation → caller |
| SCN-007 | Positive／state | Align a REST snapshot with buffered diff-depth events. | REQ-REST-002, REQ-SYNC-001 | WebSocket buffer ↔ REST snapshot → local order book |
| SCN-008 | Negative／state | Detect stale events and sequence gaps without corrupting state. | REQ-SYNC-001 | Diff-depth event → order-book transition |
| SCN-009 | Evidence | Produce reproducible deterministic evidence and distinct live evidence. | REQ-EVID-001 | pytest → GitHub Actions → JUnit／evidence record |

Each scenario maps to concrete cases in [Test Cases](test-cases.md) and to implementation evidence in the [Traceability Matrix](traceability-matrix.md).
