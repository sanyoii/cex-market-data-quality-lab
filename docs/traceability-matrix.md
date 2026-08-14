# Requirements Traceability Matrix

Status: Local review candidate. Public CI verification pending.

| Requirement | Scenarios | Test Cases／gate | Test Scripts | Verification strength | Latest evidence |
|---|---|---|---|---|---|
| REQ-SAFE-001 | SCN-001, SCN-009 | DOC-004; all LIVE cases | Documentation contract, production clients, workflow permissions | Automated + Live | 39-result local candidate; 2026-08-14 public live baseline |
| REQ-REST-001 | SCN-001 | REST-001, REST-002, REST-006, REST-008, LIVE-REST-002 | REST contract and live REST scripts | Automated + Live | Local candidate and public baseline records |
| REQ-REST-002 | SCN-002, SCN-007 | REST-003, LIVE-REST-003, LIVE-SYNC-001 | REST contract and live REST／WebSocket scripts | Automated + Live | Local candidate and public baseline records |
| REQ-REST-003 | SCN-003 | REST-005, REST-007, LIVE-REST-001 | REST contract and live REST scripts | Automated + Live | Local candidate and public baseline records |
| REQ-REST-004 | SCN-004 | REST-004, REST-009 | `tests/contract/test_rest_contract.py` | Automated | 39-result local candidate |
| REQ-WS-001 | SCN-005 | WS-001, WS-006, WS-007, WS-009, LIVE-WS-001 | WebSocket contract and live scripts | Automated + Live | Local candidate and public baseline records |
| REQ-WS-002 | SCN-005, SCN-006 | WS-001–WS-005, WS-010–WS-012, LIVE-WS-001 | WebSocket contract and live scripts | Automated + Live | Local candidate and public baseline records |
| REQ-SYNC-001 | SCN-002, SCN-007, SCN-008 | OB-001–OB-009, WS-008, LIVE-SYNC-001 | Unit, WebSocket contract, and live WebSocket scripts | Automated + Live | Local candidate and public baseline records |
| REQ-EVID-001 | SCN-009 | DOC-001–DOC-003, SUITE-REGRESSION, SUITE-LIVE | Documentation contract, workflow, and `evidence/` | Automated + Inspection | Local candidate and public baseline records |

## Mapping statement

- Requirements mapped: 9／9 requirements have an executable test or named gate.
- Scenarios mapped: 9／9 scenarios have at least one Test Case or suite gate.
- Logical cases mapped: 39／39 Test Case IDs have an exact pytest function reference.
- Local candidate result count: parameterization expands 34 deterministic logical cases to 39 deterministic pytest results. The five live logical cases bring the potential execution total to 44 results.
- Published result count: the 2026-08-14 baseline records 25 deterministic plus 5 manually triggered live automation results.

These are traceability mappings, not source-code line or branch coverage. The local candidate has no public CI evidence until it is committed and a workflow run completes.
