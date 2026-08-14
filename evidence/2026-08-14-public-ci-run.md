# Public CI and Live Verification: 2026-08-14

Status: Passed for implementation commit `b1397ef67a0b1d364a4d776c21effac6e4d452c1`.

Start and end UTC timestamps were not captured in the original Markdown receipt. GitHub preserves job timing on the linked run pages. The receipt retains only elapsed time where the original pytest result recorded it.

## Public repository

- Repository: [sanyoii/cex-market-data-quality-lab](https://github.com/sanyoii/cex-market-data-quality-lab)
- Visibility: public
- Branch: `main`
- Runner: GitHub-hosted `ubuntu-24.04`
- Workflow permissions: `contents: read`

The project uses public Binance market-data endpoints only. The workflow receives no API key, account data, order permissions, or repository secret.

## Push-triggered deterministic run

- Run: [31813000448](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31813000448)
- Event: `push`
- Source revision: `b1397ef67a0b1d364a4d776c21effac6e4d452c1`
- Python 3.12: success, 25 tests passed
- Python 3.14: success, 25 tests passed
- JUnit XML: uploaded separately for both Python versions
- Successful-job annotations: 0
- Result counts per matrix job: 25 collected, 25 passed, 0 failed, 0 skipped, 0 deselected
- Exit code: 0; retry count: 0

## Manually triggered live market-data automation run

- Run: [31813158985](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31813158985)
- Event: `workflow_dispatch`
- Source revision: `b1397ef67a0b1d364a4d776c21effac6e4d452c1`
- Deterministic Python 3.12 job: success
- Deterministic Python 3.14 job: success
- Live Python 3.14 job: 5 tests passed in 26.07s
- Live JUnit artifact: `live-market-data`, artifact ID `9223935736`
- Live artifact SHA-256: `8b29215367b9928d8d212ed7de7ed4b46c62a34455ecb5dc3dd0b34cd51cc9d3`
- Successful-job annotations: 0
- Live counts: 5 collected, 5 passed, 0 failed, 0 skipped, 0 deselected
- Live exit code: 0; retry count: 0

The live job checked Binance public `exchangeInfo`, `bookTicker`, REST depth, the book-ticker stream, and REST snapshot／diff-depth synchronization for `BTCUSDT`.

This was automated pytest execution started through `workflow_dispatch`. No human exploratory test was executed.

## Superseded warning

The first public run on commit `3fdca9a51230052a0d334875be7af830e42ca2d5` passed its deterministic jobs but reported Node.js runtime deprecation annotations from older Action versions. Commit `b1397ef67a0b1d364a4d776c21effac6e4d452c1` updated `checkout`, `setup-python`, and `upload-artifact` to their official v7 releases. The verified runs above returned no annotations.

## Remaining limits

- Live results prove the observed behavior at the recorded time, not future Binance availability.
- External API schemas, rate limits, regional policy, DNS, and runner network policy can change.
- The workflow covers public market data; it does not test authentication, balances, orders, or real funds.
