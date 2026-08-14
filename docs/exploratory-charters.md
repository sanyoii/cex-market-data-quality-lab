# Exploratory Test Charters

Status: Designed, not executed. No human exploratory test evidence exists for these charters.

These charters complement the automated suites. An exploratory session requires a named tester, a time box, contemporaneous notes, observed results, and a dated evidence record. Safe fault injection replaces intentional load or disruption of public services.

| Charter | Focus | Safe setup | Probes | Stop condition | Required evidence |
|---|---|---|---|---|---|
| EXP-001 | REST and WebSocket schema drift | Recorded or synthetic payload copies through mock transport and fake connection | Remove required fields; change object types; alter numeric encodings; add unknown fields | Stop after each public parser path has one valid and one changed payload | Payload description, parser result, exception, notes, start／end UTC |
| EXP-002 | Disconnect and resynchronization behavior | Fake connection with injected disconnects; no live traffic generation | Disconnect before snapshot, during buffering, and after applied events; inspect whether state is discarded or left incomplete | Stop when each boundary has an observed recovery requirement | Fault point, local state, observed exception, recovery decision |
| EXP-003 | Symbol and filter boundaries | Static `exchangeInfo` fixtures plus one ordinary public symbol lookup | Zero, one, and multiple symbol entries; absent and unknown filters; lowercase caller input | Stop after cardinality and filter-retention behavior is recorded | Fixture, requested symbol, result, discrepancy notes |
| EXP-004 | Rate-limit and network-policy responses | Mock HTTP 418／429, timeout, DNS, and connection-close signals | Check error preservation, bounded exit, and evidence classification as Fail or Blocked | Stop after each injected infrastructure category has a recorded outcome | Injected signal, elapsed time, exception, classification, retry count |

## Safety boundary

- Do not send load, burst traffic, destructive payloads, authenticated requests, orders, or account operations.
- Do not treat a simulated fault as proof of current public-service behavior.
- Do not mark a charter Passed without a completed session record.
