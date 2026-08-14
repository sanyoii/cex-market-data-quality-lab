# Test Cases

Each case has one direction of execution and an observable assertion. Decision branches are split into separate cases or parameter rows.

## Deterministic cases

| ID | Priority | Requirement／scenario | Preconditions and data | Atomic actions | Expected result | Suite |
|---|---|---|---|---|---|---|
| OB-001 | P1 | REQ-SYNC-001／SCN-002 | DATA-OB-VALID snapshot with unsorted levels | 1. Construct the book.<br>2. Read best bid and ask. | Highest bid and lowest ask are returned as `Decimal` levels. | SUITE-UNIT |
| OB-002 | P0 | REQ-SYNC-001／SCN-008 | Valid book at update 100; continuous update 101 | 1. Apply update.<br>2. Read state. | New levels are added, zero-quantity levels are removed, and update ID becomes 101. | SUITE-UNIT |
| OB-003 | P0 | REQ-SYNC-001／SCN-008 | Valid book at update 100; event ending at 99 | 1. Apply stale event.<br>2. Compare state. | Return `False`; update ID and visible levels do not change. | SUITE-UNIT |
| OB-004 | P0 | REQ-SYNC-001／SCN-008 | Valid book at update 100; next event starts at 105 | 1. Apply gapped event.<br>2. Inspect exception and state. | Raise `SequenceGapError` before any state mutation. | SUITE-UNIT |
| OB-005 | P0 | REQ-SYNC-001／SCN-002 | DATA-NUMERIC-INVALID crossed snapshot | 1. Construct the book. | Raise `MarketInvariantError` with bid／ask values. | SUITE-UNIT |
| OB-006 | P0 | REQ-SYNC-001／SCN-007 | Snapshot 100 plus stale and continuous buffered events | 1. Synchronize snapshot and events.<br>2. Read final state. | Discard stale event and apply continuous events through update 102. | SUITE-UNIT |
| OB-007 | P0 | REQ-SYNC-001／SCN-002 | Parameter rows: zero price, zero quantity, negative quantity | 1. Construct each snapshot row. | Every parameter row raises `MarketInvariantError`. | SUITE-UNIT |
| OB-008 | P0 | REQ-SYNC-001／SCN-008 | Valid book; update with negative quantity | 1. Apply update. | Raise `MarketInvariantError`; zero remains reserved for deletion. | SUITE-UNIT |
| OB-009 | P0 | REQ-SYNC-001／SCN-002 | DATA-NUMERIC-INVALID rows with an empty bid side or empty ask side | 1. Construct each snapshot row. | Every row raises `MarketInvariantError` because both market sides are required. | SUITE-UNIT |
| REST-001 | P1 | REQ-REST-001／SCN-001 | DATA-OB-VALID mock `bookTicker`; lowercase input symbol | 1. Request ticker.<br>2. Inspect request.<br>3. Inspect result. | Send `BTCUSDT`; return normalized symbol and `Decimal` values. | SUITE-REST-CONTRACT |
| REST-002 | P0 | REQ-REST-001／SCN-001 | Mock ticker with bid above ask | 1. Request ticker. | Raise `RestContractError` for crossed market data. | SUITE-REST-CONTRACT |
| REST-003 | P1 | REQ-REST-002／SCN-002 | Valid mock depth; input `btcusdt`; limit 5 | 1. Request depth.<br>2. Inspect request and result. | Send normalized symbol and limit; validate snapshot before returning it. | SUITE-REST-CONTRACT |
| REST-004 | P1 | REQ-REST-004／SCN-004 | DATA-REST-ERROR | 1. Request invalid symbol.<br>2. Inspect raised error. | Preserve HTTP 400, exchange code `-1121`, and message. | SUITE-REST-CONTRACT |
| REST-005 | P1 | REQ-REST-003／SCN-003 | One-symbol mock response with trading status and filters | 1. Request exchange info.<br>2. Inspect result. | Return `BTCUSDT`, `TRADING`, `PRICE_FILTER`, and `LOT_SIZE`. | SUITE-REST-CONTRACT |
| REST-006 | P0 | REQ-REST-001／SCN-001 | Mock ticker with zero bid quantity | 1. Request ticker. | Raise `RestContractError` for non-positive value. | SUITE-REST-CONTRACT |
| REST-007 | P1 | REQ-REST-003／SCN-003 | DATA-REST-CARDINALITY with zero or two `exchangeInfo` symbols | 1. Request exchange info. | Raise `RestContractError` unless the response contains one symbol. | SUITE-REST-CONTRACT |
| REST-008 | P1 | REQ-REST-001／SCN-001 | DATA-SCHEMA-INVALID with a missing ticker field or non-object payload | 1. Request ticker. | Raise `RestContractError` with a stable schema message. | SUITE-REST-CONTRACT |
| REST-009 | P1 | REQ-REST-004／SCN-004 | Mock transport raises `httpx.ReadTimeout` | 1. Request ticker. | Preserve `httpx.ReadTimeout` and its message. | SUITE-REST-CONTRACT |
| WS-001 | P1 | REQ-WS-001, REQ-WS-002／SCN-005 | Matching acknowledgement IDs and one valid event | 1. Collect one ticker.<br>2. Inspect sent controls and event. | Subscribe, validate event, unsubscribe, and correlate IDs 1／2. | SUITE-WS-CONTRACT |
| WS-002 | P0 | REQ-WS-002／SCN-006 | Events with update IDs 102 then 101 | 1. Collect two events. | Raise `WebSocketContractError` when the update ID decreases. | SUITE-WS-CONTRACT |
| WS-003 | P1 | REQ-WS-002／SCN-006 | Event symbol `ETHUSDT`; expected `BTCUSDT` | 1. Collect event. | Reject the wrong symbol with both expected and actual values. | SUITE-WS-CONTRACT |
| WS-004 | P0 | REQ-WS-002／SCN-006 | Event with zero quantity | 1. Collect event. | Reject non-positive price or quantity. | SUITE-WS-CONTRACT |
| WS-005 | P0 | REQ-WS-002／SCN-006 | Event with bid above ask | 1. Collect event. | Reject crossed market data. | SUITE-WS-CONTRACT |
| WS-006 | P1 | REQ-WS-001／SCN-005 | Acknowledgement ID 99; expected ID 1 | 1. Start subscription. | Reject the mismatched acknowledgement. | SUITE-WS-CONTRACT |
| WS-007 | P1 | REQ-WS-001／SCN-005 | Valid ticker arrives before unsubscribe acknowledgement | 1. Collect requested event.<br>2. Request unsubscribe.<br>3. Receive in-flight event and then matching acknowledgement. | Ignore the in-flight market event while waiting and complete normally. | SUITE-WS-CONTRACT |
| WS-008 | P0 | REQ-SYNC-001／SCN-007 | Fake REST snapshot 100; stale 100 and continuous 101／102 events | 1. Buffer stream.<br>2. Load snapshot.<br>3. Apply two continuous updates. | Return synchronized book at update 102 with expected bid／ask levels. | SUITE-WS-CONTRACT |
| WS-009 | P1 | REQ-WS-001／SCN-005 | Slow fake connection; timeout 0.01 seconds | 1. Start subscription.<br>2. Wait for acknowledgement. | Raise `TimeoutError` within the configured bound. | SUITE-WS-CONTRACT |
| WS-010 | P1 | REQ-WS-002／SCN-006 | DATA-SCHEMA-INVALID malformed JSON | 1. Start subscription.<br>2. Receive malformed payload. | Raise `WebSocketContractError` with an invalid-JSON message. | SUITE-WS-CONTRACT |
| WS-011 | P1 | REQ-WS-002／SCN-006 | DATA-SCHEMA-INVALID JSON array | 1. Start subscription.<br>2. Receive non-object payload. | Raise `WebSocketContractError` because the protocol payload must be an object. | SUITE-WS-CONTRACT |
| WS-012 | P1 | REQ-WS-002／SCN-006 | DATA-SCHEMA-INVALID ticker missing `A` after a valid acknowledgement | 1. Subscribe.<br>2. Receive incomplete ticker. | Raise `WebSocketContractError` with a stable schema message. | SUITE-WS-CONTRACT |
| DOC-001 | P1 | REQ-EVID-001／SCN-009 | DATA-REPO-METADATA requirements and traceability documents | 1. Parse both documents.<br>2. Compare requirement IDs. | Both documents contain the same requirement ID set. | SUITE-DOC-CONTRACT |
| DOC-002 | P1 | REQ-EVID-001／SCN-009 | DATA-REPO-METADATA catalog, Automation Map, and pytest modules | 1. Compare Case IDs.<br>2. Parse each mapped script.<br>3. Locate each test function. | Every logical Case ID maps to an existing pytest function. | SUITE-DOC-CONTRACT |
| DOC-003 | P2 | REQ-EVID-001／SCN-009 | DATA-REPO-METADATA Markdown files | 1. Parse relative Markdown links.<br>2. Resolve each target. | Every relative link points to an existing path. | SUITE-DOC-CONTRACT |
| DOC-004 | P0 | REQ-SAFE-001／SCN-001 | DATA-REPO-METADATA source, executable tests, and CI workflow | 1. Inspect configured base URLs and endpoint paths.<br>2. Scan for forbidden interface fragments. | Only allowlisted public market-data interfaces are configured; no credential, account, or order interface is referenced. | SUITE-DOC-CONTRACT |

## Live cases

| ID | Priority | Requirement／scenario | Preconditions and data | Atomic actions | Expected result | Suite |
|---|---|---|---|---|---|---|
| LIVE-REST-001 | P1 | REQ-REST-003／SCN-003 | DATA-LIVE-BTCUSDT; public REST reachable | 1. Request exchange info.<br>2. Inspect symbol, status, and filters. | `BTCUSDT` is trading with price and lot-size filters. | SUITE-LIVE |
| LIVE-REST-002 | P1 | REQ-REST-001／SCN-001 | DATA-LIVE-BTCUSDT; public REST reachable | 1. Request book ticker.<br>2. Assert invariants. | Positive quantities and non-crossed top of book. | SUITE-LIVE |
| LIVE-REST-003 | P1 | REQ-REST-002／SCN-002 | DATA-LIVE-BTCUSDT; depth limit 100 | 1. Request depth.<br>2. Build and inspect book. | Positive update ID and valid order-book state. | SUITE-LIVE |
| LIVE-WS-001 | P1 | REQ-WS-001, REQ-WS-002／SCN-005 | DATA-LIVE-BTCUSDT; public WebSocket reachable | 1. Subscribe.<br>2. Collect three events.<br>3. Unsubscribe. | Three valid events with non-decreasing update IDs. | SUITE-LIVE |
| LIVE-SYNC-001 | P0 | REQ-SYNC-001／SCN-007 | DATA-LIVE-BTCUSDT; public REST and WebSocket reachable | 1. Buffer diff depth.<br>2. Load depth snapshot.<br>3. Apply three continuous events. | Synchronized non-crossed book with positive update ID. | SUITE-LIVE |

## Result count

The catalog contains 39 logical Test Case IDs: 34 deterministic and 5 live. Parameterization expands `OB-007`, `OB-009`, `REST-007`, and `REST-008`; `WS-003`／`WS-004`／`WS-005` share three rows of one function. The local review candidate contains 39 deterministic pytest results plus 5 live results. The published baseline still records 25 deterministic plus 5 live results.

The [Automation Map](automation-map.md) links every Case ID to its code path.
