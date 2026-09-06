# Test Summary Report

Status: Current public head has deterministic PASS and no current-head live result. The historical implementation baseline retains its 2026-08-14 PASS.

## Release conclusion

The historical public market-data baseline satisfies its recorded exit criteria:

- Python 3.12 deterministic: 25 passed.
- Python 3.14 deterministic: 25 passed.
- Python 3.14 manually triggered live automation: 5 passed.
- Successful final-head job annotations: 0.
- Open S0／S1 defects: 0 known.
- Test retries: 0.

The conclusion applies only to the documented public market-data scope. It does not certify authentication, account, order, wallet, KYC／AML, performance, security, or production reconnect behavior.

## Published execution evidence

- [Implementation verification record](../evidence/2026-08-14-public-ci-run.md)
- [Final-head deterministic run 31813499294](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31813499294)
- [Final-head manually triggered live run 31813561202](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31813561202)

Public head `8fd5081254b5429e480ec20a56ef09bcc6f5ab9e` passed 39 deterministic results on Python 3.12 and 3.14 in [run 31823105148](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31823105148). Its live job was skipped by push rules, so current-head publication verification remains Incomplete.

The uncommitted local governance candidate passed 40 deterministic and 5 live results with zero retries. It is not part of a public PASS conclusion until public CI verifies it. The latest public live receipt remains the historical `9ce65e0` [run 31813561202](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31813561202).

See the [local candidate record](../evidence/2026-08-15-governance-candidate-run.md) and [current-head status record](../evidence/2026-08-15-current-head-ci-status.md).

## Defect history

| ID | Severity | Status | Detection | Cause and correction | Regression coverage |
|---|---|---|---|---|---|
| DEF-WS-001 | S2 Medium | Closed | Initial live unsubscribe flow: 3 passed, 1 failed | A valid in-flight ticker arrived before the unsubscribe acknowledgment. The client treated it as an invalid acknowledgment. The failure produced a false negative after data collection; it did not corrupt market state or cross the safety boundary. The fix waits past market events for the matching request ID while still rejecting a wrong acknowledgment ID. | WS-006, WS-007 and the final five-case live suite |

The failed attempt remains in the local execution record. Closing a defect does not erase its original evidence.
