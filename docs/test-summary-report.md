# Test Summary Report

Status: PASS for the published implementation baseline verified on 2026-08-14.

## Release conclusion

The public market-data baseline satisfies its defined exit criteria:

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

The recorded implementation revision is `b1397ef67a0b1d364a4d776c21effac6e4d452c1`. Later documentation-only commits do not change the tested Python implementation.

The uncommitted local review candidate expands the deterministic suite to 39 results. It is not part of this published PASS conclusion until public CI verifies it.

## Defect history

| ID | Severity | Status | Detection | Cause and correction | Regression coverage |
|---|---|---|---|---|---|
| DEF-WS-001 | S2 Medium | Closed | Initial live unsubscribe flow: 3 passed, 1 failed | A valid in-flight ticker arrived before the unsubscribe acknowledgement. The client treated it as an invalid acknowledgement. The failure produced a false negative after data collection; it did not corrupt market state or cross the safety boundary. The fix waits past market events for the matching request ID while still rejecting a wrong acknowledgement ID. | WS-006, WS-007 and the final five-case live suite |

The failed attempt remains in the local execution record. Closing a defect does not erase its original evidence.
