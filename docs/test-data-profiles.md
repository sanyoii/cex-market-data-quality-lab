# Test Data Profiles

Test Data Profiles keep inputs outside action and assertion intent. Deterministic profiles use static case-local values; live tests assert dynamic values through invariants rather than fixed prices.

| Profile ID | Type | Values／generation | Used by | Isolation |
|---|---|---|---|---|
| DATA-OB-VALID | Static valid | Synthetic `lastUpdateId` values near 100; bids below asks; positive decimal prices and quantities | OB-001, OB-002, OB-006, REST-001, REST-003, WS-001, WS-008 | New dictionaries and clients per case |
| DATA-OB-SEQUENCE | Static boundary | Stale range ending at 99／100, continuous event 101／102, and gap 105–106 | OB-003, OB-004, OB-006, WS-002, WS-008 | No shared mutable fixture |
| DATA-NUMERIC-INVALID | Static invalid／boundary | Zero price, zero snapshot quantity, negative snapshot quantity, negative update quantity, empty market side, crossed bid／ask | OB-005, OB-007–OB-009, REST-002, REST-006, WS-004, WS-005 | Parameter values copied into each case |
| DATA-REST-ERROR | Static invalid | Symbol `NOT_A_SYMBOL`; HTTP 400; Binance code `-1121`; message `Invalid symbol.` | REST-004 | Mock response exists only inside the case |
| DATA-WS-CONTROL | Static protocol | Matching IDs 1／2, mismatched ID 99, and an in-flight ticker before unsubscribe acknowledgement | WS-001, WS-006, WS-007, WS-009 | New fake message queue per case |
| DATA-REST-CARDINALITY | Static boundary | Empty symbol list and two-symbol list | REST-007 | Parameter values copied into the case |
| DATA-SCHEMA-INVALID | Static invalid | Missing REST／WebSocket fields, non-object JSON, and malformed JSON | REST-008, WS-010–WS-012 | Mock payload exists only inside each case |
| DATA-REPO-METADATA | Static repository | Canonical IDs, script paths, Markdown links, client defaults, endpoint paths, and workflow text | DOC-001–DOC-004 | Read-only files from the checked-out revision |
| DATA-LIVE-BTCUSDT | Dynamic live | Symbol `BTCUSDT`; REST limit 100; three ticker or applied depth events; current public market values | All LIVE cases | Read-only public requests; no persistent data or cleanup |

## Data rules

- Synthetic hosts use the reserved `.invalid` domain and never make a network request.
- Deterministic prices are assertions fixtures, not representations of current market prices.
- Live cases assert structure and invariants. They do not assert a fixed price, quantity, spread, latency, or event frequency.
- Tests use no destructive payload, account identifier, personal data, secret, database seed, or real-fund input.
- Parameterized inputs count as separate pytest results while retaining the same logical Test Case ID.
